from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from . import models
from .database import SessionLocal, engine
from .ai import generate_ai_response, moderate_content
from .auth import create_magic_link, verify_magic_link

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Echo - AI Chat Application")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Static files and templates
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/comments", response_model=List[models.CommentResponse])
async def get_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.parent_id.is_(None)).order_by(models.Comment.created_at.desc()).all()
    return comments

@app.post("/api/comments", response_model=models.CommentResponse)
@limiter.limit("100/hour")
async def create_comment(
    request: Request,
    comment: models.CommentCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Check content moderation
    is_flagged = moderate_content(comment.content)
    
    # Create comment
    db_comment = models.Comment(
        content=comment.content,
        email=comment.email,
        parent_id=comment.parent_id,
        is_flagged=is_flagged
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # Generate AI response in background
    background_tasks.add_task(generate_ai_response_task, db_comment.id, comment.content, is_flagged)
    
    return db_comment

async def generate_ai_response_task(comment_id: int, user_content: str, is_flagged: bool):
    """Background task to generate AI response"""
    db = SessionLocal()
    try:
        ai_content = await generate_ai_response(user_content, is_flagged)
        
        ai_comment = models.Comment(
            content=ai_content,
            email="carlos@echo.ai",
            parent_id=comment_id,
            is_ai=True,
            is_flagged=False
        )
        db.add(ai_comment)
        db.commit()
    finally:
        db.close()

@app.post("/api/auth/magic-link")
async def send_magic_link(email_request: models.MagicLinkRequest):
    """Send magic link for authentication"""
    try:
        await create_magic_link(email_request.email)
        return {"message": "Magic link sent to your email"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send magic link")

@app.get("/api/auth/verify/{token}")
async def verify_magic_link_endpoint(token: str):
    """Verify magic link token"""
    email = verify_magic_link(token)
    if email:
        return {"email": email, "authenticated": True}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)