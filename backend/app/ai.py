import os
import asyncio
from typing import Optional
import litellm
from openai import OpenAI

# Configure LiteLLM
litellm.set_verbose = False

# OpenAI client for moderation
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CARLOS_SYSTEM_PROMPT = """You are Carlos, an experienced AI developer and the creator of Echo. You are helpful, knowledgeable, and passionate about AI and programming. You respond in a friendly, conversational tone and love helping people learn about AI development, programming, and technology.

Key traits:
- Enthusiastic about AI and programming
- Patient and encouraging with beginners
- Practical and solution-oriented
- Occasionally shares insights about AI development
- Keeps responses concise but informative (2-3 sentences typically)
- Uses a warm, approachable tone

You're having a conversation in the comments section of your Echo application demo."""

async def generate_ai_response(user_content: str, is_flagged: bool = False) -> str:
    """Generate AI response as Carlos"""
    try:
        if is_flagged:
            return "Let's try to keep the conversation respectful and constructive. I'm here to help with any questions about AI development or programming!"
        
        response = await litellm.acompletion(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": CARLOS_SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"AI response error: {e}")
        return "Thanks for your comment! I'm having some technical difficulties right now, but I appreciate you being part of the Echo community."

def moderate_content(content: str) -> bool:
    """Check if content should be flagged using OpenAI moderation"""
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return False
            
        response = openai_client.moderations.create(input=content)
        return response.results[0].flagged
        
    except Exception as e:
        print(f"Moderation error: {e}")
        return False