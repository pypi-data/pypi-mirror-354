use crate::types::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::time::{SystemTime, Duration};

/// Configuration for server pattern matching
#[derive(Debug, Clone, Serialize, Deserialize)]
struct ServerPattern {
    command_patterns: Vec<String>,
    arg_patterns: Vec<String>,
    name_patterns: Vec<String>,
    tools: Vec<ToolTemplate>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ToolTemplate {
    name: String,
    description: String,
}

/// Complete server patterns configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
struct ServerPatternsConfig {
    filesystem_servers: Option<ServerPattern>,
    weather_servers: Option<ServerPattern>,
    desktop_servers: Option<ServerPattern>,
    dynamic_servers: Option<ServerPattern>,
    data_servers: Option<ServerPattern>,
    web_servers: Option<ServerPattern>,
}

/// Tool discovery service that dynamically categorizes tools based on external patterns
pub struct ToolDiscovery {
    tools_by_server: HashMap<String, Vec<Tool>>,
    last_refresh: HashMap<String, SystemTime>,
    cache_duration: Duration,
    server_patterns: Option<ServerPatternsConfig>,
    prompts_dir: Option<String>,
}

impl ToolDiscovery {
    pub fn new() -> Self {
        Self {
            tools_by_server: HashMap::new(),
            last_refresh: HashMap::new(),
            cache_duration: Duration::from_secs(300), // 5 minutes cache
            server_patterns: None,
            prompts_dir: None,
        }
    }

    /// Create a new ToolDiscovery with custom prompts directory
    pub fn with_prompts_dir(prompts_dir: String) -> Self {
        Self {
            tools_by_server: HashMap::new(),
            last_refresh: HashMap::new(),
            cache_duration: Duration::from_secs(300), // 5 minutes cache
            server_patterns: None,
            prompts_dir: Some(prompts_dir),
        }
    }

    /// Load server patterns from external configuration file
    fn load_server_patterns(&mut self) -> Result<&ServerPatternsConfig, PromptError> {
        if self.server_patterns.is_none() {
            let config_path = self.find_config_file()?;
            let config_content = fs::read_to_string(config_path)
                .map_err(|e| PromptError::ConfigError(format!("Failed to read server patterns config: {}", e)))?;
            
            let patterns: ServerPatternsConfig = toml::from_str(&config_content)
                .map_err(|e| PromptError::ConfigError(format!("Failed to parse server patterns config: {}", e)))?;
            
            self.server_patterns = Some(patterns);
        }
        
        Ok(self.server_patterns.as_ref().unwrap())
    }

    /// Find the server patterns configuration file
    fn find_config_file(&self) -> Result<String, PromptError> {
        // If prompts_dir is specified, look there first
        if let Some(ref prompts_dir) = self.prompts_dir {
            let config_path = Path::new(prompts_dir).join("server_patterns.toml");
            if config_path.exists() {
                return Ok(config_path.to_string_lossy().to_string());
            } else {
                return Err(PromptError::ConfigError(
                    format!("Server patterns configuration file not found at: {}", config_path.display())
                ));
            }
        }

        // Fallback to relative path discovery (for backward compatibility)
        let possible_paths = [
            "prompts/server_patterns.toml",
            "../prompts/server_patterns.toml",
            "./server_patterns.toml",
        ];

        for path in &possible_paths {
            if Path::new(path).exists() {
                return Ok(path.to_string());
            }
        }

        Err(PromptError::ConfigError(
            "Server patterns configuration file not found. Expected: prompts/server_patterns.toml".to_string()
        ))
    }

    /// Discover tools from all configured MCP servers
    pub async fn discover_tools(&mut self, mcp_config: &McpConfig) -> Result<Vec<Tool>, PromptError> {
        let mut all_tools = Vec::new();
        
        for (server_name, server_config) in &mcp_config.mcp_servers {
            if self.needs_refresh(server_name) {
                match self.infer_server_tools(server_name, server_config) {
                    Ok(tools) => {
                        self.tools_by_server.insert(server_name.clone(), tools.clone());
                        self.last_refresh.insert(server_name.clone(), SystemTime::now());
                        all_tools.extend(tools);
                    }
                    Err(e) => {
                        // Log error but continue with other servers
                        eprintln!("Failed to infer tools from server {}: {}", server_name, e);
                        // Use cached tools if available
                        if let Some(cached_tools) = self.tools_by_server.get(server_name) {
                            all_tools.extend(cached_tools.clone());
                        }
                    }
                }
            } else {
                // Use cached tools
                if let Some(cached_tools) = self.tools_by_server.get(server_name) {
                    all_tools.extend(cached_tools.clone());
                }
            }
        }
        
        Ok(all_tools)
    }

    /// Check if we need to refresh tools for a server
    fn needs_refresh(&self, server_name: &str) -> bool {
        match self.last_refresh.get(server_name) {
            Some(last_time) => {
                SystemTime::now().duration_since(*last_time)
                    .unwrap_or(Duration::from_secs(u64::MAX)) > self.cache_duration
            }
            None => true,
        }
    }

    /// Infer tools from server configuration using external patterns
    fn infer_server_tools(&mut self, server_name: &str, server_config: &McpServer) -> Result<Vec<Tool>, PromptError> {
        let patterns = self.load_server_patterns()?.clone();
        
        // Try to match against each pattern type
        let all_patterns = [
            ("filesystem", patterns.filesystem_servers.as_ref()),
            ("weather", patterns.weather_servers.as_ref()),
            ("desktop", patterns.desktop_servers.as_ref()),
            ("dynamic", patterns.dynamic_servers.as_ref()),
            ("data", patterns.data_servers.as_ref()),
            ("web", patterns.web_servers.as_ref()),
        ];

        for (_pattern_type, pattern_opt) in &all_patterns {
            if let Some(pattern) = pattern_opt {
                if Self::matches_pattern(server_name, server_config, pattern) {
                    return Ok(Self::create_tools_from_pattern(server_name, pattern));
                }
            }
        }

        // Fallback: create a generic tool
        Ok(vec![
            Tool {
                name: format!("{}.execute", server_name),
                description: format!("Execute {} functionality", server_config.command),
                server: server_name.to_string(),
                schema: None,
            },
        ])
    }

    /// Check if a server matches a given pattern
    fn matches_pattern(server_name: &str, server_config: &McpServer, pattern: &ServerPattern) -> bool {
        let server_name_lower = server_name.to_lowercase();
        let command_lower = server_config.command.to_lowercase();
        
        // Check name patterns
        for name_pattern in &pattern.name_patterns {
            if server_name_lower.contains(&name_pattern.to_lowercase()) {
                return true;
            }
        }
        
        // Check command patterns
        for command_pattern in &pattern.command_patterns {
            if command_lower.contains(&command_pattern.to_lowercase()) {
                return true;
            }
        }
        
        // Check argument patterns
        for arg_pattern in &pattern.arg_patterns {
            if server_config.args.iter().any(|arg| arg.to_lowercase().contains(&arg_pattern.to_lowercase())) {
                return true;
            }
        }
        
        false
    }

    /// Create tools from a matched pattern
    fn create_tools_from_pattern(server_name: &str, pattern: &ServerPattern) -> Vec<Tool> {
        pattern.tools.iter().map(|tool_template| {
            Tool {
                name: format!("{}.{}", server_name, tool_template.name),
                description: tool_template.description.clone(),
                server: server_name.to_string(),
                schema: None,
            }
        }).collect()
    }

    /// Force refresh tools for a specific server
    pub async fn refresh_server(&mut self, server_name: &str, mcp_config: &McpConfig) -> Result<Vec<Tool>, PromptError> {
        if let Some(server_config) = mcp_config.mcp_servers.get(server_name) {
            let tools = self.infer_server_tools(server_name, server_config)?;
            self.tools_by_server.insert(server_name.to_string(), tools.clone());
            self.last_refresh.insert(server_name.to_string(), SystemTime::now());
            Ok(tools)
        } else {
            Err(PromptError::ConfigError(format!("Server {} not found in configuration", server_name)))
        }
    }

    /// Get cached tools for all servers
    pub fn get_cached_tools(&self) -> Vec<Tool> {
        self.tools_by_server.values().flatten().cloned().collect()
    }

    /// Infer tools from MCP configuration without caching (for immediate use)
    pub fn infer_tools_from_config_immediate(&mut self, mcp_config: &McpConfig) -> Vec<Tool> {
        let mut tools = Vec::new();
        
        for (server_name, server_config) in &mcp_config.mcp_servers {
            match self.infer_server_tools(server_name, server_config) {
                Ok(server_tools) => tools.extend(server_tools),
                Err(_) => {
                    // Fallback to generic tool
                    tools.push(Tool {
                        name: format!("{}.execute", server_name),
                        description: format!("Execute {} functionality", server_config.command),
                        server: server_name.to_string(),
                        schema: None,
                    });
                }
            }
        }
        
        tools
    }
}

impl Default for ToolDiscovery {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pattern_matching() {
        let mut discovery = ToolDiscovery::new();
        
        // This would need the config file to exist for a real test
        // For now, just test the structure
        assert!(discovery.server_patterns.is_none());
    }
}
