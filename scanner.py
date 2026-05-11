def scan(args, port_range):
    print(f"target: {args.target}")
    print(f"port: {args.start_port} - {args.end_port}")
    print(f"total port: {len(port_range)}")
