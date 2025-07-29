import argparse
from .master import run_master
from .slave import run_slave

def main():
    parser = argparse.ArgumentParser(prog="saranglebah", description="Broadcast keystrokes to multiple PCs")
    subparsers = parser.add_subparsers(dest="role", required=True)

    # master
    p_master = subparsers.add_parser("boss", help="Run as master")
    p_master.add_argument("--hamba", nargs="+", required=True, help="IP addresses of slave machines")
    p_master.add_argument("--port", type=int, default=5050, help="UDP port to use (default 5050)")

    # slave
    p_slave = subparsers.add_parser("hamba", help="Run as slave")
    p_slave.add_argument("--port", type=int, default=5050, help="UDP port to listen on (default 5050)")

    args = parser.parse_args()

    if args.role == "boss":
        run_master(args.hamba, args.port)
    elif args.role == "hamba":
        run_slave(args.port)

if __name__ == "__main__":
    main()
