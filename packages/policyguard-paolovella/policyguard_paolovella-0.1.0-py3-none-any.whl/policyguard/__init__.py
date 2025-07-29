"""PolicyGuard - Stop committing AI-generated security vulnerabilities"""

from policyguard.__version__ import __version__
from policyguard.scanner import SecurityScanner, Violation
from policyguard.rules import Rule, get_default_rules

__all__ = ['SecurityScanner', 'Violation', 'Rule', 'get_default_rules', '__version__']
