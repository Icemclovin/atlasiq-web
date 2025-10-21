"""
Create test account directly using the backend code
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import AsyncSessionLocal, init_db
from app.models.user import User
from app.auth.security import get_password_hash
from sqlalchemy import select


async def create_test_account():
    """Create test account"""
    # Initialize database first
    print("Initializing database...")
    await init_db()
    
    async with AsyncSessionLocal() as db:
        try:
            # Check if user exists
            result = await db.execute(
                select(User).where(User.email == "dev@atlasiq.com")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("✅ Account already exists!")
                print(f"   Email: {existing_user.email}")
                print(f"   Name: {existing_user.full_name}")
                print(f"   Created: {existing_user.created_at}")
                return
            
            # Create new user
            print("Creating account...")
            new_user = User(
                email="dev@atlasiq.com",
                hashed_password=get_password_hash("developer123"),
                full_name="Developer Account",
                organization="AtlasIQ",
                is_active=True,
                is_admin=False,
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            print("✅ SUCCESS! Account created:")
            print(f"   Email: dev@atlasiq.com")
            print(f"   Password: developer123")
            print(f"   ID: {new_user.id}")
            print(f"   Created: {new_user.created_at}")
            print("")
            print("You can now login at http://localhost:3000")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(create_test_account())
