"""Git hook installation for PolicyGuard"""

import sys
from pathlib import Path


def install_pre_commit_hook() -> bool:
    """Install pre-commit hook in current repository"""
    git_dir = Path('.git')
    if not git_dir.exists():
        print("Error: Not a git repository", file=sys.stderr)
        return False
    
    hooks_dir = git_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)
    
    pre_commit = hooks_dir / 'pre-commit'
    
    hook_content = '''#!/bin/bash
# PolicyGuard Pre-commit Hook
# Auto-generated - do not edit

echo "🛡️  PolicyGuard: Scanning for security issues..."

# Run PolicyGuard on staged files
policyguard scan --staged

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ PolicyGuard found security issues. Fix them before committing."
    echo "💡 To bypass (not recommended): git commit --no-verify"
    exit 1
fi

echo "✅ PolicyGuard: No security issues found"
exit 0
'''
    
    pre_commit.write_text(hook_content)
    pre_commit.chmod(0o755)
    
    return True
