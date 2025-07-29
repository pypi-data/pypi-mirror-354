"""Core security scanner for PolicyGuard"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from policyguard.rules import get_default_rules, Rule


@dataclass
class Violation:
    """Represents a security violation found in code"""
    file: str
    line: int
    rule: str
    message: str
    severity: str  # 'error' or 'warning'
    confidence: float  # 0.0 to 1.0
    code_snippet: str = ""


class SecurityScanner:
    """Scans Python code for security vulnerabilities"""
    
    def __init__(self, custom_rules: Optional[List[Rule]] = None):
        """Initialize scanner with default and custom rules"""
        self.rules = get_default_rules()
        if custom_rules:
            self.rules.extend(custom_rules)
    
    def scan_file(self, filepath: Path) -> List[Violation]:
        """Scan a single Python file for security issues"""
        violations = []
        
        if not filepath.exists() or not filepath.suffix == '.py':
            return violations
        
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Check all regex rules
            for rule in self.rules:
                if rule.pattern:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(rule.pattern, line):
                            # Get code context
                            start = max(0, line_num - 2)
                            end = min(len(lines), line_num + 1)
                            context_lines = lines[start:end]
                            snippet = '\n'.join(f"  {i+start+1}: {l}" for i, l in enumerate(context_lines))
                            
                            violations.append(Violation(
                                file=str(filepath),
                                line=line_num,
                                rule=rule.id,
                                message=rule.message,
                                severity=rule.severity,
                                confidence=rule.confidence,
                                code_snippet=snippet
                            ))
            
            # AST-based checks
            if content.strip():
                violations.extend(self._ast_checks(filepath, content))
                
        except Exception as e:
            print(f"Warning: Could not scan {filepath}: {e}")
        
        return violations
    
    def _ast_checks(self, filepath: Path, content: str) -> List[Violation]:
        """Perform AST-based security checks"""
        violations = []
        
        try:
            tree = ast.parse(content)
            
            class SecurityVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.violations = []
                
                def visit_For(self, node):
                    # Check for SQL queries in loops (N+1 problem)
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if hasattr(child.func, 'attr') and child.func.attr in ['execute', 'query']:
                                self.violations.append(Violation(
                                    file=str(filepath),
                                    line=node.lineno,
                                    rule='sql_in_loop',
                                    message='SQL query in loop - potential N+1 problem',
                                    severity='warning',
                                    confidence=0.6,
                                    code_snippet=f"Line {node.lineno}: SQL query inside loop"
                                ))
                                break
                    self.generic_visit(node)
                
                def visit_Try(self, node):
                    # Check for bare except
                    for handler in node.handlers:
                        if handler.type is None:
                            self.violations.append(Violation(
                                file=str(filepath),
                                line=handler.lineno,
                                rule='bare_except',
                                message='Bare except catches all exceptions (hides bugs)',
                                severity='warning',
                                confidence=0.8,
                                code_snippet=f"Line {handler.lineno}: except:"
                            ))
                    self.generic_visit(node)
            
            visitor = SecurityVisitor()
            visitor.visit(tree)
            violations.extend(visitor.violations)
            
        except:
            pass  # AST parsing can fail on invalid Python
        
        return violations
    
    def scan_directory(self, directory: Path, exclude: List[str] = None) -> List[Violation]:
        """Scan all Python files in directory"""
        violations = []
        exclude = exclude or ['.git', '.venv', 'venv', '__pycache__', 'node_modules']
        
        for py_file in directory.rglob("*.py"):
            # Skip excluded directories
            if any(excl in py_file.parts for excl in exclude):
                continue
            violations.extend(self.scan_file(py_file))
        
        return violations
