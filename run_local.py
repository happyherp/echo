#!/usr/bin/env python3
"""
Local development server for Echo application.
Runs with SQLite database and environment variables.
"""

import os
import subprocess
import sys

def main():
    # Set environment variables for local development
    env = os.environ.copy()
    env.update({
        "DATABASE_URL": "sqlite:///./echo_local.db",
        "SECRET_KEY": "local_development_secret_key_change_in_production"
    })
    
    # Check if OpenAI API key is provided
    if not env.get("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. AI responses will not work.")
        print("   Set it with: export OPENAI_API_KEY='your_key_here'")
        print()
    
    # Check if Resend API key is provided
    if not env.get("RESEND_API_KEY"):
        print("⚠️  Warning: RESEND_API_KEY not set. Magic links will not work.")
        print("   Set it with: export RESEND_API_KEY='your_key_here'")
        print()
    
    print("🚀 Starting Echo local development server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    try:
        # Change to backend directory and start server
        os.chdir("backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], env=env)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except FileNotFoundError:
        print("❌ Error: Make sure you're in the Echo project directory")
        print("   and have installed the requirements:")
        print("   pip install -r backend/requirements.txt")

if __name__ == "__main__":
    main()