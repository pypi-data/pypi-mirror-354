# system-prompt-composer

**Native Node.js bindings** for intelligent system prompt generation for AI assistants with MCP tool integration. No Python dependencies required!

## Installation

```bash
npm install system-prompt-composer
```

🎉 **That's it!** No Python installation needed - this package uses native Rust bindings via NAPI-RS.

## Quick Start

```javascript
const { composeSystemPrompt } = require('system-prompt-composer');

const request = {
  user_prompt: "Help me analyze this code file",
  mcp_config: {
    mcpServers: {
      "desktop-commander": {
        name: "desktop-commander",
        command: "npx",
        args: ["@modelcontextprotocol/server-filesystem"]
      }
    }
  },
  session_state: {
    tool_call_count: 0
  }
};

const response = await composeSystemPrompt(request);
console.log(response.system_prompt);
```

## Features

- 🧠 **Intelligent prompts** that adapt to available MCP tools
- 📋 **Automatic task planning** for complex requests
- 🎯 **Context-aware guidance** for different domains (programming, analysis, filesystem, system)
- 📊 **Progress monitoring** for multi-step workflows
- ⚡ **Native performance** - direct Rust execution via NAPI-RS
- 🚫 **No Python dependency** - fully self-contained
- 📦 **TypeScript support** with full type definitions
- 🌍 **Cross-platform** - works on Linux, macOS, Windows

## API Reference

### Core Functions

```javascript
const { 
  composeSystemPrompt,
  listAvailableDomains,
  listAvailableBehaviors,
  getStatus,
  isAvailable 
} = require('system-prompt-composer');
```

#### `composeSystemPrompt(request)`
Generate an intelligent system prompt based on available tools and context.

```javascript
const request = {
  user_prompt: "Your user's request",
  mcp_config: {
    mcpServers: {
      "server-name": {
        name: "server-name", 
        command: "command",
        args: ["arg1", "arg2"]
      }
    }
  },
  session_state: {
    tool_call_count: 0,
    has_plan: false,
    task_complexity: "Auto" // "Auto" | "Simple" | "Complex"
  },
  domain_hints: ["programming", "analysis"], // Optional
  task_complexity: "Complex" // Optional override
};

const response = await composeSystemPrompt(request);
```

**Response Format:**
```javascript
{
  system_prompt: "Generated system prompt...",
  source: "native",
  version: "1.1.0",
  available_domains: ["programming", "analysis", "filesystem", "system"],
  available_behaviors: ["planning", "progress", "reasoning", "tools"]
}
```

#### `listAvailableDomains()`
Returns array of available domain modules.

```javascript
const domains = await listAvailableDomains();
// ["analysis", "filesystem", "programming", "system"]
```

#### `listAvailableBehaviors()`
Returns array of available behavior modules.

```javascript
const behaviors = await listAvailableBehaviors();
// ["planning", "progress", "reasoning", "tools"]
```

#### `getStatus()`
Returns system status and configuration.

```javascript
const status = await getStatus();
// {
//   available: true,
//   source: "native", 
//   version: "1.1.0",
//   domains: [...],
//   behaviors: [...]
// }
```

#### `isAvailable()`
Always returns `true` for native bindings.

```javascript
const available = await isAvailable(); // true
```

## Integration Examples

### Express.js API

```javascript
const express = require('express');
const { composeSystemPrompt } = require('system-prompt-composer');

app.post('/api/compose-prompt', async (req, res) => {
  try {
    const response = await composeSystemPrompt(req.body);
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Electron Main Process

```javascript
const { ipcMain } = require('electron');
const { composeSystemPrompt } = require('system-prompt-composer');

ipcMain.handle('prompt-composer:generate', async (event, request) => {
  try {
    return await composeSystemPrompt(request);
  } catch (error) {
    return { error: error.message, system_prompt: '' };
  }
});
```

### Next.js API Route

```javascript
// pages/api/compose.js
import { composeSystemPrompt } from 'system-prompt-composer';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const response = await composeSystemPrompt(req.body);
      res.status(200).json(response);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}
```

## Domain and Behavior Modules

The prompt composer uses modular prompt components:

### Available Domains
- **`analysis`** - Data analysis and interpretation guidance
- **`filesystem`** - File and directory operation guidance  
- **`programming`** - Code analysis and development guidance
- **`system`** - System administration and configuration guidance

### Available Behaviors
- **`planning`** - Multi-step task planning and organization
- **`progress`** - Progress tracking and status updates
- **`reasoning`** - Analytical thinking and problem-solving
- **`tools`** - Effective tool usage and integration

## Error Handling

```javascript
try {
  const response = await composeSystemPrompt(request);
  console.log(`Generated ${response.system_prompt.length} character prompt`);
} catch (error) {
  console.error('Prompt generation failed:', error.message);
  // Fallback to basic prompt
  const fallbackPrompt = "You are a helpful AI assistant.";
}
```

## Requirements

- **Node.js**: 14.0.0 or higher
- **No other dependencies** - native bindings included

## Architecture

This package uses **native Rust bindings** via NAPI-RS:

```
Node.js → NAPI-RS → Rust Core → Prompt Generation
```

**Benefits over subprocess approach:**
- ✅ No Python dependency
- ✅ Native performance
- ✅ Simple installation (`npm install`)
- ✅ Better error handling
- ✅ Smaller bundle size
- ✅ Cross-platform binary distribution

## Development

```bash
# Install dependencies
npm install

# Build native bindings
npm run build         # Release build
npm run build:debug   # Debug build

# Run tests
npm test

# Package for distribution
npm pack
```

## Building from Source

```bash
# Prerequisites: Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone and build
git clone <repository>
cd prompt-composer/node
npm install
npm run build
```

## License

MIT License - see LICENSE file for details.

## Related Projects

- [MCP SDK](https://github.com/modelcontextprotocol/sdk) - Model Context Protocol
- [NAPI-RS](https://napi.rs/) - Native bindings framework

## Support

For issues, feature requests, or questions:
- GitHub Issues: [Create an issue](https://github.com/xcud/prompt-composer/issues)
- Documentation: See main [README](../README.md)
