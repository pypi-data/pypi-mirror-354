"""Security rules for PolicyGuard"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Rule:
    """Represents a security rule"""
    id: str
    pattern: Optional[str]  # Regex pattern
    message: str
    severity: str  # 'error' or 'warning'
    confidence: float = 0.8
    category: str = 'security'


def get_default_rules() -> List[Rule]:
    """Get default security rules"""
    return [
        # Security rules
        Rule(
            id='hardcoded_password',
            pattern=r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']',
            message='Hardcoded password detected',
            severity='error',
            confidence=0.9
        ),
        Rule(
            id='hardcoded_secret',
            pattern=r'(?i)(secret|api_key|apikey|token|auth)\s*=\s*["\'][^"\']{8,}["\']',
            message='Hardcoded secret/API key detected',
            severity='error',
            confidence=0.8
        ),
        Rule(
            id='sql_injection',
            pattern=r'(execute|cursor\.execute)\s*\([^)]*(%s|\.format\(|f["\'][^"\']*{)',
            message='Possible SQL injection - use parameterized queries',
            severity='error',
            confidence=0.7
        ),
        Rule(
            id='eval_usage',
            pattern=r'\beval\s*\([^)]+\)',
            message='Dangerous eval() usage - arbitrary code execution risk',
            severity='error',
            confidence=0.95
        ),
        Rule(
            id='exec_usage',
            pattern=r'\bexec\s*\([^)]+\)',
            message='Dangerous exec() usage - arbitrary code execution risk',
            severity='error',
            confidence=0.95
        ),
        Rule(
            id='pickle_load',
            pattern=r'pickle\.(load|loads)\s*\(',
            message='Unsafe pickle usage - arbitrary code execution risk',
            severity='error',
            confidence=0.9
        ),
        Rule(
            id='weak_random',
            pattern=r'\brandom\.(random|randint|choice|randbytes)\s*\(',
            message='Weak randomness for security - use secrets module',
            severity='warning',
            confidence=0.6
        ),
        Rule(
            id='md5_usage',
            pattern=r'hashlib\.md5\s*\(',
            message='MD5 is cryptographically broken - use SHA256',
            severity='warning',
            confidence=0.8
        ),
        Rule(
            id='subprocess_shell',
            pattern=r'subprocess\.[^(]*\([^)]*shell\s*=\s*True',
            message='Shell injection risk with subprocess',
            severity='error',
            confidence=0.8
        ),
        
        # AI-specific patterns
        Rule(
            id='todo_security',
            pattern=r'#\s*TODO:?\s*(change|update|fix)\s+(password|secret|key|token)',
            message='AI-generated TODO for secrets - fix before committing',
            severity='error',
            confidence=0.95,
            category='ai-pattern'
        ),
        Rule(
            id='example_key',
            pattern=r'["\']sk-[a-zA-Z0-9]{48}["\']|["\']AKIA[A-Z0-9]{16}["\']|["\']ghp_[a-zA-Z0-9]{36}["\']',
            message='Example API key detected (common in AI code)',
            severity='error',
            confidence=0.9,
            category='ai-pattern'
        ),
        Rule(
            id='localhost_prod',
            pattern=r'["\']https?://localhost["\']|["\']127\.0\.0\.1["\']',
            message='Localhost URL in code (often AI-generated placeholder)',
            severity='warning',
            confidence=0.5,
            category='ai-pattern'
        ),
    ]
