# How to Use

```bash
pip install .
# 使用 mcp 开发工具启动调试界面
❯ mcp dev mcp_bill_track/server.py
Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

## 本地调试的方式
```json
{
	"bill-track-mcp": {
		"command": "uv",
		"args": [
			"--directory",
			"~/code-repos/freshmeat-ai/mcp",
			"run",
			"main.py"
		],
		"env": {
			"ACCOUNTING_WORKING_DIR": "your_accounting_data_path"
		}
	}
}
```

## 打包发布到 pypi
```bash
uv build
uv publish --token xxxxx
```

## 配置信息

```bash
{
  "mcpServers": {
    "bill-track-mcp": {
      "command": "your_python_path/python",
      "args": [
        "your_mcp_bill_track_path/main.py"
      ],
      "env": {
        "ACCOUNTING_WORKING_DIR": "your_accounting_data_path"
      }
    }
  }
} 
```