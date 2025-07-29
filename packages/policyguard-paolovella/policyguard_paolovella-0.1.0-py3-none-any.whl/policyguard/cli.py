"""Command-line interface for PolicyGuard"""

import sys
import json
import subprocess
from pathlib import Path
from collections import defaultdict

import click

from policyguard.scanner import SecurityScanner
from policyguard.hooks import install_pre_commit_hook

# ANSI color codes
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


@click.group()
@click.version_option()
def cli():
    """PolicyGuard - Stop committing AI-generated security vulnerabilities"""
    pass


@cli.command()
def init():
    """Install pre-commit hook in current repository"""
    if install_pre_commit_hook():
        click.echo(f"{GREEN}✅ PolicyGuard pre-commit hook installed{RESET}")
        click.echo(f"🔒 Your commits are now protected against security issues")
    else:
        click.echo(f"{RED}❌ Failed to install pre-commit hook{RESET}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', required=False, type=click.Path(exists=True))
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.option('--staged', is_flag=True, help='Only scan staged files')
@click.option('--exit-zero', is_flag=True, help='Always exit with code 0')
def scan(path, output_json, staged, exit_zero):
    """Scan Python files for security issues"""
    scanner = SecurityScanner()
    
    if staged:
        # Get staged files from git
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                capture_output=True, text=True, check=True
            )
            files = [Path(f) for f in result.stdout.strip().split('\n') if f.endswith('.py')]
            violations = []
            for file in files:
                if file.exists():
                    violations.extend(scanner.scan_file(file))
        except subprocess.CalledProcessError:
            click.echo(f"{RED}Error: Not in a git repository{RESET}", err=True)
            sys.exit(1)
    elif path:
        path_obj = Path(path)
        if path_obj.is_file():
            violations = scanner.scan_file(path_obj)
        else:
            violations = scanner.scan_directory(path_obj)
    else:
        violations = scanner.scan_directory(Path.cwd())
    
    if output_json:
        # JSON output
        output = [
            {
                'file': v.file,
                'line': v.line,
                'rule': v.rule,
                'message': v.message,
                'severity': v.severity,
                'confidence': v.confidence
            }
            for v in violations
        ]
        click.echo(json.dumps(output, indent=2))
    else:
        # Human-readable output
        if not violations:
            click.echo(f"{GREEN}✅ No security issues found{RESET}")
            return
        
        click.echo(f"\n{RED}{BOLD}🚨 Security Issues Found:{RESET}\n")
        
        # Group by file
        by_file = defaultdict(list)
        for v in violations:
            by_file[v.file].append(v)
        
        for file, file_violations in by_file.items():
            click.echo(f"{BLUE}{BOLD}📄 {file}{RESET}")
            
            for v in sorted(file_violations, key=lambda x: x.line):
                icon = "🔴" if v.severity == 'error' else "🟡"
                click.echo(f"  {icon} Line {v.line}: {BOLD}{v.message}{RESET}")
                click.echo(f"     Rule: {v.rule} (confidence: {v.confidence:.0%})")
                if v.code_snippet:
                    click.echo(f"     Code:")
                    for line in v.code_snippet.split('\n'):
                        click.echo(f"       {line}")
                click.echo()
        
        # Summary
        errors = sum(1 for v in violations if v.severity == 'error')
        warnings = sum(1 for v in violations if v.severity == 'warning')
        
        click.echo(f"{BOLD}Summary:{RESET} {RED}{errors} errors{RESET}, {YELLOW}{warnings} warnings{RESET}")
    
    if not exit_zero and violations:
        sys.exit(1 if any(v.severity == 'error' for v in violations) else 0)


@cli.command()
def rules():
    """List all available security rules"""
    from policyguard.rules import get_default_rules
    
    rules = get_default_rules()
    
    click.echo(f"\n{BOLD}📋 PolicyGuard Security Rules:{RESET}\n")
    
    # Group by category
    by_category = defaultdict(list)
    for rule in rules:
        by_category[rule.category].append(rule)
    
    for category, category_rules in by_category.items():
        click.echo(f"{BLUE}{category.replace('-', ' ').title()}:{RESET}")
        for rule in category_rules:
            severity_color = RED if rule.severity == 'error' else YELLOW
            click.echo(f"  • {rule.id}: {rule.message} [{severity_color}{rule.severity}{RESET}]")
        click.echo()


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
