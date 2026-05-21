# port-scanner

A concurrent TCP port scanner CLI written in Python using `ThreadPoolExecutor` and raw `socket` connections.

[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/akshxdevs/port-scanner)
[![Python Version](https://img.shields.io/badge/python-3.13-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![stdlib only](https://img.shields.io/badge/deps-stdlib%20only-lightgrey)](https://github.com/akshxdevs/port-scanner)

## Overview

- Scans a configurable range of TCP ports against any target host or IP
- Dispatches probes concurrently via `ThreadPoolExecutor` with a tunable thread count
- Classifies each port as `open`, `closed`, or `timeout` using `socket.connect_ex`
- Protects the shared results map with a `threading.Lock` to prevent data races
- Writes reports to disk in JSON or CSV format via a dedicated output module
- Validates port range bounds (0–65535) and argument ordering at startup

## Key Features

- `ThreadPoolExecutor(max_workers=args.threads)` dispatches one worker per port; default 100 threads
- `socket.connect_ex((target, port))` returns 0 on success, non-zero on refusal — no exception for closed ports
- `socket.settimeout(10.0)` enforced per connection; `socket.timeout` caught separately from `socket.error` to distinguish timeout from refusal
- `threading.Lock` wraps every write into the `results` dict to ensure thread-safe accumulation
- JSON report embeds `target` and a port-sorted list of `{port, status}` objects; CSV writes flat rows sorted by port number
- `argparse` validates that `start-port < end-port` and both are within 0–65535 before any scanning begins

## Tech Stack

- Python 3.13
- `socket` — TCP connection probing via `AF_INET / SOCK_STREAM`
- `concurrent.futures.ThreadPoolExecutor` — thread pool management
- `threading.Lock` — result map synchronization
- `argparse` — CLI argument parsing and validation
- `json`, `csv` — report serialization (stdlib only, no third-party dependencies)

## Installation

### Prerequisites

- Python 3.10 or later
- No external packages required — uses Python standard library only

### Run locally

```bash
git clone https://github.com/akshxdevs/port-scanner.git
cd port-scanner
python main.py --target <host> --start-port 1 --end-port 1024
```

### Scan with custom thread count and save output

```bash
python main.py --target scanme.nmap.org --start-port 1 --end-port 1024 --threads 200 --output /tmp/report.json --format json
```

## Configuration

All configuration is passed via CLI flags. There are no environment variables.

```
--target           Target hostname or IP address (required)
--start-port, -sp  First port in the scan range (default: 1, min: 0)
--end-port,   -np  Last port in the scan range (default: 1024, max: 65535)
--threads,    -th  Number of concurrent threads (default: 100)
--output,     -o   Filepath to write the report (optional; omit to skip saving)
--format,     -f   Output format: json or csv (default: json)
```

**Notes**

- `--target` is the only required argument; all others have defaults
- `--output` must be a writable path including filename (e.g. `/home/user/scan.json`)
- If `--output` is omitted, results are printed to stdout only and no file is written
- The scanner exits with an argparse error if `start-port > end-port` or either is out of range

## Usage Examples

Scan the default range (ports 1–1024) with default settings:

```bash
python main.py --target 192.168.1.1
```

Scan a wider range with more threads:

```bash
python main.py --target scanme.nmap.org -sp 1 -np 9999 -th 500
```

Save results as JSON:

```bash
python main.py --target 10.0.0.1 -sp 20 -np 1024 -o /tmp/result.json -f json
```

Save results as CSV:

```bash
python main.py --target 10.0.0.1 -sp 1 -np 65535 -th 1000 -o /tmp/result.csv -f csv
```

## Core Modules

### `main.py`

- `get_args()` — builds the `argparse` parser, validates port bounds and ordering, constructs the `port_range` list, and returns `(args, port_range)`
- Entry point calls `scan(args, port_range)` and conditionally calls `save_report` if `--output` was provided

### `scanner.py`

- `scan(args, port_range)` — initialises the shared `results` dict and a `Lock`, then submits all ports to a `ThreadPoolExecutor`; returns the completed results map
- `worker(port)` — inner closure called per thread; invokes `scan_port`, writes the result under lock, then prints the port status outside the lock to minimise contention
- `scan_port(target, port)` — opens a fresh `AF_INET / SOCK_STREAM` socket per probe, applies the module-level `timeout = 10.0`, calls `connect_ex`, and returns `"open"`, `"closed"`, or `"timeout"`

### `output.py`

- `save_report(results, target, filepath, format)` — dispatches to `save_json` or `save_csv` based on the format argument
- `save_json(results, target, filepath)` — wraps results in a `{"target": ..., "results": [...]}` envelope, sorts ports with `sorted(results.items())`, and writes indented JSON
- `save_csv(results, filepath)` — writes a `port,status` header row then one row per port in ascending order

## Project Structure

```text
port-scanner/
├── main.py          # CLI entry point and argument parsing
├── scanner.py       # TCP probing logic and thread pool orchestration
├── output.py        # JSON and CSV report serialization
├── utils.py         # (reserved)
├── requirement.txt  # No external dependencies
├── .gitignore       # Excludes __pycache__ and compiled bytecode
└── LICENSE          # MIT License
```

## Current Limitations

- No service/banner detection — only reports open/closed/timeout, not the service running on each port
- No UDP scanning — `SOCK_STREAM` only; UDP ports are invisible to this scanner
- No CIDR or hostname-range support — one target host per run
- No retry logic — a `socket.error` on a port is immediately classified as `closed` without re-attempt
- Timeout is a module-level constant (`10.0` seconds) with no CLI flag to override it
- CSV output omits the target hostname; JSON format is the only report type that preserves it

## License

Licensed under the [MIT License](LICENSE).
