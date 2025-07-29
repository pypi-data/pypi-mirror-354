# Hong Kong Finance Data MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-finance-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an MCP server that provides access to finance related data in Hong Kong through a FastMCP interface.

## Features

1. Monthly statistics on the number of new and active business registrations in Hong Kong
2. Quarterly statistics on residential mortgage loans in negative equity in Hong Kong
3. Credit card lending survey results in Hong Kong

## Examples

* What is the number of new business registered in Hong Kong 2024?
* What is the negative loan situation in Hong Kong Q1 2025 compare with Q1 2024?
* Write a commentary about the latest residential mortgage loans in negative equity in Hong Kong
* How is current Hong Kong economy by referencing credit lending data and residential mortgage loans in negative equity?

Assume chart tool is available:

* Plot a line chart showing trend and number of new business registered each month from Jan to Dec in Hong Kong 2024.
![](https://raw.githubusercontent.com/hkopenai/hk-finance-mcp-server/refs/heads/main/assets/line_chart.png)

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```

### Running Options

- Default stdio mode: `python app.py`
- SSE mode (port 8000): `python app.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hk-finance": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "uvx",
    "args": [
      "hk_finance_mcp_server"
    ]
  }
}
```

## Testing

Tests are available in the `tests/` directory. Run with:
```bash
pytest
```

