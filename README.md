# 🏛️ Amsterdam Municipal Data MCP Server

**Production-ready MCP server with 9 working Amsterdam municipal APIs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)

Access comprehensive Amsterdam city data including buildings, neighborhoods, cadastral parcels, energy consumption, sustainability initiatives, public reports, waste management, infrastructure, and Dutch vehicle registration through Claude Desktop.

---

## ✅ Working APIs (9 Tools)

### 🏘️ Property & Location
| API | Tool | Data Available | Example Query |
|-----|------|----------------|---------------|
| **BAG** | `search_bag_address` | Addresses, postcodes, building IDs | "Find addresses on Damrak" |
| **BRK2** | `get_brk2_parcel` | Cadastral parcels, ownership, mortgages | "Who owns this property?" |
| **Gebieden** | `get_gebieden` | 99 neighborhoods with GeoJSON boundaries | "Show all neighborhoods in Centrum" |

### 🌱 Energy & Sustainability
| API | Tool | Data Available | Example Query |
|-----|------|----------------|---------------|
| **Gas Consumption** | `get_gas_consumption` | Energy usage per postal code (Liander data) | "Gas consumption in 1012AB" |
| **Gas-Free Zones** | `get_gas_free_neighborhoods` | Sustainable neighborhood initiatives | "Show gas-free neighborhoods" |

### 🏗️ Infrastructure & Urban Management
| API | Tool | Data Available | Example Query |
|-----|------|----------------|---------------|
| **Infrastructure** | `get_infrastructure` | Pavements, green spaces, terrain objects | "Show green spaces in West" |
| **Waste** | `get_waste_containers` | Container locations (glass, paper, plastic) | "Find containers near Dam Square" |
| **Public Reports** | `get_public_reports` | Citizen incident reports (SIA) | "Show recent complaints in Centrum" |

### 🚗 Vehicle Registry
| API | Tool | Data Available | Example Query |
|-----|------|----------------|---------------|
| **RDW** | `get_vehicle_data` | Dutch vehicle registration (nationwide) | "Find all Tesla vehicles" |

---

## 🎯 Powerful Cross-API Queries

### Property Due Diligence
> *"For address Nieuwezijds Voorburgwal 147: show building details, cadastral ownership, gas consumption, nearby waste facilities, and recent public reports"*

**Uses:** BAG + BRK2 + Gas Consumption + Waste + Public Reports

### Sustainable Development Analysis
> *"Find all gas-free neighborhoods with high waste recycling rates and low public space complaints"*

**Uses:** Gas-Free Zones + Waste Containers + Public Reports + Neighborhoods

### Neighborhood Quality Index
> *"Compare neighborhoods by infrastructure maintenance, gas consumption, and citizen satisfaction"*

**Uses:** Infrastructure + Gas Consumption + Public Reports + Neighborhoods

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Free Amsterdam Data API key ([get yours here](https://api.data.amsterdam.nl))

### 1️⃣ Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/TCLUBNL/amsterdam-municipal-mcp-server.git
cd amsterdam-municipal-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 2️⃣ Configure API Key

Create a \`.env\` file in the project root:

\`\`\`bash
AMSTERDAM_API_KEY=your_api_key_here
\`\`\`

> 💡 **Get your free API key:** Visit [api.data.amsterdam.nl](https://api.data.amsterdam.nl) and sign up.

### 3️⃣ Test the Server

\`\`\`bash
python3 -c "from server.tools.get_gebieden import get_gebieden; r = get_gebieden('buurt'); print(f'✅ Found {r[\"count\"]} neighborhoods!')"
\`\`\`

Expected output: \`✅ Found 99 neighborhoods!\`

---

## 🔌 Claude Desktop Integration

### Step 1: Find Your Config File

**macOS:**
\`\`\`bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
\`\`\`

**Windows:**
\`\`\`bash
notepad %APPDATA%\Claude\claude_desktop_config.json
\`\`\`

### Step 2: Add Server Configuration

Replace \`/absolute/path/to/\` with your actual paths:

\`\`\`json
{
  "mcpServers": {
    "amsterdam-municipal": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/amsterdam-municipal-mcp-server/server/main.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/amsterdam-municipal-mcp-server",
        "AMSTERDAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
\`\`\`

> 💡 **Tip:** Use \`pwd\` in your terminal to get the absolute path.

### Step 3: Restart Claude Desktop

Quit Claude Desktop completely and reopen it. You should see the 🔌 icon indicating MCP servers are connected.

### Step 4: Test in Claude

Try these example queries:

- *"How many neighborhoods are in Amsterdam?"*
- *"Search for addresses on Damrak street"*
- *"Show cadastral ownership for postal code 1012AB"*
- *"Find gas-free neighborhoods in Amsterdam"*
- *"What's the gas consumption in area 1012?"*
- *"Show recent public reports in Centrum district"*
- *"Find green spaces in West district"*
- *"How many Tesla vehicles are registered in Netherlands?"*
- *"Find waste containers near Central Station"*

---

## 📡 Available Tools

### 1. search_bag_address
Search buildings and addresses in Amsterdam (BAG registry).

\`\`\`python
# Example: Find addresses on a street
search_bag_address(query="Damrak", limit=10)
\`\`\`

### 2. get_brk2_parcel
Get cadastral parcel information including ownership data.

\`\`\`python
# Example: Search by postal code
get_brk2_parcel(postcode="1012AB", huisnummer=1)
\`\`\`

### 3. get_gebieden
Get Amsterdam neighborhoods and districts with GeoJSON boundaries.

\`\`\`python
# Example: Get all neighborhoods
get_gebieden(gebied_type="buurten", limit=99)
\`\`\`

### 4. get_gas_consumption
Get gas consumption statistics per postal code area.

\`\`\`python
# Example: Energy usage in specific area
get_gas_consumption(postcode="1012", year=2023)
\`\`\`

### 5. get_gas_free_neighborhoods
Find gas-free neighborhood initiatives and planned sustainable zones.

\`\`\`python
# Example: Show realized sustainable neighborhoods
get_gas_free_neighborhoods(status="gerealiseerd")
\`\`\`

### 6. get_infrastructure
Get public space infrastructure objects (pavements, green spaces, terrain).

\`\`\`python
# Example: Find green spaces in district
get_infrastructure(object_type="groenobjecten", stadsdeel="Centrum")
\`\`\`

### 7. get_waste_containers
Find waste container locations by type and area.

\`\`\`python
# Example: Find glass containers nearby
get_waste_containers(fractie_omschrijving="Glas", limit=20)
\`\`\`

### 8. get_public_reports
Get citizen incident reports from SIA (Signalen Informatievoorziening Amsterdam).

\`\`\`python
# Example: Recent waste complaints
get_public_reports(category="afval", status="open", limit=50)
\`\`\`

### 9. get_vehicle_data
Query Dutch vehicle registration database (RDW - nationwide coverage).

\`\`\`python
# Example: Find specific vehicle brand
get_vehicle_data(merk="TESLA", limit=100)
\`\`\`

---

## 🏗️ Project Structure

\`\`\`
amsterdam-municipal-mcp-server/
├── server/
│   ├── main.py                          # MCP server entry point
│   └── tools/
│       ├── search_bag_address.py        # BAG addresses & buildings
│       ├── get_brk2_parcel.py           # Cadastral parcels ⭐ NEW
│       ├── get_gebieden.py              # Neighborhoods & districts
│       ├── get_gas_consumption.py       # Energy consumption ⭐ NEW
│       ├── get_gas_free_neighborhoods.py # Sustainability ⭐ NEW
│       ├── get_infrastructure.py        # Urban infrastructure ⭐ NEW
│       ├── get_waste_containers.py      # Waste management
│       ├── get_public_reports.py        # Civic reports ⭐ NEW
│       └── get_vehicle_data.py          # RDW vehicle registry
├── requirements.txt
├── .env.example
└── README.md
\`\`\`

---

## 🔑 API Authentication

### Free Amsterdam Data API Key
1. Visit https://api.data.amsterdam.nl
2. Register for a free account
3. Generate API key
4. Add to \`.env\` file

**Note:** Some APIs work without authentication but may have rate limits.

---

## 📊 API Coverage

| Domain | APIs | Coverage |
|--------|------|----------|
| **Property & Location** | 3 | Buildings, parcels, neighborhoods |
| **Energy & Sustainability** | 2 | Consumption data, gas-free zones |
| **Infrastructure & Urban** | 3 | Public spaces, waste, civic reports |
| **Vehicle Registry** | 1 | Nationwide vehicle data |

**Total: 9 integrated APIs** 🎉

---

## ⚠️ Known Limitations

- **Waste Containers:** Most containers in the API lack coordinate data, limiting location-based searches
- **Rate Limits:** Amsterdam API has standard rate limits; queries are cached where possible
- **Coverage:** Vehicle data covers all of Netherlands; other tools are Amsterdam-specific
- **Public Reports API:** May require authentication for full access to detailed incident data

---

## 🛠️ Development

### Testing Individual Tools

\`\`\`bash
# Activate virtual environment
source venv/bin/activate

# Test a specific tool
python -c "from server.tools.get_gas_consumption import get_gas_consumption; print(get_gas_consumption(postcode='1012'))"
\`\`\`

### Adding New Tools

1. Create new file in \`server/tools/\`
2. Follow existing pattern (requests, error handling, type hints)
3. Update \`server/main.py\` to register the tool
4. Test with Claude Desktop

---

## 📚 Resources

### Official Documentation
- **Amsterdam Data Portal:** https://data.amsterdam.nl
- **API Documentation:** https://api.data.amsterdam.nl/v1/docs/
- **Data Catalog:** https://data.amsterdam.nl/datasets/
- **RDW Open Data:** https://opendata.rdw.nl

### API Endpoints
- **BAG:** \`https://api.data.amsterdam.nl/v1/bag/\`
- **BRK2:** \`https://api.data.amsterdam.nl/v1/brk2/\`
- **Gebieden:** \`https://api.data.amsterdam.nl/v1/gebieden/\`
- **Gas Consumption:** \`https://api.data.amsterdam.nl/v1/aardgasverbruik/\`
- **Gas-Free Zones:** \`https://api.data.amsterdam.nl/v1/aardgasvrijezones/\`
- **Infrastructure:** \`https://api.data.amsterdam.nl/v1/objectenopenbareruimte/\`
- **Waste:** \`https://api.data.amsterdam.nl/v1/huishoudelijkafval/\`
- **Public Reports:** \`https://api.data.amsterdam.nl/v1/meldingen/\`
- **RDW:** \`https://opendata.rdw.nl/resource/\`

---

## 🔗 Related MCP Servers

- **[CBS Statistics MCP](https://github.com/TCLUBNL/cbs-statistics-mcp-server)** - Dutch national statistics
- **[Geospatial & Cadastral MCP](https://github.com/TCLUBNL/geospatial-cadastral-mcp-server)** - Netherlands geospatial data

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (\`git checkout -b feature/new-api\`)
3. Test thoroughly
4. Submit pull request

Issues and pull requests are welcome! Feel free to contribute improvements or report bugs.

---

## 📝 License

MIT License • Amsterdam data available under [Amsterdam Open Data License](https://data.amsterdam.nl)

---

## 🙏 Acknowledgments

- **City of Amsterdam** - Open Data Portal
- **RDW (Dutch Vehicle Authority)** - Open vehicle registration data
- **Liander** - Energy consumption data
- **Model Context Protocol** - MCP framework

---

**Built with ❤️ by [TCLUB NL](https://github.com/TCLUBNL)**

⭐ **Star this repo** if you find it useful!

*Last updated: 2025-10-24*
