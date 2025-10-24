# 🏛️ Amsterdam Municipal Data MCP Server

**Production-ready MCP server with 4 working Amsterdam municipal APIs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)

Access Amsterdam city data for buildings, neighborhoods, waste management, and Dutch vehicle registration through Claude Desktop.

---

## ✅ Working APIs (4 Tools)

| API | Endpoint | Data Available | Example Query |
|-----|----------|----------------|---------------|
| **BAG** | `/v1/bag/nummeraanduidingen/` | Addresses, postcodes, building IDs | "Find addresses in Amsterdam" |
| **Gebieden** | `/v1/gebieden/buurten/` | 99 neighborhoods with GeoJSON boundaries | "Show all neighborhoods" |
| **Waste** | `/v1/huishoudelijkafval/container/` | Waste container locations (glass, paper, plastic) | "Find containers near Dam Square" |
| **RDW** | `opendata.rdw.nl` | Dutch vehicle registration (entire Netherlands) | "Find all Tesla vehicles" |

---

## 🚀 Quick Start

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/TCLUBNL/amsterdam-municipal-mcp-server.git
cd amsterdam-municipal-mcp-server
\`\`\`

### 2. Get API Key
Visit [api.data.amsterdam.nl](https://api.data.amsterdam.nl) and request a free API key.

### 3. Configure
\`\`\`bash
cat > .env << 'EOF'
AMSTERDAM_API_KEY=your_api_key_here
EOF
\`\`\`

### 4. Install
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

### 5. Test
\`\`\`bash
python3 -c "from server.tools.get_gebieden import get_gebieden; r = get_gebieden('buurt'); print(f'Found {r[\"count\"]} neighborhoods')"
\`\`\`

---

## 🔌 Claude Desktop Setup

Edit config:
\`\`\`bash
nano ~/Library/Application\\ Support/Claude/claude_desktop_config.json
\`\`\`

Add:
\`\`\`json
{
  "mcpServers": {
    "amsterdam-municipal": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server_simple.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/amsterdam-municipal-mcp-server",
        "AMSTERDAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
\`\`\`

Restart Claude Desktop.

---

## 📡 Tools

1. **search_bag_address** - Amsterdam addresses and buildings
2. **get_gebieden** - 99 neighborhoods with GeoJSON polygons
3. **get_waste_containers** - Waste bin locations by coordinates
4. **get_vehicle_data** - Dutch vehicle registry (entire NL)

---

## 🔗 Related Servers

- [CBS Statistics MCP](https://github.com/TCLUBNL/cbs-statistics-mcp-server) - Dutch national statistics
- [Geospatial & Cadastral MCP](https://github.com/TCLUBNL/geospatial-cadastral-mcp-server) - Netherlands geospatial data

---

## 📝 License

MIT License. Amsterdam data under open data license.

**Built by TCLUB NL**
