# Peliqan MCP Server

For more info, visit https://peliqan.io/mcp.

## Configuration

Set up the connection to your Peliqan acount.

Create a configuration file named peliqan_config.json in your home folder:

```
{
    "account_id": 1234,
    "api_token": "xxx"
}
```

Or add the environment variables:
- account_id
- api_token

## Installation

```
pip install mcp-server-peliqan
```

## Usage with Claude Desktop

Add this to your claude_desktop_config.json:

```
{
  "mcpServers": {
    "peliqan": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server_peliqan"
      ],
      "env": {
        "peliqan_account_id": "1234",
        "peliqan_api_token": "xxx"
      }
    }
  }
}
```

Location on Windows: `$env:AppData\Claude\claude_desktop_config.json`
Location on Mac: `~/Library/Application\ Support/Claude/claude_desktop_config.json`