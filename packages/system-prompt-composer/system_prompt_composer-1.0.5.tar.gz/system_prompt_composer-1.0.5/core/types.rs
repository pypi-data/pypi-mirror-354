use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use thiserror::Error;

/// Configuration for an MCP server
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct McpServer {
    pub name: String,
    pub command: String,
    pub args: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub env: Option<HashMap<String, String>>,
}

/// Complete MCP configuration with all servers
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct McpConfig {
    #[serde(rename = "mcpServers")]
    pub mcp_servers: HashMap<String, McpServer>,
}

/// Information about an available tool from an MCP server
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Tool {
    pub name: String,
    pub description: String,
    pub server: String,
    pub schema: Option<serde_json::Value>,
}

/// Current session state for context-aware prompt generation
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct SessionState {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub tool_call_count: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub original_task: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub has_plan: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_action: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub current_step: Option<String>,
}

/// Task complexity assessment
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TaskComplexity {
    Auto,
    Simple,
    Complex,
}

impl Default for TaskComplexity {
    fn default() -> Self {
        TaskComplexity::Auto
    }
}

/// Request for prompt composition
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PromptRequest {
    pub user_prompt: String,
    pub mcp_config: McpConfig,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub session_state: Option<SessionState>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub domain_hints: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub behavior_hints: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub task_complexity: Option<TaskComplexity>,
}

/// Response containing the composed system prompt and metadata
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PromptResponse {
    pub system_prompt: String,
    pub applied_modules: Vec<String>,
    pub recognized_tools: Vec<String>,
    pub complexity_assessment: TaskComplexity,
}

/// Error types for prompt composition
#[derive(Debug, Error)]
pub enum PromptError {
    #[error("MCP server connection failed: {0}")]
    McpConnectionFailed(String),
    #[error("Tool discovery failed: {0}")]
    ToolDiscoveryFailed(String),
    #[error("Module loading failed: {0}")]
    ModuleLoadingFailed(String),
    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),
    #[error("HTTP request failed: {0}")]
    HttpError(#[from] reqwest::Error),
    #[error("Invalid configuration: {0}")]
    ConfigError(String),
}

/// Categories of tools for prompt module selection
#[derive(Debug, Clone, PartialEq)]
pub enum ToolCategory {
    FileSystem,
    WebApi,
    DataAnalysis,
    SystemAdmin,
    Custom,
}

impl ToolCategory {
    /// Categorize a tool based on its name and description
    pub fn from_tool(tool: &Tool) -> Self {
        let name_lower = tool.name.to_lowercase();
        let desc_lower = tool.description.to_lowercase();
        
        if name_lower.contains("file") || name_lower.contains("directory") || name_lower.contains("read") || name_lower.contains("write") {
            ToolCategory::FileSystem
        } else if desc_lower.contains("http") || desc_lower.contains("api") || desc_lower.contains("web") {
            ToolCategory::WebApi
        } else if desc_lower.contains("data") || desc_lower.contains("csv") || desc_lower.contains("analysis") {
            ToolCategory::DataAnalysis
        } else if desc_lower.contains("system") || desc_lower.contains("process") || desc_lower.contains("command") {
            ToolCategory::SystemAdmin
        } else {
            ToolCategory::Custom
        }
    }
}
