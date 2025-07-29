"""Tests for PolicyGuard scanner"""

import pytest
from pathlib import Path
from policyguard.scanner import SecurityScanner, Violation


def test_detects_hardcoded_password(tmp_path):
    """Test detection of hardcoded passwords"""
    scanner = SecurityScanner()
    
    code = '''
def connect():
    password = "admin123"
    return password
'''
    
    test_file = tmp_path / "test.py"
    test_file.write_text(code)
    
    violations = scanner.scan_file(test_file)
    
    assert len(violations) == 1
    assert violations[0].rule == 'hardcoded_password'
    assert violations[0].line == 3
    assert violations[0].severity == 'error'


def test_detects_sql_injection(tmp_path):
    """Test detection of SQL injection vulnerabilities"""
    scanner = SecurityScanner()
    
    code = '''
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
'''
    
    test_file = tmp_path / "test.py"
    test_file.write_text(code)
    
    violations = scanner.scan_file(test_file)
    
    assert any(v.rule == 'sql_injection' for v in violations)


def test_no_false_positives(tmp_path):
    """Test that safe code doesn't trigger violations"""
    scanner = SecurityScanner()
    
    safe_code = '''
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    
    # This is not a hardcoded password
    password_param = get_from_env("PASSWORD")
'''
    
    test_file = tmp_path / "test.py"
    test_file.write_text(safe_code)
    
    violations = scanner.scan_file(test_file)
    
    assert len(violations) == 0


def test_ai_pattern_detection(tmp_path):
    """Test detection of AI-specific patterns"""
    scanner = SecurityScanner()
    
    code = '''
def connect():
    # TODO: change password before production
    password = "temp123"
    api_key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
'''
    
    test_file = tmp_path / "test.py"
    test_file.write_text(code)
    
    violations = scanner.scan_file(test_file)
    
    assert any(v.rule == 'todo_security' for v in violations)
    assert any(v.rule == 'example_key' for v in violations)
