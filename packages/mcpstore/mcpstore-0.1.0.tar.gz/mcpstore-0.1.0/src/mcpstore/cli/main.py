import sys
import argparse
import uvicorn

def main():
    parser = argparse.ArgumentParser(description="mcpstore command line interface")
    subparsers = parser.add_subparsers(dest="command")

    # api 子命令
    api_parser = subparsers.add_parser("api", help="Start the mcpstore FastAPI server")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    api_parser.add_argument("--port", type=int, default=18200, help="Port to bind")
    api_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    if args.command == "api":
        uvicorn.run("mcpstore.scripts.app:app", host=args.host, port=args.port, reload=args.reload)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
