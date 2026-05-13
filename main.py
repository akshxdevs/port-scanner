import argparse

from output import save_report
from scanner import scan


def get_args():
    parser = argparse.ArgumentParser(description="The Port Scanner")
    parser.add_argument("--target", required=True)
    parser.add_argument(
        "--start-port",
        "-sp",
        type=int,
        default=1,
        help="starting range of port (default = 1)",
    )
    parser.add_argument(
        "--end-port",
        "-np",
        type=int,
        default=1024,
        help="ending range of port (default = 1)",
    )
    parser.add_argument(
        "--threads",
        "-th",
        type=int,
        default=100,
        help="number of threads: (default:100)",
    )
    parser.add_argument(
        "--output", "-o", help="filepath to save the report (eg:/home/xx/xx/xxx)"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv"],
        default="json",
        help="format type json or csv",
    )
    args = parser.parse_args()

    if args.start_port < 0 or args.end_port > 65535:
        parser.error("Port must be between 0 and 65535")

    if args.start_port > args.end_port:
        parser.error(
            f"start port {args.start_port} cannot be greater than end port {args.end_port}"
        )

    port_range = list(range(args.start_port, args.end_port + 1))

    print(f"Scanning Ports: {args.start_port} to {args.end_port}")
    print("Total ports: ", len(port_range))

    return args, port_range


if __name__ == "__main__":
    args, port_range = get_args()
    results = scan(args, port_range)

    if args.output:
        save_report(results, args.target, args.output, args.format)
