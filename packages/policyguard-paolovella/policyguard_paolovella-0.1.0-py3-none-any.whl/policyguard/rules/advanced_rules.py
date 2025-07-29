# policyguard/rules/advanced_rules.py
"""
Advanced policy rules for enterprise compliance
Patent pending: Domain-specific code governance
"""

from typing import List
import re
from ..core.engine import PolicyRule, PolicyViolation, CodeSuggestion

class ArchitectureComplianceRule(PolicyRule):
    """Ensures code follows company architecture patterns"""
    
    def __init__(self, config: dict = None):
        self.config = config or {
            'banned_imports': ['requests', 'urllib'],  # Force using company HTTP client
            'required_decorators': {
                'api_endpoint': ['@rate_limit', '@authenticate'],
                'database_query': ['@trace', '@retry'],
            },
            'naming_conventions': {
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'function': r'^[a-z_][a-z0-9_]*$',
                'constant': r'^[A-Z][A-Z0-9_]*$',
            }
        }
    
    def check(self, suggestion: CodeSuggestion) -> List[PolicyViolation]:
        violations = []
        
        # Check for banned imports
        for banned in self.config['banned_imports']:
            if f'import {banned}' in suggestion.content or f'from {banned}' in suggestion.content:
                violations.append(PolicyViolation(
                    severity='error',
                    rule_id='banned_import',
                    message=f'Use of banned import: {banned}. Use company HTTP client instead.',
                    line_number=None,
                    suggestion_id=suggestion.id,
                    auto_fixable=True,
                    fix=f'from company.http import HTTPClient  # Use instead of {banned}'
                ))
        
        return violations
    
    def fix(self, suggestion: CodeSuggestion, violation: PolicyViolation) -> str:
        # Implement architecture-specific fixes
        pass

class PerformanceRule(PolicyRule):
    """Detects potential performance issues"""
    
    def check(self, suggestion: CodeSuggestion) -> List[PolicyViolation]:
        violations = []
        
        # N+1 query detection
        if 'for ' in suggestion.content and '.objects.get(' in suggestion.content:
            violations.append(PolicyViolation(
                severity='warning',
                rule_id='n_plus_one_query',
                message='Potential N+1 query detected. Use select_related() or prefetch_related()',
                line_number=None,
                suggestion_id=suggestion.id,
                auto_fixable=True,
                fix='# Use .select_related() or .prefetch_related() to avoid N+1 queries'
            ))
        
        # Synchronous I/O in async context
        if 'async def' in suggestion.content and 'time.sleep(' in suggestion.content:
            violations.append(PolicyViolation(
                severity='error',
                rule_id='sync_in_async',
                message='Synchronous sleep in async function. Use asyncio.sleep()',
                line_number=None,
                suggestion_id=suggestion.id,
                auto_fixable=True,
                fix=None
            ))
        
        return violations
    
    def fix(self, suggestion: CodeSuggestion, violation: PolicyViolation) -> str:
        if violation.rule_id == 'sync_in_async':
            return suggestion.content.replace('time.sleep(', 'await asyncio.sleep(')
        return suggestion.content

class CostOptimizationRule(PolicyRule):
    """Prevents expensive cloud operations"""
    
    def check(self, suggestion: CodeSuggestion) -> List[PolicyViolation]:
        violations = []
        
        # Detect full table scans
        if '.scan()' in suggestion.content and 'dynamodb' in suggestion.content.lower():
            violations.append(PolicyViolation(
                severity='error',
                rule_id='expensive_scan',
                message='DynamoDB scan operations are expensive. Use query() with indexes.',
                line_number=None,
                suggestion_id=suggestion.id,
                auto_fixable=False,
                fix=None
            ))
        
        # Detect missing pagination
        if 'list(' in suggestion.content and 'limit=' not in suggestion.content:
            violations.append(PolicyViolation(
                severity='warning',
                rule_id='missing_pagination',
                message='Large list operations should use pagination',
                line_number=None,
                suggestion_id=suggestion.id,
                auto_fixable=True,
                fix='# Add pagination: .list(limit=100, offset=0)'
            ))
        
        return violations
    
    def fix(self, suggestion: CodeSuggestion, violation: PolicyViolation) -> str:
        # Implement cost-specific fixes
        pass