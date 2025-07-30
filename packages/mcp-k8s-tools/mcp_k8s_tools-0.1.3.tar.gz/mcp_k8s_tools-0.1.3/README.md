# mcp-k8s-tools

A parameterized MCP server for investigating Kubernetes clusters.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kitlabcode/mcp-k8s-tools.git
   cd mcp-k8s-tools
   ```
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. **Kubeconfig:** Ensure your kubeconfig file is present and accessible. By default, this is `~/.kube/config`. The server uses your local kubeconfig to connect to your Kubernetes cluster.

## Running the Server

Start the MCP server:
```bash
mcp-k8s-tools-server
```

## Configuring with Cursor (`.cursor/mcp.json`)

To use `mcp-k8s-tools` with Cursor, add the following entry to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "k8s": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["-m", "mcp_k8s_tools.server"],
      "description": "K8s MCP server using venv Python"
    }
  }
}
```

- Replace `/path/to/your/venv/bin/python` with the path to your Python interpreter (e.g., from your virtual environment).
- The `args` array should use `-m mcp_k8s_tools.server` to launch the server module.
- No extra environment variables are needed for Kubernetes access, as the server uses your local kubeconfig (default: `~/.kube/config`).

After updating `.cursor/mcp.json`, restart Cursor and enable the `k8s` server in the MCP panel.