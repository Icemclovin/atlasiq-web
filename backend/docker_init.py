#!/usr/bin/env python3
"""
Docker initialization script
Creates database tables and initial admin account
"""
import asyncio
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

import bcrypt
from sqlalchemy import select
from app.database import engine, AsyncSessionLocal, Base
from app.models.user import User


async def init_database():
    """Initialize database tables"""
    print("🔧 Checking database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables ready")
    except Exception as e:
        # If tables already exist, that's fine
        if "already exists" in str(e):
            print("✅ Database tables already exist")
        else:
            raise


async def create_admin_account():
    """Create initial admin account if it doesn't exist"""
    admin_email = os.getenv("ADMIN_EMAIL", "admin@atlasiq.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_name = os.getenv("ADMIN_NAME", "Administrator")
    
    async with AsyncSessionLocal() as session:
        # Check if admin exists
        result = await session.execute(
            select(User).where(User.email == admin_email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"ℹ️  Admin account already exists: {admin_email}")
            return
        
        # Create admin account
        print(f"👤 Creating admin account: {admin_email}")
        hashed_password = bcrypt.hashpw(
            admin_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        admin_user = User(
            email=admin_email,
            hashed_password=hashed_password,
            full_name=admin_name,
            organization="AtlasIQ",
            is_active=True,
            is_admin=True
        )
        
        session.add(admin_user)
        await session.commit()
        
        print("✅ Admin account created successfully")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print("   ⚠️  Please change the password after first login!")


async def main():
    """Main initialization function"""
    print("🚀 Initializing AtlasIQ Docker Environment")
    print("=" * 50)
    
    try:
        await init_database()
        await create_admin_account()
        print("=" * 50)
        print("✅ Initialization complete!")
        return 0
    except Exception as e:
        # If it's just a "already exists" error, don't fail - it's OK
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            print("ℹ️  Database already initialized, continuing...")
            print("=" * 50)
            print("✅ Initialization complete!")
            return 0
        else:
            print(f"❌ Initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return 1


if __name__ == "__main__":
    # Run the main function but DON'T call sys.exit()
    # This allows the Dockerfile CMD to continue to the next command
    exit_code = asyncio.run(main())
    if exit_code != 0:
        print(f"⚠️  Initialization returned exit code: {exit_code}")
        print("⚠️  Continuing to start server anyway...")
    # Don't call sys.exit() - let the shell continue to uvicorn
