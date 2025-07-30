use crate::types::*;
use crate::loader::PromptLoader;

/// Trait for prompt modules that provide specific guidance
pub trait PromptModule: Send + Sync {
    fn name(&self) -> &str;
    fn generate_content(&self, tools: &[Tool], session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError>;
    fn applies_to(&self, tools: &[Tool], user_prompt: &str, session_state: &SessionState) -> bool;
}

/// Basic tool usage guidance module
pub struct ToolUsageModule;

impl PromptModule for ToolUsageModule {
    fn name(&self) -> &str {
        "tool_usage"
    }

    fn generate_content(&self, tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        if tools.is_empty() {
            return Ok(String::new());
        }

        let mut content = String::from("You have access to the following tools:\n");
        
        for tool in tools {
            content.push_str(&format!("- {}: {}\n", tool.name, tool.description));
        }

        // Load general tool usage guidance from file
        let tool_guidance = loader.load_behavior("tools")?;
        let extracted_guidance = loader.extract_guidance(&tool_guidance);
        
        content.push('\n');
        content.push_str(&extracted_guidance);

        Ok(content)
    }

    fn applies_to(&self, tools: &[Tool], _user_prompt: &str, _session_state: &SessionState) -> bool {
        !tools.is_empty()
    }
}

/// File system operations guidance module
pub struct FilesystemModule;

impl PromptModule for FilesystemModule {
    fn name(&self) -> &str {
        "filesystem"
    }

    fn generate_content(&self, tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        let has_filesystem_tools = tools.iter().any(|tool| {
            ToolCategory::from_tool(tool) == ToolCategory::FileSystem
        });

        if !has_filesystem_tools {
            return Ok(String::new());
        }

        // Load filesystem guidance from file
        let filesystem_content = loader.load_domain("filesystem")?;
        let guidance = loader.extract_guidance(&filesystem_content);
        
        Ok(format!("\nFILE SYSTEM GUIDANCE:\n{}", guidance))
    }

    fn applies_to(&self, tools: &[Tool], _user_prompt: &str, _session_state: &SessionState) -> bool {
        tools.iter().any(|tool| ToolCategory::from_tool(tool) == ToolCategory::FileSystem)
    }
}

/// Task planning guidance for complex tasks
pub struct TaskPlanningModule;

impl PromptModule for TaskPlanningModule {
    fn name(&self) -> &str {
        "task_planning"
    }

    fn generate_content(&self, _tools: &[Tool], session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        let has_plan = session_state.has_plan.unwrap_or(false);
        
        if has_plan {
            return Ok(String::new());
        }

        // Load planning guidance from file
        let planning_content = loader.load_behavior("planning")?;
        let guidance = loader.extract_guidance(&planning_content);
        
        Ok(format!("\nCOMPLEX TASK PLANNING:\n{}", guidance))
    }

    fn applies_to(&self, _tools: &[Tool], user_prompt: &str, session_state: &SessionState) -> bool {
        let has_plan = session_state.has_plan.unwrap_or(false);
        !has_plan && is_complex_task(user_prompt)
    }
}

/// Progress monitoring for ongoing work
pub struct ProgressMonitoringModule;

impl PromptModule for ProgressMonitoringModule {
    fn name(&self) -> &str {
        "progress_monitoring"
    }

    fn generate_content(&self, _tools: &[Tool], session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        let tool_count = session_state.tool_call_count.unwrap_or(0);
        let original_task = session_state.original_task
            .as_deref()
            .unwrap_or("the current task");

        // Load progress monitoring guidance from file
        let progress_content = loader.load_behavior("progress")?;
        let guidance = loader.extract_guidance(&progress_content);

        Ok(format!(
            "\nPROGRESS MONITORING:\n\
            Your original task was: \"{}\"\n\n\
            You've executed {} tool calls so far.\n\n\
            {}",
            original_task, tool_count, guidance
        ))
    }

    fn applies_to(&self, _tools: &[Tool], _user_prompt: &str, session_state: &SessionState) -> bool {
        session_state.tool_call_count.unwrap_or(0) >= 6
    }
}

/// Programming best practices module
pub struct ProgrammingModule;

impl PromptModule for ProgrammingModule {
    fn name(&self) -> &str {
        "programming"
    }

    fn generate_content(&self, _tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        // Load programming guidance from file
        let programming_content = loader.load_domain("programming")?;
        let guidance = loader.extract_guidance(&programming_content);
        
        Ok(format!("\nPROGRAMMING BEST PRACTICES:\n{}", guidance))
    }

    fn applies_to(&self, tools: &[Tool], user_prompt: &str, _session_state: &SessionState) -> bool {
        let has_file_tools = tools.iter().any(|tool| {
            ToolCategory::from_tool(tool) == ToolCategory::FileSystem
        });
        
        let programming_keywords = [
            "code", "function", "class", "refactor", "implement", 
            "debug", "fix", "python", "rust", "javascript", "api"
        ];
        
        let user_prompt_lower = user_prompt.to_lowercase();
        let mentions_programming = programming_keywords.iter()
            .any(|keyword| user_prompt_lower.contains(keyword));

        has_file_tools && mentions_programming
    }
}

/// Data Analysis module
pub struct AnalysisModule;

impl PromptModule for AnalysisModule {
    fn name(&self) -> &str {
        "analysis"
    }

    fn generate_content(&self, _tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        // Load analysis guidance from file
        let analysis_content = loader.load_domain("analysis")?;
        let guidance = loader.extract_guidance(&analysis_content);
        
        Ok(format!("\nDATA ANALYSIS METHODOLOGY:\n{}", guidance))
    }

    fn applies_to(&self, tools: &[Tool], user_prompt: &str, _session_state: &SessionState) -> bool {
        let analysis_keywords = [
            "analyze", "analysis", "data", "csv", "trends", "statistics", 
            "report", "insights", "metrics", "dashboard"
        ];
        
        let user_prompt_lower = user_prompt.to_lowercase();
        let mentions_analysis = analysis_keywords.iter()
            .any(|keyword| user_prompt_lower.contains(keyword));

        let has_data_tools = tools.iter().any(|tool| {
            ToolCategory::from_tool(tool) == ToolCategory::DataAnalysis
        });

        mentions_analysis || has_data_tools
    }
}

/// System Administration module
pub struct SystemModule;

impl PromptModule for SystemModule {
    fn name(&self) -> &str {
        "system"
    }

    fn generate_content(&self, _tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        // Load system administration guidance from file
        let system_content = loader.load_domain("system")?;
        let guidance = loader.extract_guidance(&system_content);
        
        Ok(format!("\nSYSTEM ADMINISTRATION GUIDANCE:\n{}", guidance))
    }

    fn applies_to(&self, tools: &[Tool], user_prompt: &str, _session_state: &SessionState) -> bool {
        let system_keywords = [
            "server", "deployment", "infrastructure", "configuration", 
            "security", "backup", "monitor", "admin", "service"
        ];
        
        let user_prompt_lower = user_prompt.to_lowercase();
        let mentions_system = system_keywords.iter()
            .any(|keyword| user_prompt_lower.contains(keyword));

        let has_system_tools = tools.iter().any(|tool| {
            ToolCategory::from_tool(tool) == ToolCategory::SystemAdmin
        });

        mentions_system || has_system_tools
    }
}

/// Generic domain module that loads content from domain files
pub struct GenericDomainModule {
    domain_name: String,
}

impl GenericDomainModule {
    pub fn new(domain_name: String) -> Self {
        Self { domain_name }
    }
}

impl PromptModule for GenericDomainModule {
    fn name(&self) -> &str {
        &self.domain_name
    }

    fn generate_content(&self, _tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        match loader.load_domain(&self.domain_name) {
            Ok(content) => {
                let guidance = loader.extract_guidance(&content);
                Ok(format!("\n{}:\n{}", self.domain_name.to_uppercase(), guidance))
            }
            Err(_) => {
                // Domain file doesn't exist, return empty content
                Ok(String::new())
            }
        }
    }

    fn applies_to(&self, _tools: &[Tool], _user_prompt: &str, _session_state: &SessionState) -> bool {
        true // Always applies when explicitly requested
    }
}

/// Generic behavior module that loads content from behavior files
pub struct GenericBehaviorModule {
    behavior_name: String,
}

impl GenericBehaviorModule {
    pub fn new(behavior_name: String) -> Self {
        Self { behavior_name }
    }
}

impl PromptModule for GenericBehaviorModule {
    fn name(&self) -> &str {
        &self.behavior_name
    }

    fn generate_content(&self, _tools: &[Tool], _session_state: &SessionState, loader: &mut PromptLoader) -> Result<String, PromptError> {
        match loader.load_behavior(&self.behavior_name) {
            Ok(content) => {
                let guidance = loader.extract_guidance(&content);
                Ok(format!("\n{}:\n{}", self.behavior_name.to_uppercase(), guidance))
            }
            Err(_) => {
                // Behavior file doesn't exist, return empty content
                Ok(String::new())
            }
        }
    }

    fn applies_to(&self, _tools: &[Tool], _user_prompt: &str, _session_state: &SessionState) -> bool {
        true // Always applies when explicitly requested
    }
}

/// Detect if a task is complex based on user prompt
fn is_complex_task(user_prompt: &str) -> bool {
    let complex_indicators = [
        "refactor", "implement", "create a", "build", "develop", 
        "comprehensive", "analysis", "strategy", "plan", "design",
        "multiple", "all", "entire", "complete", "full"
    ];
    
    let user_prompt_lower = user_prompt.to_lowercase();
    complex_indicators.iter().any(|indicator| user_prompt_lower.contains(indicator))
        || user_prompt.len() > 100 // Long prompts tend to be complex
}

/// Module selector that determines which modules to apply
pub struct ModuleSelector;

impl ModuleSelector {
    pub fn select_modules(
        tools: &[Tool], 
        user_prompt: &str, 
        session_state: &SessionState,
        domain_hints: Option<&[String]>,
        behavior_hints: Option<&[String]>
    ) -> Vec<Box<dyn PromptModule>> {
        let mut modules: Vec<Box<dyn PromptModule>> = vec![];
        
        // Always include tool usage if we have tools
        if !tools.is_empty() {
            modules.push(Box::new(ToolUsageModule));
        }
        
        // Handle explicit domain hints first
        if let Some(domains) = domain_hints {
            for domain in domains {
                match domain.as_str() {
                    "filesystem" => modules.push(Box::new(FilesystemModule)),
                    "programming" => modules.push(Box::new(ProgrammingModule)),
                    "analysis" => modules.push(Box::new(AnalysisModule)),
                    "system" => modules.push(Box::new(SystemModule)),
                    _ => {
                        // For unknown domains, create a generic domain module
                        modules.push(Box::new(GenericDomainModule::new(domain.clone())));
                    }
                }
            }
        } else {
            // Fall back to auto-detection for domain modules
            let filesystem_module = FilesystemModule;
            if filesystem_module.applies_to(tools, user_prompt, session_state) {
                modules.push(Box::new(filesystem_module));
            }
            
            let programming_module = ProgrammingModule;
            if programming_module.applies_to(tools, user_prompt, session_state) {
                modules.push(Box::new(programming_module));
            }
            
            let analysis_module = AnalysisModule;
            if analysis_module.applies_to(tools, user_prompt, session_state) {
                modules.push(Box::new(analysis_module));
            }
            
            let system_module = SystemModule;
            if system_module.applies_to(tools, user_prompt, session_state) {
                modules.push(Box::new(system_module));
            }
        }
        
        // Handle explicit behavior hints
        if let Some(behaviors) = behavior_hints {
            for behavior in behaviors {
                match behavior.as_str() {
                    "planning" => {
                        modules.push(Box::new(TaskPlanningModule));
                    },
                    "progress" => {
                        modules.push(Box::new(ProgressMonitoringModule));
                    },
                    _ => {
                        // For unknown behaviors, create a generic behavior module
                        modules.push(Box::new(GenericBehaviorModule::new(behavior.clone())));
                    }
                }
            }
        } else {
            // Fall back to auto-detection for behavioral modules
            let planning_module = TaskPlanningModule;
            if planning_module.applies_to(tools, user_prompt, session_state) {
                modules.push(Box::new(planning_module));
            }
            
            let progress_module = ProgressMonitoringModule;
            if progress_module.applies_to(tools, user_prompt, session_state) {
                modules.push(Box::new(progress_module));
            }
        }
        
        modules
    }
}
