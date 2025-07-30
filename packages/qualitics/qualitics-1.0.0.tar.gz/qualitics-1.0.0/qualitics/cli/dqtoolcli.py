import argparse
import sys
import threading
import uuid
from datetime import datetime
from Checks.Freshness_Check.freshness_monitor import FreshnessMonitor
from Checks.check_runner import CheckRunner
from Config_parser.configService import ConfigLoader
from Connectors.connector_factory import ConnectorFactory
from Profilers.database_profiler import DatabaseProfiler
from Profilers.profilingconfig import run_profiling
from Utils import QueryExecutor
from Utils.profile_store import print_table_profile
from cli.render_check_html import render_check_result_html
from cli.render_profiling_html import render_profiling_html


def run_check_main(args):
    parser = argparse.ArgumentParser(description="Run data quality checks via CLI")

    parser.add_argument(
        "--table", "-t",
        required=True,
        help="Table name (e.g., public.orders)"
    )

    parser.add_argument(
        "--check", "-k",
        nargs="*",
        required=False,
        help="Check(s) to run (e.g., null_check, pii_check)"
    )

    parser.add_argument(
        "--column", "-col",
        help="Optional: Column to apply check on (e.g., order_id)"
    )

    parser.add_argument(
        "--conn", "-c",
        required=True,
        help="Path to dq_config.yml or redshift.yaml"
    )

    parsed_args = parser.parse_args(args)

    # Load config
    config_loader = ConfigLoader().load_config(parsed_args.conn)
    # Configuring correct connector class
    connector = ConnectorFactory.get_connector(config_loader)
    check_id = str(uuid.uuid4())
    alerting_enabled = config_loader.get("alerts", {}).get("enabled", False)
    runner = CheckRunner(full_config=config_loader, connector=connector, check_id=check_id,
                         alerting_enabled=alerting_enabled)


    if parsed_args.check:
        results = runner.run_selected(parsed_args.check)
    else:
        results = runner.run_all()

    print("check_result:" )
    print(results)

    html = render_check_result_html(results)



    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = f"CliCheckResult/dq_check_result_{timestamp}.html"

    with open(html_path, "w") as f:
        f.write(html)

    print(f"Data quality check report saved to {html_path}")

    # Extract failed check names
    failed_checks = [
        r["check_name"]
        for r in results
        if r.get("status", "").lower() != "success"
    ]

    if failed_checks:
        if len(failed_checks) == 1:
            print(f"{failed_checks[0]} failed! Check file at {html_path} for more details.")
        else:
            print(f"{', '.join(failed_checks)} failed! Check file at {html_path} for more details.")


def run_freshnessCheck_main(args):
    parser = argparse.ArgumentParser(description="Run data quality Freshnesschecks via CLI")

    parser.add_argument(
        "--table", "-t",
        required=True,
        help="Table name (e.g., public.orders)"
    )

    parser.add_argument(
        "--check", "-k",
        nargs="*",
        required=False,
        help="Check(s) to run (e.g., null_check, pii_check)"
    )

    parser.add_argument(
        "--conn", "-c",
        required=True,
        help="Path to dq_config.yml or redshift.yaml"
    )

    parsed_args = parser.parse_args(args)

    # Load config
    config_loader = ConfigLoader().load_config(parsed_args.conn)
    print("loading config file completed.................")
    print("connector connecting..............")
    connector = ConnectorFactory.get_connector(config_loader)
    print("running the checks start...............")
    check_id = str(uuid.uuid4())
    alerting_enabled = config_loader.get("alerts", {}).get("enabled", False)
    freshness_check_cfg = [check for check in config_loader['checks'] if check['name'] == 'freshness_check'][0]
    if freshness_check_cfg:
        monitor = FreshnessMonitor(config_loader=config_loader, check_cfg=freshness_check_cfg, \
                                   connector=connector, check_id=check_id,\
                                   alerting_enabled=alerting_enabled)
        # monitor.start()
        t = threading.Thread(target=monitor.start(), daemon=True)
        t.start()


    connector.close()
    print("freshness completed")



def run_profiling_main(args):
    parser = argparse.ArgumentParser(description="Run database profiling via CLI")
    parser.add_argument("--schema", help="Schema name to profile (e.g., public)")
    parser.add_argument("--table", help="Table to profile (e.g., orders)")
    parser.add_argument("--column", help="Optional: Column to profile (e.g., order_id)")
    parser.add_argument("--conn", "-c", required=True, help="Path to dq_config.yml or redshift.yaml")
    parsed_args = parser.parse_args(args)
    config_loader = ConfigLoader().load_config(parsed_args.conn)
    # Configuring correct connector class
    connector = ConnectorFactory.get_connector(config_loader)

    print("profiling started.........")
    executor = QueryExecutor(
        connector,
        config_loader['data_source']['type'],
        config_loader['data_source']
    )
    profiler = DatabaseProfiler(executor)
    print("Starting database profiling...")
    results = run_profiling(profiler, config_loader)
    html = render_profiling_html(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = f"CliProfilerResult/dq_profiler_result_{timestamp}.html"

    with open(html_path, "w") as f:
        f.write(html)


    print(f"Profiling report saved to {html_path}")

    # Clean up
    connector.close()


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        sub_args = sys.argv[2:]

        if command == "run-check":
            run_check_main(sub_args)
        elif command == "run-profile":
            run_profiling_main(sub_args)
        elif command == "run-freshnessCheck":
            run_freshnessCheck_main(sub_args)
        else:
            print(f"\nUnknown command: {command}")
            print_usage()
    else:
        print_usage()


def print_usage():
    print("""
Usage:
  dqtoolss run-check   --table <table> --check <check(s)> --conn <config_path>
  dqtoolss run-profile --schema <schema> --table <table> --conn <config_path>

Examples:
  dqtoolx run-check --table public.users --check null_check uniqueness_check --conn dq_config.yml
  dqtoolx run-profile --schema public --table employees --conn dq_config.yml
""")


if __name__ == "__main__":
    main()
