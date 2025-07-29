//! Enhanced unused import analysis and trimming using ruff_python_codegen
//!
//! This module builds upon the existing unused import detection to provide
//! actual code transformation capabilities, removing unused imports and
//! generating clean Python code using AST rewriting techniques.

use anyhow::{Context, Result};
use indexmap::IndexSet;
use ruff_python_ast::{self as ast, Stmt};
use ruff_python_codegen::{Generator, Stylist};
use ruff_python_parser;

use crate::unused_imports_simple::{UnusedImport, UnusedImportAnalyzer};

/// Enhanced unused import trimmer that provides AST-based code transformation
pub struct UnusedImportTrimmer {
    analyzer: UnusedImportAnalyzer,
}

/// Result of trimming unused imports from Python code
#[derive(Debug, Clone)]
pub struct TrimResult {
    /// The transformed Python code with unused imports removed
    pub code: String,
    /// List of unused imports that were removed
    pub removed_imports: Vec<UnusedImport>,
    /// Whether any changes were made to the original code
    pub has_changes: bool,
}

/// Configuration for import trimming behavior
#[derive(Debug, Clone)]
pub struct TrimConfig {
    /// Whether to preserve imports with side effects
    pub preserve_side_effects: bool,
    /// Whether to preserve star imports
    pub preserve_star_imports: bool,
    /// Whether to preserve __future__ imports
    pub preserve_future_imports: bool,
    /// Custom patterns for imports to always preserve
    pub preserve_patterns: Vec<String>,
}

impl Default for TrimConfig {
    fn default() -> Self {
        Self {
            preserve_side_effects: true,
            preserve_star_imports: true,
            preserve_future_imports: true,
            preserve_patterns: vec![],
        }
    }
}

impl UnusedImportTrimmer {
    /// Create a new unused import trimmer
    pub fn new() -> Self {
        Self {
            analyzer: UnusedImportAnalyzer::new(),
        }
    }

    /// Analyze and trim unused imports from Python source code
    ///
    /// This method:
    /// 1. Parses the Python source into an AST
    /// 2. Identifies unused imports using the existing analyzer
    /// 3. Removes unused import statements from the AST
    /// 4. Generates clean Python code using ruff_python_codegen
    ///
    /// # Arguments
    /// * `source` - The Python source code to analyze and trim
    /// * `config` - Configuration for trimming behavior
    ///
    /// # Returns
    /// * `Ok(TrimResult)` - The trimmed code and metadata about changes
    /// * `Err` - If parsing or unparsing fails
    pub fn trim_unused_imports(&mut self, source: &str, config: &TrimConfig) -> Result<TrimResult> {
        // Step 1: Analyze for unused imports
        let unused_imports = self.analyze_unused_imports(source)?;

        if unused_imports.is_empty() {
            return self.create_no_changes_result(source);
        }

        // Step 2: Parse source into AST
        let module = self.parse_source_to_ast(source)?;

        // Step 3: Filter unused imports based on config
        let imports_to_remove = self.filter_imports_to_remove(&unused_imports, config);

        if imports_to_remove.is_empty() {
            return self.create_no_changes_result(source);
        }

        // Step 4-6: Transform AST and generate code
        self.transform_ast_and_generate_code(&module, imports_to_remove)
    }

    /// Analyze source for unused imports
    fn analyze_unused_imports(&mut self, source: &str) -> Result<Vec<UnusedImport>> {
        self.analyzer
            .analyze_file(source)
            .context("Failed to analyze unused imports")
    }

    /// Create a result indicating no changes were made
    fn create_no_changes_result(&self, source: &str) -> Result<TrimResult> {
        Ok(TrimResult {
            code: source.to_string(),
            removed_imports: vec![],
            has_changes: false,
        })
    }

    /// Parse source code into AST
    fn parse_source_to_ast(
        &self,
        source: &str,
    ) -> Result<ruff_python_parser::Parsed<ast::ModModule>> {
        ruff_python_parser::parse_module(source).context("Failed to parse Python source code")
    }

    /// Transform AST by removing unused imports and generate clean code
    fn transform_ast_and_generate_code(
        &self,
        module: &ruff_python_parser::Parsed<ast::ModModule>,
        imports_to_remove: Vec<UnusedImport>,
    ) -> Result<TrimResult> {
        // Build set of import names to remove for efficient lookup
        let remove_set: IndexSet<String> = imports_to_remove
            .iter()
            .map(|import| import.name.clone())
            .collect();

        // Transform AST by removing unused import statements
        let original_count = module.syntax().body.len();
        let filtered_body = self.filter_statements(&module.syntax().body, &remove_set)?;
        let has_changes = filtered_body.len() < original_count;

        // Create a new ModModule with the filtered statements
        let filtered_module = ast::ModModule {
            body: filtered_body,
            range: module.syntax().range,
        };

        // Generate clean Python code using ruff_python_codegen
        let code = self.generate_code(&filtered_module)?;

        Ok(TrimResult {
            code,
            removed_imports: imports_to_remove,
            has_changes,
        })
    }

    /// Analyze source code without making changes
    ///
    /// Useful for preview/dry-run mode to see what would be changed
    pub fn analyze_only(&mut self, source: &str, config: &TrimConfig) -> Result<Vec<UnusedImport>> {
        let unused_imports = self
            .analyzer
            .analyze_file(source)
            .context("Failed to analyze unused imports")?;

        Ok(self.filter_imports_to_remove(&unused_imports, config))
    }

    /// Filter unused imports based on configuration settings
    fn filter_imports_to_remove(
        &self,
        unused_imports: &[UnusedImport],
        config: &TrimConfig,
    ) -> Vec<UnusedImport> {
        unused_imports
            .iter()
            .filter(|import| self.should_remove_import(import, config))
            .cloned()
            .collect()
    }

    /// Determine if an import should be removed based on config
    fn should_remove_import(&self, import: &UnusedImport, config: &TrimConfig) -> bool {
        // Check if it's a __future__ import
        if config.preserve_future_imports && import.qualified_name.starts_with("__future__") {
            return false;
        }

        // Check custom preserve patterns
        for pattern in &config.preserve_patterns {
            if import.qualified_name.contains(pattern) {
                return false;
            }
        }

        // For now, always remove - the analyzer already handles side effects and star imports
        // In the future, we can add more sophisticated filtering here
        true
    }

    /// Filter AST statements to remove unused import statements
    fn filter_statements(
        &self,
        statements: &[Stmt],
        remove_set: &IndexSet<String>,
    ) -> Result<Vec<Stmt>> {
        let mut filtered_statements = Vec::new();

        for stmt in statements {
            match stmt {
                Stmt::Import(import_stmt) => {
                    self.process_import_statement(
                        import_stmt,
                        remove_set,
                        &mut filtered_statements,
                    );
                }
                Stmt::ImportFrom(import_from_stmt) => {
                    self.process_import_from_statement(
                        import_from_stmt,
                        remove_set,
                        &mut filtered_statements,
                    );
                }
                _ => {
                    // Keep all non-import statements as-is
                    filtered_statements.push(stmt.clone());
                }
            }
        }

        Ok(filtered_statements)
    }

    /// Process a regular import statement, filtering out unused aliases
    fn process_import_statement(
        &self,
        import_stmt: &ast::StmtImport,
        remove_set: &IndexSet<String>,
        filtered_statements: &mut Vec<Stmt>,
    ) {
        let filtered_aliases = self.filter_import_aliases(&import_stmt.names, remove_set);

        // Only keep the import statement if it has remaining aliases
        if !filtered_aliases.is_empty() {
            let mut new_import = import_stmt.clone();
            new_import.names = filtered_aliases;
            filtered_statements.push(Stmt::Import(new_import));
        }
    }

    /// Process an import-from statement, filtering out unused aliases
    fn process_import_from_statement(
        &self,
        import_from_stmt: &ast::StmtImportFrom,
        remove_set: &IndexSet<String>,
        filtered_statements: &mut Vec<Stmt>,
    ) {
        let filtered_aliases = self.filter_import_aliases(&import_from_stmt.names, remove_set);

        // Only keep the import statement if it has remaining aliases
        if !filtered_aliases.is_empty() {
            let mut new_import = import_from_stmt.clone();
            new_import.names = filtered_aliases;
            filtered_statements.push(Stmt::ImportFrom(new_import));
        }
    }

    /// Filter aliases based on whether they should be removed
    fn filter_import_aliases(
        &self,
        aliases: &[ast::Alias],
        remove_set: &IndexSet<String>,
    ) -> Vec<ast::Alias> {
        aliases
            .iter()
            .filter(|alias| {
                let local_name = alias
                    .asname
                    .as_ref()
                    .map(|n| n.as_str())
                    .unwrap_or_else(|| alias.name.as_str());
                !remove_set.contains(local_name)
            })
            .cloned()
            .collect()
    }

    /// Generate Python code from AST using ruff_python_codegen
    fn generate_code(&self, module: &ast::ModModule) -> Result<String> {
        // Use default styling for the generated code
        let empty_parsed = ruff_python_parser::parse_module("")?;
        let stylist = Stylist::from_tokens(empty_parsed.tokens(), "");

        // Generate code for each statement and combine them
        let mut code_parts = Vec::new();
        for stmt in &module.body {
            let generator = Generator::from(&stylist);
            let stmt_code = generator.stmt(stmt);
            code_parts.push(stmt_code);
        }

        Ok(code_parts.join("\n"))
    }
}

impl Default for UnusedImportTrimmer {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
#[allow(clippy::disallowed_methods)]
mod tests {
    use super::*;
    use insta::{assert_snapshot, with_settings};

    fn format_trim_result(result: &TrimResult) -> String {
        let mut output = String::new();

        output.push_str(&format!("Has changes: {}\n", result.has_changes));
        output.push_str(&format!(
            "Removed imports count: {}\n",
            result.removed_imports.len()
        ));

        if !result.removed_imports.is_empty() {
            output.push_str("Removed imports:\n");
            // Sort removed imports by name for deterministic output
            let mut sorted_imports = result.removed_imports.clone();
            sorted_imports.sort_by(|a, b| a.name.cmp(&b.name));
            for import in &sorted_imports {
                output.push_str(&format!(
                    "  - {} ({})\n",
                    import.name, import.qualified_name
                ));
            }
        }

        output.push_str("Transformed code:\n");
        output.push_str(&result.code);

        output
    }

    #[test]
    fn test_basic_unused_import_trimming() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"import os
import sys
from pathlib import Path

def main():
    print(sys.version)
    p = Path(".")
    print(p)

if __name__ == "__main__":
    main()
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed");

        with_settings!({
            description => "Basic unused import trimming removes only unused imports"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }

    #[test]
    fn test_partial_import_trimming() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"from typing import List, Dict, Optional, Union

def process_data(items: List[str]) -> Dict[str, int]:
    result = {}
    for item in items:
        result[item] = len(item)
    return result
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed for partial import trimming");

        with_settings!({
            description => "Partial import trimming removes only unused items from from-imports"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }

    #[test]
    fn test_no_unused_imports() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"import math
import json

def calculate(x):
    result = math.sqrt(x)
    data = json.dumps({"result": result})
    return data
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed when no unused imports");

        with_settings!({
            description => "Code with no unused imports remains unchanged"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }

    #[test]
    fn test_complex_import_scenarios() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"import os
import sys
import json
from typing import List, Dict, Optional
from collections import defaultdict, Counter
import re

def main():
    # Use sys
    print(sys.version)

    # Use List from typing
    numbers: List[int] = [1, 2, 3]

    # Use defaultdict
    dd = defaultdict(int)
    dd["test"] = 5

    print(f"Numbers: {numbers}")
    print(f"Defaultdict: {dict(dd)}")
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed for complex import scenarios");

        with_settings!({
            description => "Complex import scenario with mixed used and unused imports"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }

    #[test]
    fn test_future_imports_preserved() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"from __future__ import annotations, print_function
import sys
import json

def main():
    print(sys.version)
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed for future imports");

        with_settings!({
            description => "Future imports are preserved by default configuration"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }

    #[test]
    fn test_analyze_only_mode() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"import os
import sys
from pathlib import Path

def main():
    print(sys.version)
    p = Path(".")
    print(p)
"#;

        let unused_imports = trimmer
            .analyze_only(source, &config)
            .expect("analyze_only should succeed");

        let mut output = String::new();
        output.push_str(&format!("Unused imports count: {}\n", unused_imports.len()));
        for import in &unused_imports {
            output.push_str(&format!(
                "  - {} ({})\n",
                import.name, import.qualified_name
            ));
        }

        with_settings!({
            description => "Analyze-only mode identifies unused imports without modifying code"
        }, {
            assert_snapshot!(output);
        });
    }

    #[test]
    fn test_custom_preserve_patterns() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig {
            preserve_patterns: vec!["django".to_string(), "pytest".to_string()],
            ..Default::default()
        };

        let source = r#"import os
import django.setup
import pytest_django
import json

def main():
    pass
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed for custom preserve patterns");

        with_settings!({
            description => "Custom preserve patterns keep specified imports even if unused"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }

    #[test]
    fn test_empty_import_statements_removed() {
        let mut trimmer = UnusedImportTrimmer::new();
        let config = TrimConfig::default();

        let source = r#"from typing import Optional, Union
from collections import Counter, deque
import json

def process(data: Optional[str]) -> str:
    return data or "default"
"#;

        let result = trimmer
            .trim_unused_imports(source, &config)
            .expect("trim_unused_imports should succeed for empty import statements removal");

        with_settings!({
            description => "Import statements with all unused items are completely removed"
        }, {
            assert_snapshot!(format_trim_result(&result));
        });
    }
}
