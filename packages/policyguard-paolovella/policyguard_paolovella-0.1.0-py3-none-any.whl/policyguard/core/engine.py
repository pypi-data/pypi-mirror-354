# policyguard/core/engine.py
"""
PolicyGuard Core Engine
Patent Pending: Real-time AI suggestion governance
"""

import ast
import time
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
import hashlib
import json

@dataclass
class CodeSuggestion:
    """Represents an AI-generated code suggestion"""
    id: str
    content: str
    language: str
    context: Dict
    source: str  # 'copilot', 'codewhisperer', 'claude', etc.
    timestamp: float

@dataclass
class PolicyViolation:
    """Represents a detected policy violation"""
    severity: str  # 'error', 'warning', 'info'
    rule_id: str
    message: str
    line_number: Optional[int]
    suggestion_id: str
    auto_fixable: bool
    fix: Optional[str]

class PolicyRule(ABC):
    """Abstract base for all policy rules"""
    
    @abstractmethod
    def check(self, suggestion: CodeSuggestion) -> List[PolicyViolation]:
        pass
    
    @abstractmethod
    def fix(self, suggestion: CodeSuggestion, violation: PolicyViolation) -> str:
        pass

class SecurityPolicyRule(PolicyRule):
    """Detects security vulnerabilities in AI suggestions"""
    
    def __init__(self):
        # This is where your patent magic happens
        self.patterns = {
            'sql_injection': {
                'pattern': r'(SELECT|INSERT|UPDATE|DELETE).*\+',
                'message': 'Potential SQL injection vulnerability',
                'severity': 'error'
            },
            'hardcoded_secrets': {
                'pattern': r'(password|api_key|secret|token)\s*=\s*["\'][^"\']+["\']',
                'message': 'Hardcoded secrets detected',
                'severity': 'error'
            },
            'unsafe_eval': {
                'pattern': r'eval\s*\(',
                'message': 'Unsafe eval() usage',
                'severity': 'error'
            }
        }
    
    def check(self, suggestion: CodeSuggestion) -> List[PolicyViolation]:
        violations = []
        
        # Patent claim: Multi-pass semantic analysis
        for rule_id, rule in self.patterns.items():
            if re.search(rule['pattern'], suggestion.content, re.IGNORECASE):
                violations.append(PolicyViolation(
                    severity=rule['severity'],
                    rule_id=rule_id,
                    message=rule['message'],
                    line_number=None,  # TODO: Calculate line
                    suggestion_id=suggestion.id,
                    auto_fixable=True,
                    fix=self._generate_fix(suggestion, rule_id)
                ))
        
        return violations
    
    def fix(self, suggestion: CodeSuggestion, violation: PolicyViolation) -> str:
        # Your proprietary fix logic
        return self._generate_fix(suggestion, violation.rule_id)
    
    def _generate_fix(self, suggestion: CodeSuggestion, rule_id: str) -> str:
        # Simplified for demo - real version would be sophisticated
        if rule_id == 'sql_injection':
            return "# Use parameterized queries instead"
        elif rule_id == 'hardcoded_secrets':
            return "# Use environment variables: os.getenv('SECRET_KEY')"
        return "# Security fix required"

class CompliancePolicyRule(PolicyRule):
    """Ensures code meets compliance standards (GDPR, SOC2, etc.)"""
    
    def check(self, suggestion: CodeSuggestion) -> List[PolicyViolation]:
        violations = []
        
        # Patent claim: Compliance-aware code analysis
        if 'user_data' in suggestion.content.lower():
            if 'log' in suggestion.content.lower() or 'print' in suggestion.content.lower():
                violations.append(PolicyViolation(
                    severity='warning',
                    rule_id='gdpr_logging',
                    message='Potential GDPR violation: logging user data',
                    line_number=None,
                    suggestion_id=suggestion.id,
                    auto_fixable=True,
                    fix="# Ensure PII is masked before logging"
                ))
        
        return violations
    
    def fix(self, suggestion: CodeSuggestion, violation: PolicyViolation) -> str:
        # Compliance-specific fixes
        return "# Add PII masking before processing"

class PolicyEngine:
    """
    Core PolicyGuard Engine
    This is your main patent: Real-time policy enforcement for AI code generation
    """
    
    def __init__(self):
        self.rules: List[PolicyRule] = []
        self.cache = {}  # Performance optimization
        self.metrics = {
            'suggestions_processed': 0,
            'violations_found': 0,
            'auto_fixes_applied': 0,
            'avg_latency_ms': 0
        }
    
    def add_rule(self, rule: PolicyRule):
        """Register a new policy rule"""
        self.rules.append(rule)
    
    def process_suggestion(
        self, 
        suggestion: CodeSuggestion, 
        auto_fix: bool = True
    ) -> Tuple[CodeSuggestion, List[PolicyViolation]]:
        """
        Patent claim: Process AI suggestion through policy engine
        Returns: (possibly modified suggestion, violations found)
        """
        start_time = time.time()
        
        # Check cache first (performance optimization)
        cache_key = hashlib.md5(suggestion.content.encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        all_violations = []
        current_content = suggestion.content
        
        # Multi-pass rule checking (patent claim)
        for rule in self.rules:
            violations = rule.check(suggestion)
            all_violations.extend(violations)
            
            # Auto-fix if enabled and possible
            if auto_fix:
                for violation in violations:
                    if violation.auto_fixable:
                        current_content = self._apply_fix(
                            current_content, 
                            violation, 
                            rule
                        )
                        self.metrics['auto_fixes_applied'] += 1
        
        # Create modified suggestion if needed
        modified_suggestion = CodeSuggestion(
            id=suggestion.id,
            content=current_content,
            language=suggestion.language,
            context=suggestion.context,
            source=suggestion.source,
            timestamp=suggestion.timestamp
        ) if current_content != suggestion.content else suggestion
        
        # Update metrics
        self.metrics['suggestions_processed'] += 1
        self.metrics['violations_found'] += len(all_violations)
        
        latency_ms = (time.time() - start_time) * 1000
        if self.metrics['suggestions_processed'] == 1:
            self.metrics['avg_latency_ms'] = latency_ms
        else:
            self.metrics['avg_latency_ms'] = (
                (self.metrics['avg_latency_ms'] * (self.metrics['suggestions_processed'] - 1) + latency_ms) 
                / self.metrics['suggestions_processed']
            )
        
        # Cache result
        result = (modified_suggestion, all_violations)
        self.cache[cache_key] = result
        
        return result
    
    def _apply_fix(self, content: str, violation: PolicyViolation, rule: PolicyRule) -> str:
        """Apply automatic fix to content"""
        # Simplified for demo - real version would be AST-based
        return f"{content}\n{violation.fix}"
    
    def get_metrics(self) -> Dict:
        """Return performance metrics"""
        return self.metrics.copy()