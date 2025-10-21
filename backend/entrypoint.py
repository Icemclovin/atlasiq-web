#!/usr/bin/env python3
"""
Entrypoint script for Railway deployment
Runs initialization then starts uvicorn
"""
import os
import sys
import subprocess

print("=" * 60)
print("🚀 AtlasIQ Backend Startup Script")
print("=" * 60)

# Step 1: Run database initialization
print("\n📦 Step 1: Running database initialization...")
try:
    result = subprocess.run([sys.executable, "docker_init.py"], check=False)
    print(f"✅ Initialization completed with exit code: {result.returncode}")
except Exception as e:
    print(f"⚠️  Initialization error: {e}")
    print("⚠️  Continuing anyway...")

# Step 2: Start Uvicorn
port = os.getenv("PORT", "8000")
print(f"\n🌐 Step 2: Starting Uvicorn on port {port}...")
print("=" * 60)
print()

# Use exec to replace this process with uvicorn
os.execvp("uvicorn", ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", port])
