#!/usr/bin/env node

/**
 * Post-build script to apply our marshaling layer
 * This runs after napi-rs generates the raw bindings
 */

const fs = require('fs');
const path = require('path');

console.log('🔧 Applying post-build fixes...');

// Read the auto-generated index.js
let content = fs.readFileSync('index.js', 'utf8');

// Find the exports section and replace it with our marshaling layer
const exportsStart = content.indexOf('const { composeSystemPrompt,');
const exportsEnd = content.indexOf('module.exports.getStatus = getStatus') + 'module.exports.getStatus = getStatus'.length;

if (exportsStart === -1 || exportsEnd === -1) {
  console.error('❌ Could not find exports section to replace');
  process.exit(1);
}

const marshalingLayer = `const { 
  composeSystemPromptWithPromptsDir,
  isAvailable, 
  getStatus: nativeGetStatus 
} = nativeBinding

// Minimal convenience functions for data marshaling only
function composeSystemPrompt(request) {
  const requestJson = typeof request === 'string' ? request : JSON.stringify(request);
  const promptsDir = join(__dirname, 'prompts');
  const responseJson = composeSystemPromptWithPromptsDir(requestJson, promptsDir);
  return JSON.parse(responseJson);
}

function getStatus() {
  const statusJson = nativeGetStatus();
  return JSON.parse(statusJson);
}

// Export the minimal API
module.exports = {
  composeSystemPrompt,
  isAvailable,
  getStatus
}`;

// Add path require at the top if not present
if (!content.includes("const { join } = require('path')")) {
  content = content.replace(
    "const { existsSync, readFileSync } = require('fs')",
    "const { existsSync, readFileSync } = require('fs')\nconst { join } = require('path')"
  );
}

// Replace the exports section
const beforeExports = content.substring(0, exportsStart);
const afterExports = content.substring(exportsEnd);
content = beforeExports + marshalingLayer + afterExports;

// Write back the modified content
fs.writeFileSync('index.js', content);

// Update TypeScript definitions
const tsDefinitions = `/* tslint:disable */
/* eslint-disable */

/** 
 * System prompt composer - intelligent system prompt generation for AI assistants
 * Direct native bindings with minimal JavaScript wrapper layer
 */

/** Request object for prompt composition */
export interface PromptRequest {
  user_prompt: string;
  mcp_config: {
    mcpServers: { [key: string]: McpServer };
  };
  session_state?: SessionState;
  domain_hints?: string[];
  behavior_hints?: string[];
  task_complexity?: 'Simple' | 'Complex';
}

/** MCP server configuration */
export interface McpServer {
  name: string;
  command: string;
  args: string[];
  env?: { [key: string]: string };
}

/** Session state for context-aware prompts */
export interface SessionState {
  tool_call_count?: number;
  original_task?: string;
  has_plan?: boolean;
  last_action?: string;
  current_step?: string;
}

/** Response from prompt composition */
export interface PromptResponse {
  system_prompt: string;
  applied_modules: string[];
  recognized_tools: string[];
  complexity_assessment: 'Simple' | 'Complex';
}

/** Status information */
export interface StatusResponse {
  available: boolean;
  behaviors: string[];
  domains: string[];
  source: string;
  version: string;
}

/** 
 * Compose a system prompt based on request object or JSON string
 * Accepts either a PromptRequest object or JSON string representation
 */
export declare function composeSystemPrompt(request: PromptRequest | string): PromptResponse;

/** List available domain modules */
export declare function listAvailableDomains(): string[];

/** List available behavior modules */
export declare function listAvailableBehaviors(): string[];

/** Check if the native bindings are available (always returns true) */
export declare function isAvailable(): boolean;

/** Get status information including available domains and behaviors */
export declare function getStatus(): StatusResponse;
`;

fs.writeFileSync('index.d.ts', tsDefinitions);

console.log('✅ Post-build fixes applied successfully!');
console.log('   - Added marshaling layer to index.js');
console.log('   - Updated TypeScript definitions');
console.log('   - Ready for publishing!');
