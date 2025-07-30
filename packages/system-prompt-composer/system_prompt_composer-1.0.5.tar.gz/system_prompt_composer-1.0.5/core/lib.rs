pub mod types;
pub mod modules;
pub mod discovery;
pub mod loader;
pub mod composition;

#[cfg(feature = "python")]
pub mod python;

// For PyO3, we need to define the module at the crate root
#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
fn _system_prompt_composer(_py: Python, m: &PyModule) -> PyResult<()> {
    python::python_module(_py, m)
}

// NAPI-RS bindings - must be in lib.rs for proper registration
#[cfg(feature = "nodejs")]
use napi_derive::napi;

use types::*;
use composition::PromptComposer;
use discovery::ToolDiscovery;
use std::sync::Mutex;

/// Global tool discovery instance with caching
static TOOL_DISCOVERY: Mutex<Option<ToolDiscovery>> = Mutex::new(None);

/// Main function to compose system prompts based on MCP configuration and session state
pub async fn compose_system_prompt(request: PromptRequest) -> Result<PromptResponse, PromptError> {
    compose_system_prompt_with_prompts_dir(request, None).await
}

/// Compose system prompt with custom prompts directory
pub async fn compose_system_prompt_with_prompts_dir(
    request: PromptRequest, 
    prompts_dir: Option<String>
) -> Result<PromptResponse, PromptError> {
    let start_time = std::time::Instant::now();
    
    // Initialize or get tool discovery instance
    let mut discovery = {
        let mut guard = TOOL_DISCOVERY.lock().unwrap();
        if guard.is_none() {
            *guard = Some(match &prompts_dir {
                Some(dir) => ToolDiscovery::with_prompts_dir(dir.clone()),
                None => ToolDiscovery::new(),
            });
        }
        guard.take().unwrap()
    };

    // Discover available tools
    let tools = discovery.discover_tools(&request.mcp_config).await?;
    
    // Put discovery back
    {
        let mut guard = TOOL_DISCOVERY.lock().unwrap();
        *guard = Some(discovery);
    }

    // Create composer with appropriate prompts directory
    let mut composer = match prompts_dir {
        Some(dir) => PromptComposer::with_prompts_dir(dir),
        None => PromptComposer::new(),
    };

    // Compose the prompt
    let response = composer.compose(&request, &tools)?;
    
    // Track performance
    let elapsed = start_time.elapsed();
    if elapsed.as_millis() > 50 {
        eprintln!("Warning: Prompt composition took {}ms", elapsed.as_millis());
    }

    Ok(response)
}

/// Synchronous version that uses cached tools or infers from config
pub fn compose_system_prompt_cached(request: PromptRequest) -> Result<PromptResponse, PromptError> {
    compose_system_prompt_cached_with_prompts_dir(request, None)
}

/// Cached version with custom prompts directory
pub fn compose_system_prompt_cached_with_prompts_dir(
    request: PromptRequest, 
    prompts_dir: Option<String>
) -> Result<PromptResponse, PromptError> {
    let start_time = std::time::Instant::now();
    
    // Get cached tools, but if cache is empty, infer from config
    let tools = {
        let mut guard = TOOL_DISCOVERY.lock().unwrap();
        if let Some(ref mut discovery) = *guard {
            let cached = discovery.get_cached_tools();
            if cached.is_empty() {
                // Cache is empty, infer tools from MCP config
                discovery.infer_tools_from_config_immediate(&request.mcp_config)
            } else {
                cached
            }
        } else {
            // No discovery instance, create temporary one to infer from config
            let mut discovery = ToolDiscovery::new();
            discovery.infer_tools_from_config_immediate(&request.mcp_config)
        }
    };

    // Create composer with appropriate prompts directory
    let mut composer = match prompts_dir {
        Some(dir) => PromptComposer::with_prompts_dir(dir),
        None => PromptComposer::new(),
    };

    // Compose the prompt
    let response = composer.compose(&request, &tools)?;
    
    // Track performance
    let elapsed = start_time.elapsed();
    if elapsed.as_millis() > 10 {
        eprintln!("Warning: Cached prompt composition took {}ms", elapsed.as_millis());
    }

    Ok(response)
}

/// Force refresh tools for a specific server
pub async fn refresh_server_tools(server_name: &str, mcp_config: &McpConfig) -> Result<Vec<Tool>, PromptError> {
    let mut discovery = {
        let mut guard = TOOL_DISCOVERY.lock().unwrap();
        guard.take().unwrap_or_else(ToolDiscovery::new)
    };

    let tools = discovery.refresh_server(server_name, mcp_config).await?;
    
    // Put discovery back
    {
        let mut guard = TOOL_DISCOVERY.lock().unwrap();
        *guard = Some(discovery);
    }

    Ok(tools)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[tokio::test]
    async fn test_basic_prompt_composition() {
        let mut mcp_servers = HashMap::new();
        mcp_servers.insert("test-server".to_string(), McpServer {
            name: "test-server".to_string(),
            command: "test-command".to_string(),
            args: vec![],
            env: None,
        });

        let request = PromptRequest {
            user_prompt: "Read the README.md file".to_string(),
            mcp_config: McpConfig { mcp_servers },
            session_state: Some(SessionState {
                tool_call_count: Some(0),
                ..Default::default()
            }),
            domain_hints: None,
            behavior_hints: None,
            task_complexity: Some(TaskComplexity::Simple),
        };

        let response = compose_system_prompt(request).await.unwrap();
        assert!(!response.system_prompt.is_empty());
        // Note: tool recognition depends on server pattern matching
    }

    #[test]
    fn test_cached_prompt_composition() {
        let mut mcp_servers = HashMap::new();
        mcp_servers.insert("test-server".to_string(), McpServer {
            name: "test-server".to_string(),
            command: "test-command".to_string(),
            args: vec![],
            env: None,
        });

        let request = PromptRequest {
            user_prompt: "Read a file".to_string(),
            mcp_config: McpConfig { mcp_servers },
            session_state: None,
            domain_hints: None,
            behavior_hints: None,
            task_complexity: None,
        };

        let response = compose_system_prompt_cached(request).unwrap();
        assert!(!response.system_prompt.is_empty());
        // Note: tool recognition depends on server pattern matching
    }

    #[test]
    fn test_list_modules() {
        // These will only work if prompts directory exists
        if let Ok(domains) = list_available_domains() {
            println!("Available domains: {:?}", domains);
        }
        
        if let Ok(behaviors) = list_available_behaviors() {
            println!("Available behaviors: {:?}", behaviors);
        }
    }
}

// NAPI-RS bindings for Node.js
#[cfg(feature = "nodejs")]
mod napi_bindings {
    use super::*;
    use napi_derive::napi;

    /// Compose a system prompt using the cached version for better performance
    #[napi]
    pub fn compose_system_prompt(request: String) -> napi::Result<String> {
        use serde_json;
        
        // Parse the request
        let parsed_request: types::PromptRequest = serde_json::from_str(&request)
            .map_err(|e| napi::Error::from_reason(format!("Invalid JSON: {}", e)))?;
        
        // Call the cached version for better performance
        let response = crate::compose_system_prompt_cached(parsed_request)
            .map_err(|e| napi::Error::from_reason(format!("Composition failed: {}", e)))?;
        
        // Return as JSON string
        serde_json::to_string(&response)
            .map_err(|e| napi::Error::from_reason(format!("Serialization failed: {}", e)))
    }

    /// Compose a system prompt with custom prompts directory
    #[napi]
    pub fn compose_system_prompt_with_prompts_dir(request: String, prompts_dir: String) -> napi::Result<String> {
        use serde_json;
        
        // Parse the request
        let parsed_request: types::PromptRequest = serde_json::from_str(&request)
            .map_err(|e| napi::Error::from_reason(format!("Invalid JSON: {}", e)))?;
        
        // Call the version with custom prompts directory
        let response = crate::compose_system_prompt_cached_with_prompts_dir(parsed_request, Some(prompts_dir))
            .map_err(|e| napi::Error::from_reason(format!("Composition failed: {}", e)))?;
        
        // Return as JSON string
        serde_json::to_string(&response)
            .map_err(|e| napi::Error::from_reason(format!("Serialization failed: {}", e)))
    }

    /// Check if the native bindings are available (always true)
    #[napi]
    pub fn is_available() -> bool {
        true
    }

    /// Get status information as JSON string
    #[napi]
    pub fn get_status() -> napi::Result<String> {
        use serde_json;
        
        let composer = crate::PromptComposer::new();
        let domains = composer.list_domains().unwrap_or_default();
        let behaviors = composer.list_behaviors().unwrap_or_default();
        let tools = composer.list_tools().unwrap_or_default();
        
        let status = serde_json::json!({
            "available": true,
            "source": "native",
            "version": env!("CARGO_PKG_VERSION"),
            "domains": domains,
            "behaviors": behaviors,
            "tools": tools
        });
        
        serde_json::to_string(&status)
            .map_err(|e| napi::Error::from_reason(format!("Serialization failed: {}", e)))
    }
}
