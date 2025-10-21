"""
Create test account directly in SQLite database
This bypasses the API to ensure account creation works
"""
import sqlite3
import bcrypt
from datetime import datetime

# Database path
db_path = "backend/atlasiq.db"

# Account details
email = "dev@atlasiq.com"
password = "developer123"
full_name = "Developer Account"
organization = "AtlasIQ"

# Hash the password using bcrypt directly
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

# Create/connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255),
        organization VARCHAR(255),
        is_active BOOLEAN NOT NULL DEFAULT 1,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        last_login_at DATETIME
    )
    ''')
    
    # Check if user exists
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    
    if existing:
        print("✅ Account already exists!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
    else:
        # Insert new user
        now = datetime.utcnow().isoformat()
        cursor.execute('''
        INSERT INTO users (email, hashed_password, full_name, organization, is_active, is_admin, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, hashed_password, full_name, organization, True, False, now, now))
        
        conn.commit()
        
        print("✅ SUCCESS! Account created in database:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Database: {db_path}")
        print("")
        print("You can now login at http://localhost:3000")
    
    # Show all users
    cursor.execute("SELECT id, email, full_name, is_active, created_at FROM users")
    users = cursor.fetchall()
    print(f"\nTotal users in database: {len(users)}")
    for user in users:
        print(f"  - {user[1]} ({user[2]}) - Active: {user[3]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
