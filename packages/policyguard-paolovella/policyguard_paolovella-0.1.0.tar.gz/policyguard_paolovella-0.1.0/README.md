<div align="center">

# 🛡️ PolicyGuard

**Pre-commit security scanner for AI-generated Python code**

[![PyPI](https://img.shields.io/pypi/v/policyguard)](https://pypi.org/project/policyguard/)
[![Python](https://img.shields.io/pypi/pyversions/policyguard)](https://pypi.org/project/policyguard/)
[![License](https://img.shields.io/github/license/yourusername/policyguard)](LICENSE)
[![Tests](https://github.com/yourusername/policyguard/workflows/Tests/badge.svg)](https://github.com/yourusername/policyguard/actions)

</div>

---

PolicyGuard catches common security vulnerabilities in your Python code, especially those often introduced by AI coding assistants like GitHub Copilot.

## ✨ Features

- 🚨 **Detects hardcoded secrets** - passwords, API keys, tokens
- 💉 **Prevents SQL injection** - finds string concatenation in queries  
- 🎯 **Catches dangerous functions** - eval(), exec(), pickle.load()
- 🤖 **AI-specific patterns** - TODOs for passwords, example keys
- ⚡ **Fast** - typically <100ms per file
- 🎨 **Beautiful output** - color-coded, with context
- 🔧 **Git pre-commit hook** - catch issues before they're committed
- 📦 **Zero dependencies** - minimal requirements

## 🚀 Quick Start

### Install

```bash
pip install policyguard
```

### Initialize in your repo

```bash
cd your-python-project
policyguard init
```

### That's it! 

PolicyGuard will now check your Python files before each commit.

## 📋 What It Catches

### Security Issues
- Hardcoded passwords and secrets
- SQL injection vulnerabilities
- Command injection risks
- Insecure deserialization (pickle)
- Weak random number generation
- Dangerous eval/exec usage

### AI-Specific Patterns
- `# TODO: change password` comments
- Example API keys (sk-xxx, AKIA-xxx)
- Placeholder emails (test@test.com)
- Localhost URLs in production code

## 🔧 Usage

### Scan manually

```bash
# Scan current directory
policyguard scan

# Scan specific file
policyguard scan auth.py

# Output as JSON
policyguard scan --json
```

### View all rules

```bash
policyguard rules
```

## 🤝 Contributing

We love contributions! Please see our contributing guidelines.

## 📄 License

MIT - see [LICENSE](LICENSE)

---

<div align="center">

**Built with ❤️ to keep AI-generated code secure**

</div>
