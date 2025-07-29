# Changelog

All notable changes to PolicyGuard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release
- Core security rules for Python code
- AI-specific pattern detection
- Git pre-commit hook integration
- Beautiful CLI output with color coding
- JSON output format
- Configurable rules system

### Security Rules
- Hardcoded passwords and secrets detection
- SQL injection vulnerability detection
- Dangerous function usage (eval, exec, pickle)
- Weak randomness detection
- Subprocess shell injection detection
- AI-generated TODO patterns
- Example API key detection

[0.1.0]: https://github.com/yourusername/policyguard/releases/tag/v0.1.0
