import argparse

from scanner import scan


def get_args():
    praser = argparse.ArgumentParser(description="The Port Scanner")
    praser.add_argument("--target", required=True)
    praser.add_argument(
        "--start-port",
        "-sp",
        type=int,
        default=1,
        help="starting range of port (default = 1)",
    )
    praser.add_argument(
        "--end-port",
        "-np",
        type=int,
        default=1024,
        help="ending range of port (default = 1)",
    )

    args = praser.parse_args()

    if args.start_port < 0 or args.end_port > 65535:
        praser.error("Port must me between 0 and 65535")

    if args.start_port > args.end_port:
        praser.error(
            f"start port {args.start_port} cannot be greater than end port {args.end_port}"
        )

    port_range = list(range(args.start_port, args.end_port + 1))

    print(f"Scanning Ports: {args.start_port} to {args.end_port}")
    print("Total ports: ", len(port_range))

    scan(args, port_range)

    return args, port_range


if __name__ == "__main__":
    args = get_args()
    print(args)
