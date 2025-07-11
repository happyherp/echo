import os
import pytest
from fastapi.testclient import TestClient

# Set test environment variables before importing the app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["OPENAI_API_KEY"] = "test_key"

from app.main import app
from app.database import SessionLocal, engine
from app import models

# Create test database
models.Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_comments_empty():
    """Test getting comments when none exist"""
    response = client.get("/api/comments")
    assert response.status_code == 200
    assert response.json() == []

def test_create_comment():
    """Test creating a new comment"""
    comment_data = {
        "content": "This is a test comment",
        "email": "test@example.com"
    }
    
    response = client.post("/api/comments", json=comment_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["content"] == comment_data["content"]
    assert data["email"] == comment_data["email"]
    assert data["is_ai"] == False
    assert "id" in data
    assert "created_at" in data

def test_get_comments_with_data():
    """Test getting comments after creating one"""
    response = client.get("/api/comments")
    assert response.status_code == 200
    
    comments = response.json()
    assert len(comments) >= 1
    assert comments[0]["content"] == "This is a test comment"

def test_create_reply():
    """Test creating a reply to a comment"""
    # First get the parent comment
    response = client.get("/api/comments")
    parent_comment = response.json()[0]
    
    reply_data = {
        "content": "This is a reply",
        "email": "reply@example.com",
        "parent_id": parent_comment["id"]
    }
    
    response = client.post("/api/comments", json=reply_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["content"] == reply_data["content"]
    assert data["parent_id"] == parent_comment["id"]

def test_invalid_comment():
    """Test creating comment with invalid data"""
    invalid_data = {
        "content": "",  # Empty content
        "email": "invalid-email"  # Invalid email
    }
    
    response = client.post("/api/comments", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_magic_link_request():
    """Test requesting a magic link"""
    email_data = {"email": "test@example.com"}
    
    response = client.post("/api/auth/magic-link", json=email_data)
    # Should succeed even without Resend API key (just won't send email)
    assert response.status_code == 200
    assert "message" in response.json()

def test_verify_invalid_token():
    """Test verifying an invalid magic link token"""
    response = client.get("/api/auth/verify/invalid_token")
    assert response.status_code == 400
    assert "Invalid or expired token" in response.json()["detail"]

# Cleanup after tests
def teardown_module():
    """Clean up test database"""
    try:
        os.remove("test.db")
    except FileNotFoundError:
        pass