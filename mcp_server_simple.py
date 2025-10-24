#!/usr/bin/env python3
"""Amsterdam Municipal Data MCP Server - 4 Working APIs"""
import json, sys, logging
from typing import Any, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)
logger = logging.getLogger("amsterdam-mcp")

from server.tools.search_bag_address import search_bag_address
from server.tools.get_gebieden import get_gebieden
from server.tools.get_waste_containers import get_waste_containers
from server.tools.get_vehicle_data import get_vehicle_data

def main():
    logger.info("Amsterdam Municipal MCP Server - 4 tools active")
    while True:
        line = sys.stdin.readline()
        if not line: break
        try:
            req = json.loads(line.strip())
            method = req.get("method")
            
            if method == "initialize":
                res = {"jsonrpc":"2.0","id":req.get("id"),"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"amsterdam-municipal","version":"1.0.0"}}}
            elif method == "tools/list":
                res = {"jsonrpc":"2.0","id":req.get("id"),"result":{"tools":[
                    {"name":"search_bag_address","description":"Search Amsterdam addresses","inputSchema":{"type":"object","properties":{"query":{"type":"string"},"limit":{"type":"integer"}},"required":["query"]}},
                    {"name":"get_gebieden","description":"Get Amsterdam neighborhoods (99 areas)","inputSchema":{"type":"object","properties":{"gebied_type":{"type":"string"},"naam":{"type":"string"}},"required":["gebied_type"]}},
                    {"name":"get_waste_containers","description":"Find waste containers","inputSchema":{"type":"object","properties":{"lat":{"type":"number"},"lon":{"type":"number"},"radius":{"type":"integer"},"container_type":{"type":"string"}}}},
                    {"name":"get_vehicle_data","description":"Dutch vehicle registration data","inputSchema":{"type":"object","properties":{"kenteken":{"type":"string"},"postcode":{"type":"string"},"merk":{"type":"string"}}}}
                ]}}
            elif method == "tools/call":
                tool = req["params"]["name"]
                args = req["params"].get("arguments",{})
                if tool == "search_bag_address": data = search_bag_address(args["query"], args.get("limit",20))
                elif tool == "get_gebieden": data = get_gebieden(args["gebied_type"], args.get("naam"))
                elif tool == "get_waste_containers": data = get_waste_containers(args.get("lat"), args.get("lon"), args.get("radius",500), args.get("container_type"))
                elif tool == "get_vehicle_data": data = get_vehicle_data(args.get("kenteken"), args.get("postcode"), args.get("merk"))
                else: raise ValueError(f"Unknown tool: {tool}")
                res = {"jsonrpc":"2.0","id":req.get("id"),"result":{"content":[{"type":"text","text":json.dumps(data,indent=2,ensure_ascii=False)}]}}
            else: res = None
            
            if res: print(json.dumps(res), flush=True)
        except Exception as e:
            logger.error(f"Error: {e}")
            print(json.dumps({"jsonrpc":"2.0","id":req.get("id",0),"error":{"code":-32603,"message":str(e)}}), flush=True)

if __name__ == "__main__": main()
