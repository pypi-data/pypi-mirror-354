use std::collections::HashMap;
use std::fs;
use std::path::Path;
use crate::types::*;

/// Loads prompt content from markdown files
pub struct PromptLoader {
    prompts_dir: String,
    cached_content: HashMap<String, String>,
}

impl PromptLoader {
    /// Create a new prompt loader with specified prompts directory
    pub fn new(prompts_dir: Option<String>) -> Self {
        let default_dir = prompts_dir.unwrap_or_else(|| {
            // Try to find prompts directory relative to current working directory
            if std::path::Path::new("prompts").exists() {
                "prompts".to_string()
            } else if std::path::Path::new("../prompts").exists() {
                "../prompts".to_string()
            } else {
                // Fallback to a path relative to where the binary might be
                "prompts".to_string()
            }
        });
        
        Self {
            prompts_dir: default_dir,
            cached_content: HashMap::new(),
        }
    }

    /// Load content from a specific prompt file
    pub fn load_prompt(&mut self, category: &str, name: &str) -> Result<String, PromptError> {
        let cache_key = format!("{}:{}", category, name);
        
        // Check cache first
        if let Some(cached) = self.cached_content.get(&cache_key) {
            return Ok(cached.clone());
        }

        // Build file path
        let file_path = Path::new(&self.prompts_dir)
            .join(category)
            .join(format!("{}.md", name));

        // Read file content
        let content = fs::read_to_string(&file_path)
            .map_err(|e| PromptError::ModuleLoadingFailed(
                format!("Failed to load prompt file {:?}: {}", file_path, e)
            ))?;

        // Cache and return
        self.cached_content.insert(cache_key, content.clone());
        Ok(content)
    }

    /// Load domain-specific guidance
    pub fn load_domain(&mut self, domain: &str) -> Result<String, PromptError> {
        self.load_prompt("domains", domain)
    }

    /// Load behavioral pattern guidance
    pub fn load_behavior(&mut self, behavior: &str) -> Result<String, PromptError> {
        self.load_prompt("behaviors", behavior)
    }

    /// Load tool-specific guidance
    pub fn load_tool(&mut self, tool_name: &str) -> Result<String, PromptError> {
        self.load_prompt("tools", tool_name)
    }

    /// Check if a tool-specific prompt file exists
    pub fn has_tool_prompt(&self, tool_name: &str) -> bool {
        let file_path = Path::new(&self.prompts_dir)
            .join("tools")
            .join(format!("{}.md", tool_name));
        file_path.exists()
    }

    /// Extract the main content from markdown (skip headers, get body)
    pub fn extract_guidance(&self, markdown_content: &str) -> String {
        let lines: Vec<&str> = markdown_content.lines().collect();
        let mut guidance_lines = Vec::new();
        let mut in_content = false;
        
        for line in lines {
            // Skip title headers
            if line.starts_with("# ") {
                continue;
            }
            
            // Start collecting after first section header or bullet point
            if line.starts_with("## ") || line.starts_with("- ") || line.starts_with("### ") {
                in_content = true;
            }
            
            if in_content {
                // Convert markdown headers to plain text for prompts
                if line.starts_with("### ") {
                    guidance_lines.push(line[4..].to_string());
                } else if line.starts_with("## ") {
                    let formatted = format!("{}:", &line[3..]);
                    guidance_lines.push(formatted);
                } else {
                    guidance_lines.push(line.to_string());
                }
            }
        }
        
        guidance_lines.join("\n").trim().to_string()
    }

    /// Get list of available domain files
    pub fn list_domains(&self) -> Result<Vec<String>, PromptError> {
        self.list_category("domains")
    }

    /// Get list of available behavior files  
    pub fn list_behaviors(&self) -> Result<Vec<String>, PromptError> {
        self.list_category("behaviors")
    }

    /// Get list of available tool files
    pub fn list_tools(&self) -> Result<Vec<String>, PromptError> {
        self.list_category("tools")
    }

    fn list_category(&self, category: &str) -> Result<Vec<String>, PromptError> {
        let category_path = Path::new(&self.prompts_dir).join(category);
        
        let entries = fs::read_dir(&category_path)
            .map_err(|e| PromptError::ModuleLoadingFailed(
                format!("Failed to read {} directory: {}", category, e)
            ))?;

        let mut files = Vec::new();
        for entry in entries {
            let entry = entry.map_err(|e| PromptError::ModuleLoadingFailed(
                format!("Failed to read directory entry: {}", e)
            ))?;
            
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("md") {
                if let Some(stem) = path.file_stem().and_then(|s| s.to_str()) {
                    files.push(stem.to_string());
                }
            }
        }
        
        files.sort();
        Ok(files)
    }

    /// Check if prompts directory exists and is accessible
    pub fn validate_prompts_dir(&self) -> Result<(), PromptError> {
        let prompts_path = Path::new(&self.prompts_dir);
        
        if !prompts_path.exists() {
            return Err(PromptError::ConfigError(
                format!("Prompts directory does not exist: {}", self.prompts_dir)
            ));
        }

        let domains_path = prompts_path.join("domains");
        let behaviors_path = prompts_path.join("behaviors");
        let tools_path = prompts_path.join("tools");

        if !domains_path.exists() {
            return Err(PromptError::ConfigError(
                format!("Domains directory does not exist: {:?}", domains_path)
            ));
        }

        if !behaviors_path.exists() {
            return Err(PromptError::ConfigError(
                format!("Behaviors directory does not exist: {:?}", behaviors_path)
            ));
        }

        // Tools directory is optional for backward compatibility
        if !tools_path.exists() {
            eprintln!("Note: Tools directory does not exist: {:?} (this is optional)", tools_path);
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_guidance() {
        let loader = PromptLoader::new(None);
        let markdown = r#"# File System Operations

## Core Principles

- Always read files first
- Use absolute paths

## Best Practices

### Writing
- Use chunked writing
"#;

        let guidance = loader.extract_guidance(markdown);
        assert!(guidance.contains("Core Principles:"));
        assert!(guidance.contains("Always read files first"));
        assert!(guidance.contains("Writing"));
    }
}
