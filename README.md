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

### Prerequisites
- Python 3.9+
- Free Amsterdam Data API key ([get yours here](https://api.data.amsterdam.nl))

### 1️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/TCLUBNL/amsterdam-municipal-mcp-server.git
cd amsterdam-municipal-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure API Key

Create a `.env` file in the project root:

```bash
AMSTERDAM_API_KEY=your_api_key_here
```

> 💡 **Get your free API key:** Visit [api.data.amsterdam.nl](https://api.data.amsterdam.nl) and sign up.

### 3️⃣ Test the Server

```bash
python3 -c "from server.tools.get_gebieden import get_gebieden; r = get_gebieden('buurt'); print(f'✅ Found {r[\"count\"]} neighborhoods!')"
```

Expected output: `✅ Found 99 neighborhoods!`

---

## 🔌 Claude Desktop Integration

### Step 1: Find Your Config File

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### Step 2: Add Server Configuration

Replace `/absolute/path/to/` with your actual paths:

```json
{
  "mcpServers": {
    "amsterdam-municipal": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/amsterdam-municipal-mcp-server/mcp_server_simple.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/amsterdam-municipal-mcp-server",
        "AMSTERDAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

> 💡 **Tip:** Use `pwd` in your terminal to get the absolute path.

### Step 3: Restart Claude Desktop

Quit Claude Desktop completely and reopen it. You should see the 🔌 icon indicating MCP servers are connected.

### Step 4: Test in Claude

Try these example queries:

- *"How many neighborhoods are in Amsterdam?"*
- *"Search for addresses on Damrak street"*
- *"How many Tesla vehicles are registered in Netherlands?"*
- *"Find waste containers near Central Station"*

---

## 📡 Available Tools

| Tool | Description | Example Use |
|------|-------------|-------------|
| `search_bag_address` | Search Amsterdam addresses & buildings | Find specific street addresses |
| `get_gebieden` | Get neighborhood boundaries with GeoJSON | Analyze city districts |
| `get_waste_containers` | Locate waste bins by type & location | Find nearest recycling points |
| `get_vehicle_data` | Dutch vehicle registry (RDW) | Query vehicle registrations nationwide |

---

## ⚠️ Known Limitations

- **Waste Containers:** Most containers in the API lack coordinate data, limiting location-based searches
- **Rate Limits:** Amsterdam API has standard rate limits; queries are cached where possible
- **Coverage:** Vehicle data covers all of Netherlands; other tools are Amsterdam-specific

---

## 🔗 Related MCP Servers

- **[CBS Statistics MCP](https://github.com/TCLUBNL/cbs-statistics-mcp-server)** - Dutch national statistics
- **[Geospatial & Cadastral MCP](https://github.com/TCLUBNL/geospatial-cadastral-mcp-server)** - Netherlands geospatial data

---

## 📝 License

MIT License • Amsterdam data available under [Amsterdam Open Data License](https://data.amsterdam.nl)

---

## 🤝 Contributing

Issues and pull requests are welcome! Feel free to contribute improvements or report bugs.

---

**Built with ❤️ by [TCLUB NL](https://github.com/TCLUBNL)**

⭐ **Star this repo** if you find it useful!