import socket
import threading
from concurrent.futures import ThreadPoolExecutor

timeout = 10.0


def scan(args, port_range):
    print(f"target: {args.target}")
    print(f"port: {args.start_port} - {args.end_port}")
    print(f"total port: {len(port_range)}")

    results = {}
    lock = threading.Lock()

    def worker(port):
        status = scan_port(args.target, port)
        with lock:
            results[port] = status
            if status == "open":
                print(f"[OPEN]  port {port}")
            elif status == "timeout":
                print(f"[TIMEOUT]  port {port}")
            else:
                print(f"[CLOSED] port {port}")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(worker, port_range)

    return results


def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            return "open"
        else:
            return "closed"
    except socket.timeout:
        return "timeout"
    except socket.error:
        return "closed"
