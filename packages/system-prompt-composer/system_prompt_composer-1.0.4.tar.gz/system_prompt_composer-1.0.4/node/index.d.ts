/* tslint:disable */
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
