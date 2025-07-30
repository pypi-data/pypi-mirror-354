use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use crate::types::*;

/// Python wrapper for the prompt composition functionality
#[pyfunction]
fn compose_system_prompt(request_json: &str) -> PyResult<String> {
    let request: PromptRequest = serde_json::from_str(request_json)
        .map_err(|e| PyRuntimeError::new_err(format!("Invalid JSON request: {}", e)))?;
    
    let rt = tokio::runtime::Runtime::new()
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to create async runtime: {}", e)))?;
    
    let response = rt.block_on(crate::compose_system_prompt(request))
        .map_err(|e| PyRuntimeError::new_err(format!("Prompt composition failed: {}", e)))?;
    
    serde_json::to_string(&response)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize response: {}", e)))
}

/// Python wrapper for the prompt composition with custom prompts directory
#[pyfunction]
fn compose_system_prompt_with_prompts_dir(request_json: &str, prompts_dir: &str) -> PyResult<String> {
    let request: PromptRequest = serde_json::from_str(request_json)
        .map_err(|e| PyRuntimeError::new_err(format!("Invalid JSON request: {}", e)))?;
    
    let rt = tokio::runtime::Runtime::new()
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to create async runtime: {}", e)))?;
    
    let response = rt.block_on(crate::compose_system_prompt_with_prompts_dir(request, Some(prompts_dir.to_string())))
        .map_err(|e| PyRuntimeError::new_err(format!("Prompt composition failed: {}", e)))?;
    
    serde_json::to_string(&response)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize response: {}", e)))
}

/// Python wrapper for cached prompt composition (faster, synchronous)
#[pyfunction]
fn compose_system_prompt_cached(request_json: &str) -> PyResult<String> {
    let request: PromptRequest = serde_json::from_str(request_json)
        .map_err(|e| PyRuntimeError::new_err(format!("Invalid JSON request: {}", e)))?;
    
    let response = crate::compose_system_prompt_cached(request)
        .map_err(|e| PyRuntimeError::new_err(format!("Prompt composition failed: {}", e)))?;
    
    serde_json::to_string(&response)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize response: {}", e)))
}

/// Python wrapper for cached prompt composition with custom prompts directory
#[pyfunction]
fn compose_system_prompt_cached_with_prompts_dir(request_json: &str, prompts_dir: &str) -> PyResult<String> {
    let request: PromptRequest = serde_json::from_str(request_json)
        .map_err(|e| PyRuntimeError::new_err(format!("Invalid JSON request: {}", e)))?;
    
    let response = crate::compose_system_prompt_cached_with_prompts_dir(request, Some(prompts_dir.to_string()))
        .map_err(|e| PyRuntimeError::new_err(format!("Prompt composition failed: {}", e)))?;
    
    serde_json::to_string(&response)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize response: {}", e)))
}

/// Python wrapper for refreshing server tools
#[pyfunction]
fn refresh_server_tools(server_name: &str, mcp_config_json: &str) -> PyResult<String> {
    let mcp_config: McpConfig = serde_json::from_str(mcp_config_json)
        .map_err(|e| PyRuntimeError::new_err(format!("Invalid MCP config JSON: {}", e)))?;
    
    let rt = tokio::runtime::Runtime::new()
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to create async runtime: {}", e)))?;
    
    let tools = rt.block_on(crate::refresh_server_tools(server_name, &mcp_config))
        .map_err(|e| PyRuntimeError::new_err(format!("Tool refresh failed: {}", e)))?;
    
    serde_json::to_string(&tools)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize tools: {}", e)))
}

/// Python wrapper for listing available domains
#[pyfunction]
fn list_available_domains() -> PyResult<String> {
    let domains = crate::list_available_domains()
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to list domains: {}", e)))?;
    
    serde_json::to_string(&domains)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize domains: {}", e)))
}

/// Python wrapper for listing available behaviors
#[pyfunction]
fn list_available_behaviors() -> PyResult<String> {
    let behaviors = crate::list_available_behaviors()
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to list behaviors: {}", e)))?;
    
    serde_json::to_string(&behaviors)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize behaviors: {}", e)))
}

/// Python wrapper for listing available domains in custom directory
#[pyfunction]
fn list_available_domains_in_dir(prompts_dir: &str) -> PyResult<String> {
    let domains = crate::list_available_domains_in_dir(prompts_dir.to_string())
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to list domains: {}", e)))?;
    
    serde_json::to_string(&domains)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize domains: {}", e)))
}

/// Python wrapper for listing available behaviors in custom directory
#[pyfunction]
fn list_available_behaviors_in_dir(prompts_dir: &str) -> PyResult<String> {
    let behaviors = crate::list_available_behaviors_in_dir(prompts_dir.to_string())
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to list behaviors: {}", e)))?;
    
    serde_json::to_string(&behaviors)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize behaviors: {}", e)))
}

/// Python wrapper for getting status information
#[pyfunction]
fn get_status() -> PyResult<String> {
    use serde_json;
    
    let domains = crate::list_available_domains().unwrap_or_default();
    let behaviors = crate::list_available_behaviors().unwrap_or_default();
    
    let status = serde_json::json!({
        "available": true,
        "source": "python",
        "version": env!("CARGO_PKG_VERSION"),
        "domains": domains,
        "behaviors": behaviors
    });
    
    serde_json::to_string(&status)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize status: {}", e)))
}

/// Test function to verify module registration
#[pyfunction]
fn test_tools_feature() -> PyResult<String> {
    Ok("Tools feature is working!".to_string())
}

/// Python module definition
#[pymodule]
pub fn python_module(_py: Python, m: &PyModule) -> PyResult<()> {
    // Core functions
    m.add_function(wrap_pyfunction!(compose_system_prompt, m)?)?;
    m.add_function(wrap_pyfunction!(compose_system_prompt_with_prompts_dir, m)?)?;
    m.add_function(wrap_pyfunction!(compose_system_prompt_cached, m)?)?;
    m.add_function(wrap_pyfunction!(compose_system_prompt_cached_with_prompts_dir, m)?)?;
    m.add_function(wrap_pyfunction!(refresh_server_tools, m)?)?;
    
    // Discovery functions
    m.add_function(wrap_pyfunction!(list_available_domains, m)?)?;
    m.add_function(wrap_pyfunction!(list_available_behaviors, m)?)?;
    m.add_function(wrap_pyfunction!(list_available_domains_in_dir, m)?)?;
    m.add_function(wrap_pyfunction!(list_available_behaviors_in_dir, m)?)?;
    m.add_function(wrap_pyfunction!(get_status, m)?)?;
    
    // Test function
    m.add_function(wrap_pyfunction!(test_tools_feature, m)?)?;
    
    // Add version info
    m.add("__version__", "1.0.4")?;
    m.add("__doc__", "A modular system prompt composition framework for AI assistants")?;
    
    Ok(())
}
