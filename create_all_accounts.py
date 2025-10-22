"""
Create multiple test accounts directly in SQLite database
"""
import sqlite3
import bcrypt
from datetime import datetime

# Database path
db_path = "backend/atlasiq.db"

# Test accounts to create
accounts = [
    {
        "email": "dev@atlasiq.com",
        "password": "developer123",
        "full_name": "Developer Account",
        "organization": "AtlasIQ",
        "is_admin": False
    },
    {
        "email": "test@atlasiq.com",
        "password": "testpass123",
        "full_name": "Test User",
        "organization": "AtlasIQ",
        "is_admin": False
    },
    {
        "email": "admin@atlasiq.com",
        "password": "admin123456",
        "full_name": "Admin Account",
        "organization": "AtlasIQ",
        "is_admin": True
    }
]

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
    
    print("=" * 60)
    print("Creating Test Accounts")
    print("=" * 60)
    
    created_count = 0
    existing_count = 0
    
    for account in accounts:
        email = account["email"]
        password = account["password"]
        full_name = account["full_name"]
        organization = account["organization"]
        is_admin = account["is_admin"]
        
        # Check if user exists
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"\n✓ Account already exists: {email}")
            existing_count += 1
        else:
            # Hash the password using bcrypt
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
            
            # Insert new user
            now = datetime.utcnow().isoformat()
            cursor.execute('''
            INSERT INTO users (email, hashed_password, full_name, organization, is_active, is_admin, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, hashed_password, full_name, organization, True, is_admin, now, now))
            
            print(f"\n✅ Created: {email}")
            print(f"   Password: {password}")
            print(f"   Name: {full_name}")
            print(f"   Admin: {'Yes' if is_admin else 'No'}")
            created_count += 1
    
    conn.commit()
    
    print("\n" + "=" * 60)
    print(f"Summary: {created_count} created, {existing_count} already existed")
    print("=" * 60)
    
    # Show all users
    cursor.execute("SELECT id, email, full_name, is_active, is_admin, created_at FROM users")
    users = cursor.fetchall()
    
    print(f"\n📋 All Users in Database ({len(users)} total):")
    print("-" * 60)
    for user in users:
        admin_badge = "👑 ADMIN" if user[4] else "👤 USER"
        active_badge = "✓" if user[3] else "✗"
        print(f"{admin_badge} [{active_badge}] {user[1]}")
        print(f"         Name: {user[2]}")
        print(f"         Created: {user[5][:10]}")
        print()
    
    print("=" * 60)
    print("🔐 Login Credentials")
    print("=" * 60)
    for account in accounts:
        print(f"\nEmail:    {account['email']}")
        print(f"Password: {account['password']}")
        print(f"Role:     {'Admin' if account['is_admin'] else 'User'}")
    
    print("\n" + "=" * 60)
    print("🚀 Ready to login at http://localhost:3000")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
