import os
import secrets
import resend
from datetime import datetime, timedelta
from typing import Optional

# Configure Resend
resend.api_key = os.getenv("RESEND_API_KEY")

# In-memory token storage (use Redis in production)
magic_tokens = {}

async def create_magic_link(email: str) -> str:
    """Create and send magic link"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    magic_tokens[token] = {
        "email": email,
        "expires_at": expires_at
    }
    
    # Send email via Resend
    if resend.api_key:
        magic_link = f"http://localhost:8000/api/auth/verify/{token}"
        
        params = {
            "from": "Echo <noreply@echo.ai>",
            "to": [email],
            "subject": "Your Echo Magic Link",
            "html": f"""
            <h2>Welcome to Echo!</h2>
            <p>Click the link below to authenticate:</p>
            <a href="{magic_link}">Authenticate with Echo</a>
            <p>This link expires in 15 minutes.</p>
            """
        }
        
        try:
            resend.Emails.send(params)
        except Exception as e:
            print(f"Email sending error: {e}")
    
    return token

def verify_magic_link(token: str) -> Optional[str]:
    """Verify magic link token"""
    if token not in magic_tokens:
        return None
    
    token_data = magic_tokens[token]
    
    if datetime.utcnow() > token_data["expires_at"]:
        del magic_tokens[token]
        return None
    
    email = token_data["email"]
    del magic_tokens[token]
    
    return email