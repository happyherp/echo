#!/usr/bin/env python3
"""
Echo Application Demo Script

This script demonstrates the full functionality of the Echo application
with a working OpenAI API key.

Usage:
    export OPENAI_API_KEY="your_openai_api_key_here"
    python demo.py
"""

import os
import subprocess
import time
import requests
import json

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
DATABASE_URL = "sqlite:///./echo_demo.db"
SECRET_KEY = "demo_secret_key"
BASE_URL = "http://localhost:8000"

def start_server():
    """Start the Echo server with proper environment variables."""
    print("🚀 Starting Echo server...")
    
    env = os.environ.copy()
    env.update({
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "DATABASE_URL": DATABASE_URL,
        "SECRET_KEY": SECRET_KEY
    })
    
    # Change to backend directory and start server
    process = subprocess.Popen([
        "python", "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ], cwd="backend", env=env)
    
    # Wait for server to start
    time.sleep(3)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server started successfully!")
            return process
        else:
            print("❌ Server failed to start")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return None

def demo_conversation():
    """Demonstrate a conversation with the AI."""
    print("\n💬 Starting conversation demo...")
    
    # Create first comment
    print("\n1. User asks about AI development:")
    comment1_data = {
        "content": "Hi Carlos! I'm new to programming and interested in AI. Where should I start?",
        "email": "newbie@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/api/comments", json=comment1_data)
    if response.status_code == 200:
        comment1 = response.json()
        print(f"   User: {comment1['content']}")
        print(f"   Comment ID: {comment1['id']}")
    else:
        print("❌ Failed to create comment")
        return
    
    # Wait for AI response
    print("\n2. Waiting for AI response...")
    time.sleep(5)
    
    # Get comments to see AI response
    response = requests.get(f"{BASE_URL}/api/comments")
    if response.status_code == 200:
        comments = response.json()
        if comments and comments[0]['children']:
            ai_response = comments[0]['children'][0]
            print(f"   Carlos: {ai_response['content']}")
        else:
            print("❌ No AI response found")
            return
    else:
        print("❌ Failed to get comments")
        return
    
    # Reply to AI
    print("\n3. User replies to AI:")
    reply_data = {
        "content": "Thanks! What about Python libraries for machine learning?",
        "parent_id": ai_response['id'],
        "email": "newbie@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/api/comments", json=reply_data)
    if response.status_code == 200:
        reply = response.json()
        print(f"   User: {reply['content']}")
    else:
        print("❌ Failed to create reply")
        return
    
    # Wait for AI response to reply
    print("\n4. Waiting for AI response to reply...")
    time.sleep(5)
    
    # Get final conversation
    response = requests.get(f"{BASE_URL}/api/comments")
    if response.status_code == 200:
        comments = response.json()
        # Find the nested AI response
        if (comments and comments[0]['children'] and 
            comments[0]['children'][0]['children'] and
            comments[0]['children'][0]['children'][0]['children']):
            final_ai_response = comments[0]['children'][0]['children'][0]['children'][0]
            print(f"   Carlos: {final_ai_response['content']}")
        else:
            print("❌ No final AI response found")
    else:
        print("❌ Failed to get final comments")

def demo_moderation():
    """Demonstrate content moderation."""
    print("\n🛡️  Testing content moderation...")
    
    inappropriate_comment = {
        "content": "This is a test of inappropriate content with bad language",
        "email": "tester@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/api/comments", json=inappropriate_comment)
    if response.status_code == 200:
        comment = response.json()
        print(f"   Comment flagged: {comment['is_flagged']}")
        if comment['is_flagged']:
            print("   ✅ Content moderation working correctly!")
        else:
            print("   ⚠️  Content not flagged (may be acceptable)")
    else:
        print("❌ Failed to test moderation")

def show_final_conversation():
    """Show the complete conversation tree."""
    print("\n📋 Final conversation structure:")
    
    response = requests.get(f"{BASE_URL}/api/comments")
    if response.status_code == 200:
        comments = response.json()
        print(json.dumps(comments, indent=2))
    else:
        print("❌ Failed to get conversation")

def main():
    """Run the complete demo."""
    print("🎯 Echo Application Demo")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if OPENAI_API_KEY == "your_openai_api_key_here":
        print("❌ Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your_actual_api_key_here'")
        return
    
    # Start server
    server_process = start_server()
    if not server_process:
        return
    
    try:
        # Run demos
        demo_conversation()
        demo_moderation()
        show_final_conversation()
        
        print("\n🎉 Demo completed successfully!")
        print(f"🌐 Visit {BASE_URL} to see the web interface")
        print("Press Ctrl+C to stop the server")
        
        # Keep server running
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()