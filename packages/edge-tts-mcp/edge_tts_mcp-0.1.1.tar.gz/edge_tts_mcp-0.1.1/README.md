# edge-tts-mcp

This is a Text-to-Speech (TTS) service based on Model Context Protocol (MCP), using Microsoft Edge TTS engine.

## Features

This service provides two main tools:

1. `list_voice`: Get available voice list, equivalent to `edge-tts --list-voices` command functionality
2. `tts`: Convert text to speech and return generated audio file and subtitle file paths

## Requirements

- Python >= 3.11
- Internet connection (for accessing Microsoft Edge TTS service)

**Note: TTS service uses Microsoft TTS engine, poor network connectivity will affect service calls.**

## Installation

**Runtime environment requires [Python](https://python.org) and [UV](https://docs.astral.sh/uv/getting-started/installation/) to be installed first**

Add the following content to the MCP configuration:


```json
{
    "mcpServers": {
        "edge-tts-mcp": {
            "command": "uvx",
            "args": [
                "edge_tts_mcp"
            ]
        }
    }
}
```
