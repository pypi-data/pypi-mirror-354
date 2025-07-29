# policyguard/core/transformers.py
"""
Code transformation engine for auto-fixing violations
This is the REAL patent - automated secure code transformation
"""

import ast
import re
from typing import Dict, List, Tuple, Optional

class CodeTransformer:
    """Transforms unsafe code into secure alternatives"""
    
    @staticmethod
    def fix_sql_injection(code: str) -> str:
        """Transform string concatenation to parameterized queries"""
        lines = code.split('\n')
        transformed_lines = []
        
        for line in lines:
            # Pattern: query = "SELECT ... " + variable
            if 'query = ' in line and ' + ' in line:
                # Extract the SQL and variable parts
                match = re.search(r'query\s*=\s*"([^"]+)"\s*\+\s*(\w+)', line)
                if match:
                    sql_part = match.group(1).rstrip()
                    var_name = match.group(2)
                    indent = len(line) - len(line.lstrip())
                    
                    # Replace with parameterized query
                    new_line = f"{' ' * indent}query = \"{sql_part}%s\""
                    transformed_lines.append(new_line)
                    
                    # Add the parameters line
                    params_line = f"{' ' * indent}params = ({var_name},)"
                    transformed_lines.append(params_line)
                    
                    # Update any execute_query calls
                    continue
            
            # Update execute_query to use params
            if 'execute_query(query)' in line:
                line = line.replace('execute_query(query)', 'execute_query(query, params)')
            
            transformed_lines.append(line)
        
        return '\n'.join(transformed_lines)
    
    @staticmethod
    def fix_hardcoded_secrets(code: str) -> str:
        """Replace hardcoded secrets with environment variables"""
        import_added = False
        lines = code.split('\n')
        transformed_lines = []
        
        # Patterns for different types of secrets
        secret_patterns = [
            (r'password\s*=\s*["\']([^"\']+)["\']', 'DB_PASSWORD'),
            (r'api_key\s*=\s*["\']([^"\']+)["\']', 'API_KEY'),
            (r'secret\s*=\s*["\']([^"\']+)["\']', 'SECRET_KEY'),
            (r'token\s*=\s*["\']([^"\']+)["\']', 'AUTH_TOKEN'),
        ]
        
        for line in lines:
            transformed_line = line
            
            for pattern, env_var in secret_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    # Get the indentation
                    indent = len(line) - len(line.lstrip())
                    var_name = line.split('=')[0].strip()
                    
                    # Replace with environment variable
                    transformed_line = f"{' ' * indent}{var_name} = os.getenv('{env_var}')"
                    
                    # Add import if needed
                    if not import_added:
                        import_added = True
                        transformed_lines.insert(0, 'import os\n')
                    break
            
            transformed_lines.append(transformed_line)
        
        return '\n'.join(transformed_lines)
    
    @staticmethod
    def fix_gdpr_logging(code: str) -> str:
        """Add PII masking to user data logging"""
        lines = code.split('\n')
        transformed_lines = []
        mask_function_added = False
        
        for line in lines:
            # Check for print/log statements with user_data
            if ('print' in line or 'log' in line) and 'user_data' in line:
                # Add mask_pii wrapper
                line = re.sub(
                    r'(print|log|logger\.\w+)\s*\(([^)]+user_data[^)]+)\)',
                    r'\1(mask_pii(\2))',
                    line
                )
                
                # Add the mask function if not already added
                if not mask_function_added:
                    mask_function_added = True
                    # Insert at the beginning after imports
                    mask_func = '''
def mask_pii(data):
    """Mask personally identifiable information"""
    if isinstance(data, str):
        # Mask email addresses
        data = re.sub(r'[\w\.-]+@[\w\.-]+', '***@***.***', data)
        # Mask phone numbers
        data = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '***-***-****', data)
    elif isinstance(data, dict):
        sensitive_keys = ['email', 'phone', 'ssn', 'password', 'credit_card']
        return {k: '***REDACTED***' if k in sensitive_keys else v for k, v in data.items()}
    return data
'''
                    # Find where to insert (after imports)
                    import_end = 0
                    for i, l in enumerate(transformed_lines):
                        if l.strip() and not l.startswith('import') and not l.startswith('from'):
                            import_end = i
                            break
                    
                    # Add import re if needed
                    if not any('import re' in l for l in transformed_lines[:import_end]):
                        transformed_lines.insert(import_end, 'import re')
                        import_end += 1
                    
                    transformed_lines.insert(import_end, mask_func)
            
            transformed_lines.append(line)
        
        return '\n'.join(transformed_lines)