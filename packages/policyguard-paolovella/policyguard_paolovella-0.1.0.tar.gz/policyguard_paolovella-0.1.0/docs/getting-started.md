# Getting Started with PolicyGuard

## Installation

```bash
pip install policyguard
```

## Quick Setup

1. Navigate to your Python project:
```bash
cd my-python-project
```

2. Initialize PolicyGuard:
```bash
policyguard init
```

3. Try to commit some vulnerable code:
```python
# test.py
password = "admin123"  # This will be caught!
```

4. PolicyGuard will block the commit and show you what to fix.

## Manual Scanning

You can also scan files manually:

```bash
# Scan entire project
policyguard scan

# Scan specific file
policyguard scan src/auth.py

# Get JSON output
policyguard scan --json > report.json
```

## Configuration

Create `.policyguard.yml` in your project root:

```yaml
# Ignore specific rules
ignore:
  - weak_random

# Add custom patterns
custom_rules:
  - id: internal_api
    pattern: 'internal_api_key\s*='
    message: "Don't hardcode internal API keys"
    severity: error
```
