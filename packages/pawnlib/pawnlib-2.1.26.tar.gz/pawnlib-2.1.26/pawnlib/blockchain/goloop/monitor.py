
from pawnlib.metrics.tracker import TPSCalculator, SyncSpeedTracker, BlockDifferenceTracker, calculate_reset_percentage, calculate_pruning_percentage
from pawnlib.utils.http import AsyncIconRpcHelper, append_http
from pawnlib.typing.date_utils import format_seconds_to_hhmmss, second_to_dayhhmm
from pawnlib.config import pawn, LoggerMixinVerbose
import time
from typing import Optional

import asyncio


class NodeStatsMonitor(LoggerMixinVerbose):
    """
    Monitors a Goloop node by periodically polling its status and computing statistics.
    """
    def __init__(
        self,
        network_api: str,
        compare_api: str,
        helper: Optional[AsyncIconRpcHelper] = None,
        interval: int = 2,
        history_size: int = 100,
        log_interval: int = 20,
        logger=None,
    ):
        """
        Initialize the NodeStatsMonitor.

        :param network_api: RPC URL of the target node to monitor.
        :param compare_api: RPC URL of the node to compare against.
        :param helper: Optional AsyncIconRpcHelper instance for RPC calls. If None, a default helper is created.
        :param interval: Polling interval in seconds between data fetches.
        :param history_size: Number of entries to retain for TPS, block diff, and sync speed calculations.
        :param log_interval: Number of polls between full static information logs.
        :param logger: Optional logger instance. If None, a default logger is initialized.
        """
        self.network_api = network_api
        self.compare_api = compare_api
        self.helper = helper or AsyncIconRpcHelper(logger=pawn.console, timeout=2, return_with_time=True, retries=1)

        self.interval = interval
        self.log_interval = log_interval
        self.init_logger(logger=logger, verbose=1)


        # 상태를 가지는 추적기들을 인스턴스 변수로 관리
        self.tps_calculator = TPSCalculator(history_size=history_size, variable_time=True)
        self.block_tracker = BlockDifferenceTracker(history_size=history_size)
        self.sync_speed_tracker = SyncSpeedTracker(history_size=history_size)

    async def _fetch_data(self) -> dict:
        """
        Asynchronously fetch chain information from the target and comparison nodes.

        :return: A dict with 'target_node' and 'external_node' keys, each containing the fetched data
                 along with elapsed time or error details.
        """
        try:
            target_node, target_node_time = await self.helper.fetch(
                url=f"{self.network_api}/admin/chain", return_first=True
            )

            target_node = (
                {"elapsed": target_node_time, **target_node}
                if isinstance(target_node, dict)
                else {"elapsed": target_node_time, "error": "Invalid target node response"}
            )

        except Exception as e:
            target_node = {"error": f"Failed to fetch target node data: {e}"}

        if self.compare_api:
            try:
                external_height, external_node_time = await self.helper.get_last_blockheight(url=self.compare_api)

                external_node = {
                    "elapsed": external_node_time,
                    "height": external_height,
                } if external_height else {
                    "elapsed": external_node_time,
                    "error": "Failed to fetch external node block height"
                }

            except Exception as e:
                external_node = {"error": f"Failed to fetch external node data: {e}"}
        else:
            external_node = {}

        return {"target_node": target_node, "external_node": external_node}

    def _process_stats(self, data: dict) -> dict:
        """
        Compute statistical metrics based on fetched node data.

        :param data: Dictionary containing 'target_node' and 'external_node' data entries.
        :return: A dict with calculated metrics including:
                 - height: Current block height
                 - tps: Transactions per second (current)
                 - avg_tps: Average transactions per second
                 - tx_count: Number of transactions in the last interval
                 - diff: Block height difference to external node
                 - state: Node state
                 - last_error: Last error message from the node
                 - cid, nid, channel: Node identifiers
                 - sync_time: Estimated time to sync (if applicable)
        """
        target_node = data.get('target_node', {})
        external_node = data.get('external_node', {})


        current_height = target_node.get('height')

        if not isinstance(current_height, int):
            raise ValueError(f"Invalid 'height' received from {self.network_api}")

        current_time = time.time()
        self.sync_speed_tracker.update(current_height, current_time)

        external_height = external_node.get("height", 0)
        block_difference = external_height - current_height if external_height > 0 else 0
        self.block_tracker.add_difference(block_difference)

        current_tps, average_tps = self.tps_calculator.calculate_tps(current_height, current_time)

        stats = {
            "height": current_height,
            "tps": current_tps,
            "avg_tps": average_tps,
            "tx_count": self.tps_calculator.last_n_tx(),
            "diff": block_difference,
            "state": target_node.get('state'),
            "last_error": target_node.get('lastError'),
            "cid": target_node.get('cid'),
            "nid": target_node.get('nid'),
            "channel": target_node.get('channel'),
        }

        avg_speed = self.sync_speed_tracker.get_average_sync_speed()
        if block_difference > 1 and avg_speed > 0:
            estimated_seconds = block_difference / avg_speed
            stats["sync_time"] = second_to_dayhhmm(estimated_seconds)

        return stats

    def _format_log_message(self, stats: dict) -> str:
        """
        Format computed statistics into a human-readable log message.

        :param stats: Dictionary of computed metrics from _process_stats.
        :return: Formatted log string, with static info prepended at configured intervals.
        """
        dynamic_parts = [
            f"Height: {stats['height']}",
            f"TPS: {stats['tps']:.2f} (Avg: {stats['avg_tps']:.2f})",
            f"TX Count: {stats['tx_count']:.2f}",
            f"Diff: {stats['diff']}",
        ]
        if stats.get("sync_time"):
            dynamic_parts.append(f"Sync Time: {stats['sync_time']}")


        if stats['state'] != "started" or stats['last_error']:
            state_msg = f"State: {stats['state']} | lastError: {stats['last_error']}"
            if "reset" in stats['state']:
                _state = calculate_reset_percentage(stats['state'])
                state = f"reset {_state.get('reset_percentage')}%"

            elif "pruning" in stats['stats']:
                _state = calculate_pruning_percentage(stats['state'])
                # state = f"reset {_state.get('reset_percentage')}%"
                state_msg = f"Progress  {_state.get('progress')}% ({_state.get('resolve_progress_percentage')}%) | "

            dynamic_parts.append(f"[red]{state_msg}[/red]")
        log_message = " | ".join(dynamic_parts)

        if (self.tps_calculator.call_count % self.log_interval) == 1:
            static_parts = [
                f"{self.network_api}",
                f"channel: {stats.get('channel', 'N/A')}",
                f"cid: {stats.get('cid', 'N/A')}",
                f"nid: {stats.get('nid', 'N/A')}"
            ]
            static_log_message = ", ".join(static_parts)
            return f"[bold blue]{static_log_message}[/bold blue]\n{log_message}"

        return log_message

    async def run(self):
        """
        Start the monitoring loop.

        Continuously fetches node data, processes statistics, logs the output,
        and sleeps for the configured interval.
        """
        self.logger.info(f"Starting node monitor for {self.network_api}...")
        while True:
            try:
                start_time = time.time()
                raw_data = await self._fetch_data()

                processed_stats = self._process_stats(raw_data)
                log_message = self._format_log_message(processed_stats)
                self.logger.info(log_message)

                elapsed_time = time.time() - start_time
                sleep_time = self.interval - elapsed_time
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            except Exception as e:
                self.logger.error(f"An error occurred in monitor loop: {e}", exc_info=True)
                await asyncio.sleep(self.interval)
