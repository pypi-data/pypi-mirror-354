#!/usr/bin/env python3
import asyncio
from pawnlib.builder.generator import generate_banner
from pawnlib.__version__ import __version__ as _version
from pawnlib.config import pawn, pconf, create_app_logger
from pawnlib.utils.http import  NetworkInfo, AsyncIconRpcHelper, append_http
from pawnlib.typing import StackList

# from pawnlib.metrics.tracker import TPSCalculator, SyncSpeedTracker, BlockDifferenceTracker, calculate_reset_percentage, calculate_pruning_percentage
# from pawnlib.output import print_var
from collections import deque
import os
from pawnlib.input.prompt import CustomArgumentParser, ColoredHelpFormatter
# from pawnlib.typing.date_utils import format_seconds_to_hhmmss, second_to_dayhhmm
import json
import aiohttp

from pawnlib.blockchain.goloop.p2p import P2PNetworkParser
from pawnlib.blockchain.goloop.monitor import NodeStatsMonitor
from pawnlib.blockchain.goloop.info import NodeInfoFetcher, NodeInfoFormatter

__description__ = "A powerful and flexible tool for real-time blockchain node and network monitoring."

__epilog__ = (
    "Available Commands:",
    "-------------------",
    "- **stats**: Monitors the blockchain node status, calculates TPS, and estimates synchronization times.",
    "- **info**: Fetches and displays detailed information about the node and network configuration.",
    "",
    "Key Features:",
    "-------------",
    "- **Blockchain Node Monitoring**: Analyze synchronization status, transaction rates (TPS),",
    "  and block differences in real time.",
    "- **Comparison Support**: Compare local node performance with external nodes to identify",
    "  synchronization gaps.",
    "- **Customizable Intervals**: Set data refresh intervals for dynamic tracking of metrics.",
    "- **Detailed Logging**: Leverage verbosity levels to control log output and view additional details.",
    "",
    "Examples:",
    "---------",
    "1. **Monitor Node Stats**:",
    "   pawns goloop stats --url http://localhost:9000",
    "",
    "2. **View Node Information**:",
    "   pawns goloop info --url http://localhost:9000",
    "",
    "3. **Add Comparison with External Node**:",
    "   pawns goloop stats --url http://localhost:9000 --compare-url http://external-node.com",
    "",
    "4. **Set Custom Update Interval**:",
    "   pawns goloop stats --url http://localhost:9000 --interval 2",
    "",
    "5. **Verbose Output for Debugging**:",
    "   pawns goloop stats --url http://localhost:9000 --verbose",
    "",
    "6. **Quiet Mode for Minimal Logs**:",
    "   pawns goloop stats --url http://localhost:9000 --quiet",
    "",
    "Options:",
    "--------",
    "- `command`        The action to perform. Choices are `stats` or `info` (default: `stats`).",
    "- `--url`          The target node's API endpoint (required).",
    "- `--compare-url`  Optional external API endpoint for node comparison.",
    "- `--interval`     Update interval in seconds (default: 1).",
    "- `--verbose`      Increase verbosity for detailed logs.",
    "- `--quiet`        Suppress output for minimal logging.",
    "",
    "Get Started:",
    "------------",
    "This tool offers in-depth analysis for monitoring blockchain nodes and network metrics.",
    "Run `--help` for more details or consult the documentation."
)
from aiohttp import ClientSession
import atexit


_SESSION_POOL = None

def get_session_pool():
    global _SESSION_POOL
    if _SESSION_POOL is None:
        _SESSION_POOL = ClientSession(connector=aiohttp.TCPConnector(limit=20, force_close=True))
    return _SESSION_POOL

async def cleanup_session_pool():
    global _SESSION_POOL
    if _SESSION_POOL is not None and not _SESSION_POOL.closed:
        await _SESSION_POOL.close()
        _SESSION_POOL = None

# 프로그램 종료 시 세션 풀 정리
def cleanup_on_exit():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cleanup_session_pool())
    loop.close()

atexit.register(cleanup_on_exit)


def get_parser():
    parser = CustomArgumentParser(
        description='monitor',
        epilog=__epilog__,
        formatter_class=ColoredHelpFormatter
    )
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument('command',
                        help='The action to perform. Choose "stats" to monitor the node or "info" to display node details.',
                        choices=['stats', 'check', 'info', 'p2p'],
                        type=str, nargs='?', default="stats"
                        )
    parser.add_argument('-c', '--config-file', type=str, help='config', default="config.ini")
    parser.add_argument('-v', '--verbose', action='count', help='verbose mode. view level (default: %(default)s)', default=1)
    parser.add_argument('-q', '--quiet', action='count', help='Quiet mode. Dont show any messages. (default: %(default)s)', default=0)
    parser.add_argument('-i', '--interval', type=float, help='interval sleep time seconds. (default: %(default)s)', default=2)
    parser.add_argument('-b', '--base-dir', type=str, help='base dir for httping (default: %(default)s)', default=os.getcwd())
    parser.add_argument('-u', '--url', type=str, help='printing type  %(default)s)', default="localhost:9000")
    parser.add_argument('-cu', '--compare-url', type=str, help='compare url  %(default)s)', default=None)
    parser.add_argument('-f', '--filter',
                        nargs='*',
                        type=str,
                        help='Filtering keys to fetch from the network (e.g., --filter node_info chain_info)',
                        default=[])
    parser.add_argument('-t', '--target-key',
                        type=str,
                        help='Recursively extract a specific key\'s value from the fetched data.',
                        default=None)
    parser.add_argument('--host', type=str, help='host (default: %(default)s)', default="localhost")
    parser.add_argument('-p', '--ports', nargs='+', type=int, help='List of ports to connect to', default=None)

    parser.add_argument( '--log-type', choices=['console', 'file', 'both'], default='console', help='Choose logger type: console or file (default: console)')
    parser.add_argument('--max-concurrent', type=int, help='Maximum concurrent connections for P2P analysis (default: %(default)s)', default=5)
    parser.add_argument('--timeout', type=int, help='timeout  (default: %(default)s)', default=5)
    parser.add_argument('--max-depth', type=int, help='depth  (default: %(default)s)', default=3)

    return parser


def save_output(data, file_path, format='text'):
    """
    Saves output to a file in the specified format.

    :param data: The data to be saved.
    :param file_path: The path to the output file.
    :param format: The format of the output, 'json' or 'text'.
    """
    try:
        if format == 'json':
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        elif format == 'text':
            with open(file_path, 'w') as f:
                if isinstance(data, str):
                    f.write(data)
                else:
                    f.write(json.dumps(data, indent=4))
        print(f"[green]Output saved to {file_path} in {format} format.[/green]")
    except Exception as e:
        print(f"[red]Failed to save output:[/red] {e}")


def print_banner():
    banner = generate_banner(
        app_name=pconf().app_name,
        author="jinwoo",
        description=f"{__description__} \n"
                    f" - base_dir    : {pconf().args.base_dir} \n"
                    f" - logs_dir    : {pconf().args.base_dir}/logs \n",
        font="graffiti",
        version=_version
    )
    print(banner)

async def find_open_ports(start_port=9000, end_port=9999):

    tasks = [check_port(port) for port in range(start_port, end_port + 1)]
    results = await asyncio.gather(*tasks)
    open_ports = [port for port, is_open in results if is_open]
    pawn.console.log(f"Checking for open ports... ({start_port} ~ {end_port}), Found: {open_ports}")
    return open_ports


async def check_port(port):
    loop = asyncio.get_event_loop()
    try:
        await loop.create_connection(lambda: asyncio.Protocol(), 'localhost', port)
        pawn.console.debug(f"Port {port} is open.")
        return port, True
    except:
        return port, False


def calculate_tps(heights, times, sleep_duration=1):
    if len(heights) < 2:
        return 0, 0
        # 최근 TPS 및 평균 TPS 계산
    recent_tx_count = heights[-1] - heights[-2]
    avg_tx_count = heights[-1] - heights[0]

    recent_tps = recent_tx_count / sleep_duration if sleep_duration > 0 else 0
    avg_tps = avg_tx_count / (times[-1] - times[0]) if (times[-1] - times[0]) > 0 else 0
    return recent_tps, avg_tps, recent_tx_count

async def find_and_check_stat(sleep_duration=2, host="localhost", ports=None):
    refresh_interval = 30  # 포트 갱신 간격 (초)
    last_refresh_time = asyncio.get_event_loop().time()

    # 초기 포트 스캔
    if ports:
        open_ports = ports
    else:
        open_ports = await find_open_ports()
    if not open_ports:
        pawn.console.log("No open ports found. Exiting.")
        return

    block_heights = {port: deque(maxlen=60) for port in open_ports}
    block_times = {port: deque(maxlen=60) for port in open_ports}
    consecutive_failures = {port: 0 for port in open_ports}

    api_url = append_http(host)

    async with AsyncIconRpcHelper(logger=pawn.console, timeout=2, return_with_time=False, retries=1) as rpc_helper:

        while True:
            current_time = asyncio.get_event_loop().time()

            # 주기적 포트 갱신 (초기 스캔 이후)
            if current_time - last_refresh_time >= refresh_interval:
                if ports:
                    new_open_ports = ports
                else:
                    new_open_ports = await find_open_ports()
                last_refresh_time = current_time

                # 새로운 포트 추가
                for port in new_open_ports:
                    if port not in open_ports:
                        open_ports.append(port)
                        block_heights[port] = deque(maxlen=60)
                        block_times[port] = deque(maxlen=60)
                        consecutive_failures[port] = 0

                # 닫힌 포트 제거
                closed_ports = [port for port in open_ports if port not in new_open_ports]
                for port in closed_ports:
                    open_ports.remove(port)
                    del block_heights[port]
                    del block_times[port]
                    del consecutive_failures[port]

            # tasks = [fetch_chain(rpc_helper.session, port) for port in open_ports]
            # tasks = [rpc_helper.fetch(f":{port}/admin/chain", return_first=True) for port in open_ports]

            tasks = [rpc_helper.fetch(url=f"{api_url}:{port}/admin/chain", return_first=True) for port in open_ports]
            results = await asyncio.gather(*tasks)

            active_ports = 0
            total_ports = len(open_ports)


            for port, result in zip(open_ports, results):
                state = ""
                if result and result is not None and isinstance(result, dict):
                    active_ports += 1
                    nid = result.get('nid')
                    height = result.get('height')
                    state = result.get('state', "N/A")
                    if "reset" in state:
                        _state = calculate_reset_percentage(state)
                        state = f"reset {_state.get('reset_percentage')}%"
                    elif "pruning" in state:
                        _state = calculate_pruning_percentage(state)
                        # state = f"reset {_state.get('reset_percentage')}%"
                        state = f"Progress  {_state.get('progress')}% ({_state.get('resolve_progress_percentage')}%) | "

                    block_heights[port].append(height)
                    block_times[port].append(current_time)

                    if len(block_heights[port]) >= 2:
                        recent_tps, avg_tps, recent_tx_count = calculate_tps(
                            list(block_heights[port]),
                            list(block_times[port]),
                            sleep_duration=sleep_duration
                        )
                        status = "ok"
                        consecutive_failures[port] = 0
                    else:
                        recent_tps = avg_tps = recent_tx_count = 0
                        status = 'initializing'
                else:
                    status = 'no result'
                    nid = 'N/A'
                    height = 'N/A'
                    recent_tps = avg_tps = recent_tx_count = 0
                    consecutive_failures[port] += 1

                if consecutive_failures[port] >= 3:
                    status = 'warn'

                if status != "ok":
                    status_color = "[red]"
                elif avg_tps == 0 and recent_tps == 0:
                    status_color = "[red]"
                elif avg_tps and avg_tps > 1:
                    status_color = "[yellow]"
                else:
                    status_color = "[dim]"

                try:
                    if state:
                        if state == "started":
                            server_state = ""
                        else:
                            server_state = state

                        pawn.console.log(f'{status_color}Port {port}: Status={status:<3}, Height={height:,}, nid={nid}, '
                                         f'TPS(AVG)={avg_tps:5.2f}, [dim]TPS={recent_tps:5.2f}[/dim], '
                                         f'TX Cnt={recent_tx_count:<3},{server_state}')
                    else:
                        pawn.console.log(f'{status_color}Port {port}, result={result}')

                except Exception as e:
                    pawn.console.log(f"Error in AsyncIconRpcHelper : port={port}, error={e}, result={result}, status={status}")

            pawn.console.debug(f"Active Ports: {active_ports}/{total_ports}")
            await asyncio.sleep(sleep_duration)

async def run_stats_command(args, network_info):
    _compare_api = ""
    try:
        if args.compare_url:
            pawn.console.log(f"[yellow]Using user-provided compare URL:[/yellow] {args.compare_url}")
            _compare_api = args.compare_url
        else:
            pawn.console.log(f"[yellow]Attempting to find network information for platform:[/yellow] {network_info.platform}, [yellow]NID:[/yellow] {network_info.nid}")
            guessed_network = network_info.find_network_by_platform_and_nid(
                platform=network_info.platform,
                nid=network_info.nid
            )
            pawn.console.log(f"[green]Guessed network info:[/green] {guessed_network}")
            pawn.console.log(f"[green]Guessed network name:[/green] {guessed_network.get('network_name')}")
            _compare_api = guessed_network.get('network_api')

        if not _compare_api:
            pawn.console.log("[red]Could not determine a compare API endpoint. Please provide a valid --compare-url.[/red]")
    except ValueError as e:
        pawn.console.log(f"[red]Error finding network by platform and NID:[/red] {e}")
    except Exception as e:
        pawn.console.log(f"[red]Unexpected error while finding compare API:[/red] {e}")

    if _compare_api:
        pawn.console.log(f"[green]Compare API set to:[/green] {_compare_api}")

    async with aiohttp.ClientSession() as session:
        helper = AsyncIconRpcHelper(session=session, logger=pawn.console, timeout=2, return_with_time=True, retries=1)
        monitor = NodeStatsMonitor(
            network_api=args.url,
            compare_api=_compare_api,
            helper=helper,
            interval=args.interval,
            logger=pawn.console
        )
        await monitor.run()


async def main():
    app_name = 'goloop_stats'
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    config_file = args.config_file

    is_hide_line_number = args.verbose > 2
    stdout = not args.quiet

    logger = create_app_logger(
        app_name=app_name,
        log_type=args.log_type,
        verbose=args.verbose,
        propagate=True,
    )

    pawn.set(
        # PAWN_CONFIG_FILE=config_file,
        # PAWN_PATH=args.base_dir,
        # PAWN_CONSOLE=dict(
        #     redirect=True,
        #     record=True,
        #     log_path=is_hide_line_number, # hide line number on the right side
        # ),
        app_name=app_name,
        args=args,
        try_pass=False,
        last_execute_point=0,
        data={
            "response_time": StackList(),
        },
        logger=logger,
        fail_count=0,
        total_count=0,
    )

    if args.verbose > 2:
        pawn.set(
            PAWN_LOGGER=dict(
                log_level="DEBUG",
                stdout_level="DEBUG",
                # log_path=f"{args.base_dir}/logs",
                stdout=stdout,
                use_hook_exception=True,
                show_path=False, #hide line numbers
            ),
        )

    print_banner()
    pconf().logger.info(args)
    network_info = NetworkInfo(network_api=append_http(args.url))

    if args.command == "info":
        fetcher = NodeInfoFetcher()
        pawn.console.log(network_info)
        node_data = await fetcher.fetch_all(url=network_info.network_api, filter_keys=args.filter, target_key=args.target_key)
        formatter = NodeInfoFormatter(logger=pawn.console)
        formatter.print_tree(node_data)
    elif args.command == "stats":
        try:
            await run_stats_command(args, network_info)
        except Exception as e:
            pawn.console.log(f"[red]Error during stats display:[/red] {e}")
    elif args.command == "check":
        await find_and_check_stat(sleep_duration=args.interval, host=args.host, ports=args.ports)

    elif args.command == "p2p":
        try:
            parser = P2PNetworkParser(
                args.url,
                max_concurrent=args.max_concurrent,
                timeout=args.timeout, logger=logger, max_depth=args.max_depth, verbose=args.verbose
            )
            ip_to_hx_map = await parser.run()

            pawn.console.rule("[bold blue]P2P Network Analysis[/bold blue]")
            total_peer_ip_count = len(ip_to_hx_map.get('ip_to_hx'))
            pawn.console.log(f"Total Peer Count = {total_peer_ip_count}")

            for hx_address, peer_info in ip_to_hx_map['hx_to_ip'].items():
                if peer_info.ip_count > 1 and peer_info.hx:
                    pawn.console.log(peer_info)
        except Exception as e:
            pawn.console.log(f"[red]Error during P2P analysis:[/red] {e}")


def guess_network(network_info):
    try:
        guessed_network = network_info.find_network_by_platform_and_nid(
            platform=network_info.platform,
            nid=network_info.nid
        )
        pawn.console.log(f"[green]Guessed network info:[/green] {guessed_network}")
        pawn.console.log(f"[green]Guessed network name:[/green] {guessed_network.get('network_name')}")
        return guessed_network
    except Exception as e:
        pawn.console.log(f"{e}")
        return {}


main.__doc__ = (
    f"{__description__} \n"
    f"{__epilog__}"
)

if __name__ == '__main__':

    try:
        asyncio.run(main())
    except Exception as e:
        pawn.console.log(e)
