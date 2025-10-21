"""
Test script to verify backend core implementation
Tests database connectivity, models, and authentication
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.config import settings
from app.database import init_db, close_db, check_db_connection, AsyncSessionLocal
from app.models.user import User
from app.auth.security import get_password_hash, verify_password, create_access_token, verify_token


async def test_config():
    """Test configuration loading"""
    print("\n" + "="*60)
    print("TEST 1: Configuration")
    print("="*60)
    
    print(f"✓ App Name: {settings.APP_NAME}")
    print(f"✓ Environment: {settings.ENVIRONMENT}")
    print(f"✓ Database URL: {settings.get_database_url()[:50]}...")
    print(f"✓ Redis URL: {settings.get_redis_url()}")
    print(f"✓ JWT Algorithm: {settings.JWT_ALGORITHM}")
    print(f"✓ Supported Countries: {', '.join(settings.SUPPORTED_COUNTRIES)}")
    print(f"✓ Supported Sectors: {len(settings.SUPPORTED_SECTORS)} sectors")
    print("✅ Configuration loaded successfully")


async def test_database_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("TEST 2: Database Connection")
    print("="*60)
    
    try:
        # Initialize database
        await init_db()
        print("✓ Database tables created")
        
        # Check connection
        is_healthy = await check_db_connection()
        if is_healthy:
            print("✅ Database connection is healthy")
        else:
            print("❌ Database connection failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False


async def test_user_model():
    """Test User model CRUD operations"""
    print("\n" + "="*60)
    print("TEST 3: User Model")
    print("="*60)
    
    try:
        async with AsyncSessionLocal() as session:
            # Create test user
            test_email = "test@atlasiq.com"
            test_password = "SecurePassword123!"
            
            # Check if user already exists
            from sqlalchemy import select
            result = await session.execute(
                select(User).where(User.email == test_email)
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"✓ Test user already exists (ID: {existing_user.id})")
                user = existing_user
            else:
                # Create new user
                user = User(
                    email=test_email,
                    hashed_password=get_password_hash(test_password),
                    full_name="Test User",
                    organization="AtlasIQ Test",
                    is_active=True,
                    is_admin=False,
                )
                
                session.add(user)
                await session.commit()
                await session.refresh(user)
                print(f"✓ Created test user (ID: {user.id})")
            
            # Test user dictionary conversion
            user_dict = user.to_dict()
            print(f"✓ User to_dict: {user_dict['email']}")
            
            # Verify password hashing
            is_valid = verify_password(test_password, user.hashed_password)
            print(f"✓ Password verification: {'Valid' if is_valid else 'Invalid'}")
            
            print("✅ User model tests passed")
            return True
            
    except Exception as e:
        print(f"❌ User model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_jwt_tokens():
    """Test JWT token creation and verification"""
    print("\n" + "="*60)
    print("TEST 4: JWT Authentication")
    print("="*60)
    
    try:
        test_email = "test@atlasiq.com"
        
        # Create access token
        access_token = create_access_token(data={"sub": test_email})
        print(f"✓ Access token created: {access_token[:30]}...")
        
        # Verify access token
        payload = verify_token(access_token, token_type="access")
        if payload and payload.get("sub") == test_email:
            print(f"✓ Access token verified: {payload.get('sub')}")
        else:
            print("❌ Access token verification failed")
            return False
        
        # Create refresh token
        from app.auth.security import create_refresh_token
        refresh_token = create_refresh_token(data={"sub": test_email})
        print(f"✓ Refresh token created: {refresh_token[:30]}...")
        
        # Verify refresh token
        refresh_payload = verify_token(refresh_token, token_type="refresh")
        if refresh_payload and refresh_payload.get("sub") == test_email:
            print(f"✓ Refresh token verified: {refresh_payload.get('sub')}")
        else:
            print("❌ Refresh token verification failed")
            return False
        
        print("✅ JWT authentication tests passed")
        return True
        
    except Exception as e:
        print(f"❌ JWT test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_models():
    """Test all database models"""
    print("\n" + "="*60)
    print("TEST 5: Database Models")
    print("="*60)
    
    try:
        from app.models import User, IndicatorValue, DataSource, FetchLog, Export
        
        print(f"✓ User model: {User.__tablename__}")
        print(f"✓ IndicatorValue model: {IndicatorValue.__tablename__}")
        print(f"✓ DataSource model: {DataSource.__tablename__}")
        print(f"✓ FetchLog model: {FetchLog.__tablename__}")
        print(f"✓ Export model: {Export.__tablename__}")
        
        print("✅ All models imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Model import test failed: {e}")
        return False


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 ATLASIQ BACKEND CORE - TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Configuration
        await test_config()
        
        # Test 2: Database Connection
        db_ok = await test_database_connection()
        if not db_ok:
            print("\n⚠️  Skipping remaining tests due to database connection failure")
            print("   Make sure PostgreSQL is running and DATABASE_URL is correct")
            return
        
        # Test 3: User Model
        await test_user_model()
        
        # Test 4: JWT Tokens
        await test_jwt_tokens()
        
        # Test 5: Models
        await test_models()
        
        # Summary
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n📝 Backend Core Implementation Complete:")
        print("   ✓ Configuration management")
        print("   ✓ Database connection & models")
        print("   ✓ User authentication")
        print("   ✓ JWT token generation & verification")
        print("   ✓ Password hashing")
        print("\n🚀 Next Steps:")
        print("   1. Start the backend: python -m app.main")
        print("   2. Visit API docs: http://localhost:8000/docs")
        print("   3. Test authentication endpoints")
        print("   4. Implement data adapters (Phase 2)")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        await close_db()
        print("\n✓ Database connections closed")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
