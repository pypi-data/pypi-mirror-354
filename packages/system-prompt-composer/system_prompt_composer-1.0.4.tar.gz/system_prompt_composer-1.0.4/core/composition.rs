use crate::types::*;
use crate::modules::{ModuleSelector, PromptModule};
use crate::loader::PromptLoader;

/// Main prompt composition service
pub struct PromptComposer {
    loader: PromptLoader,
}

impl PromptComposer {
    /// Create a new composer with default prompts directory
    pub fn new() -> Self {
        Self {
            loader: PromptLoader::new(None),
        }
    }

    /// Create a new composer with custom prompts directory
    pub fn with_prompts_dir(prompts_dir: String) -> Self {
        Self {
            loader: PromptLoader::new(Some(prompts_dir)),
        }
    }

    /// Compose a system prompt based on request
    pub fn compose(&mut self, request: &PromptRequest, tools: &[Tool]) -> Result<PromptResponse, PromptError> {
        let start_time = std::time::Instant::now();
        
        // Validate prompts directory exists
        self.loader.validate_prompts_dir()?;
        
        // Assess task complexity
        let complexity = assess_task_complexity(request);
        
        // Get session state with defaults
        let session_state = request.session_state.as_ref().cloned().unwrap_or_default();
        
        // Select appropriate modules
        let modules = ModuleSelector::select_modules(
            tools, 
            &request.user_prompt, 
            &session_state,
            request.domain_hints.as_deref(),
            request.behavior_hints.as_deref()
        );
        
        // Generate prompt content (this will include tool instructions)
        let (system_prompt, tool_instructions_used) = self.generate_prompt_content(request, tools, &modules, &session_state)?;
        
        // Build applied modules list (includes both behavior/domain modules and tool instructions)
        let mut applied_modules: Vec<String> = modules.iter().map(|m| m.name().to_string()).collect();
        applied_modules.extend(tool_instructions_used.into_iter().map(|t| format!("tool:{}", t)));
        
        // Track performance
        let elapsed = start_time.elapsed();
        if elapsed.as_millis() > 50 {
            eprintln!("Warning: Prompt composition took {}ms", elapsed.as_millis());
        }

        Ok(PromptResponse {
            system_prompt,
            applied_modules,
            recognized_tools: tools.iter().map(|t| t.name.clone()).collect(),
            complexity_assessment: complexity,
        })
    }

    /// Generate the final prompt content by combining all module outputs
    fn generate_prompt_content(
        &mut self,
        request: &PromptRequest,
        tools: &[Tool], 
        modules: &[Box<dyn PromptModule>], 
        session_state: &SessionState
    ) -> Result<(String, Vec<String>), PromptError> {
        let mut content = String::new();
        
        // Add content from behavior/domain modules
        for module in modules {
            let module_content = module.generate_content(tools, session_state, &mut self.loader)?;
            if !module_content.is_empty() {
                if !content.is_empty() {
                    content.push('\n');
                }
                content.push_str(&module_content);
            }
        }
        
        // Add tool-specific instructions for each MCP server
        let (tool_instructions, included_tools) = self.generate_tool_instructions(request)?;
        if !tool_instructions.is_empty() {
            if !content.is_empty() {
                content.push_str("\n\n");
            }
            content.push_str(&tool_instructions);
        }
        
        // Add general guidance if we have tools but no specific modules generated content
        if content.is_empty() && !tools.is_empty() {
            content = format!(
                "You have access to {} tools. Use them appropriately to complete the user's request.",
                tools.len()
            );
        }
        
        Ok((content, included_tools))
    }

    /// Generate tool-specific instructions based on available MCP servers
    fn generate_tool_instructions(&mut self, request: &PromptRequest) -> Result<(String, Vec<String>), PromptError> {
        let mut tool_content = String::new();
        let mut included_tools = Vec::new();
        
        // Check each MCP server for corresponding tool instructions
        for (server_name, _server_config) in &request.mcp_config.mcp_servers {
            if self.loader.has_tool_prompt(server_name) {
                match self.loader.load_tool(server_name) {
                    Ok(tool_instructions) => {
                        if !tool_content.is_empty() {
                            tool_content.push_str("\n\n");
                        }
                        
                        // Extract the guidance content and format it appropriately
                        let guidance = self.loader.extract_guidance(&tool_instructions);
                        if !guidance.is_empty() {
                            tool_content.push_str(&guidance);
                            included_tools.push(server_name.clone());
                        }
                    }
                    Err(e) => {
                        eprintln!("Warning: Failed to load tool instructions for {}: {}", server_name, e);
                    }
                }
            }
        }
        
        if !included_tools.is_empty() {
            eprintln!("Included tool-specific instructions for: {}", included_tools.join(", "));
        }
        
        Ok((tool_content, included_tools))
    }

    /// Get list of available domain modules
    pub fn list_domains(&self) -> Result<Vec<String>, PromptError> {
        self.loader.list_domains()
    }

    /// Get list of available behavior modules  
    pub fn list_behaviors(&self) -> Result<Vec<String>, PromptError> {
        self.loader.list_behaviors()
    }

    /// Get list of available tool modules
    pub fn list_tools(&self) -> Result<Vec<String>, PromptError> {
        self.loader.list_tools()
    }
}

impl Default for PromptComposer {
    fn default() -> Self {
        Self::new()
    }
}

/// Assess task complexity based on user prompt and configuration
fn assess_task_complexity(request: &PromptRequest) -> TaskComplexity {
    match request.task_complexity {
        Some(ref complexity) => complexity.clone(),
        None => {
            // Auto-detect complexity
            let prompt = &request.user_prompt;
            let complex_indicators = [
                "refactor", "implement", "create", "build", "develop",
                "comprehensive", "analysis", "strategy", "plan", "design",
                "multiple", "all", "entire", "complete", "full", "system"
            ];
            
            let prompt_lower = prompt.to_lowercase();
            let has_complex_keywords = complex_indicators.iter()
                .any(|indicator| prompt_lower.contains(indicator));
            
            let is_long = prompt.len() > 100;
            let has_multiple_servers = request.mcp_config.mcp_servers.len() > 2;
            
            if has_complex_keywords || is_long || has_multiple_servers {
                TaskComplexity::Complex
            } else {
                TaskComplexity::Simple
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn test_complexity_assessment() {
        let mut mcp_servers = HashMap::new();
        mcp_servers.insert("test".to_string(), McpServer {
            name: "test".to_string(),
            command: "test".to_string(),
            args: vec![],
            env: None,
        });

        let simple_request = PromptRequest {
            user_prompt: "What's the weather?".to_string(),
            mcp_config: McpConfig { mcp_servers: mcp_servers.clone() },
            session_state: None,
            domain_hints: None,
            behavior_hints: None,
            task_complexity: None,
        };

        let complex_request = PromptRequest {
            user_prompt: "Refactor the entire codebase to implement a comprehensive microservices architecture".to_string(),
            mcp_config: McpConfig { mcp_servers },
            session_state: None,
            domain_hints: None,
            behavior_hints: None,
            task_complexity: None,
        };

        let simple_complexity = assess_task_complexity(&simple_request);
        let complex_complexity = assess_task_complexity(&complex_request);

        assert!(matches!(simple_complexity, TaskComplexity::Simple));
        assert!(matches!(complex_complexity, TaskComplexity::Complex));
    }
}
