from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

Base = declarative_base()

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    email = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    is_ai = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Self-referential relationship for threaded comments
    children = relationship("Comment", backref="parent", remote_side=[id])

# Pydantic models for API
class CommentBase(BaseModel):
    content: str
    email: EmailStr
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    is_ai: bool
    is_flagged: bool
    created_at: datetime
    children: List['CommentResponse'] = []
    
    class Config:
        from_attributes = True

# Update forward reference
CommentResponse.model_rebuild()

class MagicLinkRequest(BaseModel):
    email: EmailStr