
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


# async def display_stats_async(network_api, compare_api="", history_size=100, interval=2, log_interval=20):
#     """
#     Fetches data from a network API, calculates TPS (Transactions Per Second), and logs the results.

#     This function periodically calls a specified network API to retrieve blockchain-related data,
#     calculates various metrics such as TPS and synchronization speed, and logs the information
#     in a structured format. It also estimates the time required for synchronization if applicable.

#     :param network_api: The API endpoint to fetch data from.
#     :type network_api: str
#     :param compare_api: An optional external API endpoint to compare synchronization status.
#     :type compare_api: str, optional
#     :param history_size: The size of the history buffer for calculating moving averages of TPS and sync speed.
#     :type history_size: int
#     :param interval: The time interval (in seconds) between API calls.
#     :type interval: int
#     :param log_interval: The number of calls after which static information is re-logged.
#     :type log_interval: int

#     Example:
#         .. code-block:: python

#             # Basic usage with default parameters
#             display_stats(network_api="http://localhost:9000/api/v1/status")

#             # With an external API for comparison
#             display_stats(
#                 network_api="http://localhost:9000/api/v1/status",
#                 compare_api="http://external-node.com/api/v1/status"
#             )

#             # Custom history size and intervals
#             display_stats(
#                 network_api="http://localhost:9000/api/v1/status",
#                 history_size=200,
#                 interval=5,
#                 log_interval=50
#             )
#     """
#     tps_calculator = TPSCalculator(history_size=history_size, variable_time=True)
#     block_tracker = BlockDifferenceTracker(history_size=history_size)
#     sync_speed_tracker = SyncSpeedTracker(history_size=history_size)
#     helper = AsyncIconRpcHelper(logger=pawn.console, timeout=2, return_with_time=True, retries=1)

#     while True:
#         try:
#             start_time = time.time()
#             result = await fetch_admin_chain(target_url=network_api, external_url=compare_api, helper=helper)

#             target_node = result.get('target_node', {})
#             current_height = target_node.get('height')
#             current_time = time.time()

#             if current_height is None or not isinstance(current_height, int):
#                 pawn.console.log(f"[red]Error:[/red] Invalid 'height' value received from {network_api}. result={result}")

#                 time.sleep(2)
#                 return

#             sync_speed_tracker.update(current_height, current_time)
#             average_sync_speed = sync_speed_tracker.get_average_sync_speed()

#             external_height = result.get("external_node", {}).get("height", 0)
#             block_difference = external_height - current_height
#             block_tracker.add_difference(block_difference)

#             if block_difference > 1:
#                 if average_sync_speed and average_sync_speed > 0:
#                     estimated_sync_time_seconds = block_difference / average_sync_speed
#                     estimated_sync_time_display = second_to_dayhhmm(estimated_sync_time_seconds)
#                 else:
#                     average_block_time = 2
#                     estimated_sync_time_seconds = block_difference * average_block_time
#                     estimated_sync_time_display = second_to_dayhhmm(estimated_sync_time_seconds)
#                 show_sync_time = True
#             else:
#                 estimated_sync_time_display = None
#                 show_sync_time = False

#             current_tps, average_tps = tps_calculator.calculate_tps(current_height, current_time)
#             last_tx = tps_calculator.last_n_tx()

#             # Prepare dynamic log message
#             dynamic_parts = [
#                 f"Height: {current_height}",
#                 f"TPS: {current_tps:.2f} (Avg: {average_tps:.2f})",
#                 f"TX Count: {last_tx:.2f}",
#                 f"Diff: {block_difference}",
#             ]

#             if show_sync_time and estimated_sync_time_display:
#                 dynamic_parts.append(f"Sync Time: {estimated_sync_time_display}")

#             if target_node.get('state') != "started" or target_node.get('lastError'):
#                 target_state = target_node.get('state')
#                 percent_state = ""
#                 target_state_pct = ""

#                 if "reset" in target_state:
#                     try:
#                         percent_state = calculate_reset_percentage(target_state)
#                         target_state_pct = f"Progress  {percent_state.get('progress')}% | "
#                     except:
#                         pass

#                 elif "pruning" in target_state:
#                     try:
#                         percent_state = calculate_pruning_percentage(target_state)
#                         target_state_pct = f"Progress  {percent_state.get('progress')}% ({percent_state.get('resolve_progress_percentage')}%) | "
#                     except:
#                         pass
#                 else:
#                     target_state_pct = ""
#                 dynamic_parts.append(f"[red]{target_state_pct}State: {target_node['state']} | lastError: {target_node['lastError']}")

#             dynamic_log_message = " | ".join(dynamic_parts)

#             if (tps_calculator.call_count % log_interval) == 1:
#                 static_parts = [
#                     f"{network_api}",
#                     f"channel: {target_node.get('channel', 'N/A')}",
#                     f"cid: {target_node.get('cid', 'N/A')}",
#                     f"nid: {target_node.get('nid', 'N/A')}"
#                 ]
#                 static_log_message = ", ".join(static_parts)
#                 full_log_message = f"[bold blue]{static_log_message}[/bold blue]\n{dynamic_log_message}"
#             else:
#                 full_log_message = dynamic_log_message

#             pawn.console.log(full_log_message)

#             elapsed_time = time.time() - start_time
#             sleep_time = interval - elapsed_time
#             if sleep_time > 0:
#                 time.sleep(sleep_time)

#         except Exception as e:
#             pawn.console.log(f"[red]Exception occurred:[/red] {e}")
#             time.sleep(interval)



# async def fetch_admin_chain(target_url="", external_url="", helper=None):
#     """
#     Fetches data from the target and external ICON nodes.

#     Args:
#         target_url (str): URL of the target ICON node.
#         external_url (str): URL of the external ICON node.

#     Returns:
#         dict: A dictionary containing data from the target and external nodes with elapsed time.
#     """
#     # connector = aiohttp.TCPConnector(limit=20, ssl=False)
#     # session = aiohttp.ClientSession(connector=connector)

#     try:
#         async with helper as rpc_helper:
#             try:
#                 # await check_network_api_availability(target_url)
#                 target_node, target_node_time = await rpc_helper.fetch(
#                     url=f"{target_url}/admin/chain", return_first=True
#                 )

#                 target_node = (
#                     {"elapsed": target_node_time, **target_node}
#                     if isinstance(target_node, dict)
#                     else {"elapsed": target_node_time, "error": "Invalid target node response"}
#                 )
#             except Exception as e:
#                 target_node = {"elapsed": None, "error": f"Failed to fetch target node data: {str(e)}"}

#             if external_url:
#                 try:
#                     # Fetch block height from the external node
#                     external_node_blockheight, external_node_time = await rpc_helper.get_last_blockheight(url=external_url)
#                     external_node = {
#                         "elapsed": external_node_time,
#                         "height": external_node_blockheight,
#                     } if external_node_blockheight else {
#                         "elapsed": external_node_time,
#                         "error": "Failed to fetch external node block height"
#                     }
#                 except Exception as e:
#                     external_node = {"elapsed": None, "error": f"Failed to fetch external node data: {str(e)}"}
#             else:
#                 external_node = {"elapsed": None, "error": f"external url not provided: {external_url}"}

#             result = {
#                 "target_node": target_node,
#                 "external_node": external_node,
#             }
#             return result
#     finally:
#         # 세션을 명시적으로 닫기
#         if helper and getattr(helper, 'session', None) and not helper.session.closed:
#             await helper.close()


# async def fetch_icon_data(url="", guessed_network_endpoint=""):
#     rpc_helper = AsyncIconRpcHelper(
#         url=url,
#         logger=pawn.console
#     )
#     if not await check_network_api_availability(url):
#         pawn.console.log(f"Cannot connect to {url}")
#         return {}

#     await rpc_helper.initialize()

#     if guessed_network_endpoint:
#         preps_name_info =  await rpc_helper.get_node_name_by_address()
#     else:
#         preps_name_info = {}

#     pawn.set(preps_name_info=preps_name_info)

#     last_block_height = await rpc_helper.get_last_blockheight()
#     chain_info = await rpc_helper.fetch("/admin/chain", return_first=True)
#     node_info =  await rpc_helper.fetch("/admin/chain/icon_dex")
#     network_info =  await rpc_helper.get_network_info()

#     await rpc_helper.session.close()

#     return {
#         "node_info": node_info,
#         "network_info": network_info,
#         "chain_info": chain_info,
#         "last_block_height": last_block_height,
#         "preps_name_info": preps_name_info
#     }


# async def check_network_api_availability(network_api):
#     """
#     Checks if the network API is available and the port is open.

#     :param network_api: The network API URL to check.
#     :return: True if the network API is available, False otherwise.
#     """
#     from urllib.parse import urlparse
#     parsed_url = urlparse(append_http(network_api))

#     host = parsed_url.hostname
#     port = parsed_url.port

#     if not host or not port:
#         pawn.console.log("[red]Invalid network API URL provided.[/red]")
#         return False

#     is_open = await is_port_open(host, port)

#     if not is_open:
#         pawn.console.log(f"[red]Port {port} on {host} is not open.[/red]")
#         return False
#     pawn.console.log(f"[green]Port {port} on {host} is open and accessible.[/green]")
#     return True


# async def is_port_open(host, port):
#     """
#     Checks if a specific port on a host is open.

#     :param host: The hostname or IP address to check.
#     :param port: The port number to check.
#     :return: True if the port is open, False otherwise.
#     """
#     try:
#         reader, writer = await asyncio.open_connection(host, port)
#         writer.close()
#         await writer.wait_closed()
#         return True
#     except Exception:
#         return False
