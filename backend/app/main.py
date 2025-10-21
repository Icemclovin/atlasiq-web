"""
FastAPI main application
AtlasIQ Web - Macro-economic data aggregation and risk assessment platform
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db, close_db, check_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Debug: {settings.DEBUG}")
    
    # Initialize database (non-blocking in dev mode)
    try:
        await init_db()
        print("✅ Database initialized")
        
        # Check database connection
        if await check_db_connection():
            print("✅ Database connection healthy")
        else:
            print("⚠️  Database connection check failed")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")
        print("   Server will start anyway. Some features may not work without database.")
        print("   To fix: Start PostgreSQL or update DATABASE_URL in .env")
    
    print(f"\n🌐 Server running on http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API docs available at http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔍 Health check at http://{settings.HOST}:{settings.PORT}/health\n")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    await close_db()
    print("✅ Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Macro-economic data aggregation and risk assessment platform for Benelux + Germany",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
cors_origins = settings.get_cors_origins()
print(f"🔒 CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel preview deployments
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.get_cors_methods(),
    allow_headers=settings.get_cors_headers(),
)

# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Returns application status and database connectivity
    """
    db_healthy = await check_db_connection()
    
    health_status = {
        "status": "healthy" if db_healthy else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if db_healthy else "disconnected",
    }
    
    status_code = status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(content=health_status, status_code=status_code)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    Returns API information
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


# Import and include routers
from app.api.v1 import auth, data, companies
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(data.router, prefix="/api/v1/data", tags=["Data"])
app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
