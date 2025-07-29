"""Example vulnerable code for testing"""

# Various security issues that should be caught

def connect_db():
    # TODO: change password before production
    password = "admin123"
    api_key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
    
    conn_string = f"postgres://admin:{password}@localhost/db"
    return conn_string

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)  # SQL injection!
    
def check_auth(token):
    # This is insecure
    return eval(f"validate_{token}()")
    
def generate_session():
    import random
    return random.randint(1000, 9999)  # Weak randomness

# Subprocess with shell=True
import subprocess
subprocess.run(f"echo {user_input}", shell=True)
