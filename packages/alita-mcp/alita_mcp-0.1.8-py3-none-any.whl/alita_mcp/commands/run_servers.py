import asyncio
import sys

from ..config import load_config
from ..utils.menu import show_menu
from ..utils.sio import start_socket_connection, get_all_tools


def run_servers():
    config = load_config()
    print("\nMcp Servers from configuration:")
    print(", ".join(config["servers"].keys()))
    print("\nConnecting to the servers...")
    all_tools = asyncio.run(get_all_tools(config["servers"]))
    # tree = {}
    # for server in all_tools:
    #     tools = [tool["name"] for tool in server.get("tools", [])]
    #     tree[server["name"]] = tools

    # print result
    print("\nAvailable Mcp Servers and Tools to serve:")
    for server in all_tools:
        print(f"\n  {server['name']}")
        for tool in server["tools"]:
            print(f"    {tool['name']}")

    try:
        # show_menu(tree)
        print(f"\nStarting MCP client...")
        start_socket_connection(config)
        while True:
            user_input = input("").strip()
            
    except KeyboardInterrupt:
        print("\nExiting application...")
        sys.exit(0)