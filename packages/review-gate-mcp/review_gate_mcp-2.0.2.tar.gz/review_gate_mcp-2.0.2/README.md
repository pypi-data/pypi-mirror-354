# Review Gate MCP Server 🚀

A modern Model Context Protocol (MCP) server for AI-powered code review and interaction tools.

## ✨ Features

- **🔄 Interactive Review Chat**: Get real-time feedback from users through popup dialogs
- **⚡ Quick Input**: Fast user input collection with customizable timeouts
- **🎤 Speech-to-Text**: Convert audio to text using Whisper (disabled by default, requires configuration)
- **🎯 MCP Client Integration**: Seamless integration with any MCP-compatible client

## 🚀 Installation

```bash
uvx review-gate-mcp
```

## 🔧 Configuration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "review-gate": {
      "command": "uvx",
      "args": ["review-gate-mcp"]
    }
  }
}
```

## 🛠️ Available Tools

- **`review_gate_chat`**: Interactive chat popup for user feedback and code reviews
- **`quick_input`**: Quick user input with shorter timeout for fast interactions
- **`speech_to_text`**: Convert audio files to text using Whisper (optional)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Original Review Gate concept by Lakshman Turlapati. Built with [Model Context Protocol](https://modelcontextprotocol.io/).
