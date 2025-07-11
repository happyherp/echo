# 🚀 Echo Deployment Guide

## Quick Start for Testing

### 1. Clone the Repository
```bash
git clone https://github.com/happyherp/echo.git
cd echo
git checkout echo-mvp-complete
```

### 2. Set Up Environment
```bash
# Required: OpenAI API key
export OPENAI_API_KEY="your_openai_api_key_here"

# Optional: Email functionality
export RESEND_API_KEY="your_resend_api_key_here"
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Run the Application
```bash
python run_local.py
```

### 5. Open Your Browser
Visit: http://localhost:8000

## Demo Script

To see all features in action:
```bash
export OPENAI_API_KEY="your_key_here"
python demo.py
```

## Docker Deployment

For production-like environment:
```bash
cp .env.example .env
# Edit .env with your API keys
docker-compose up -d
```

## Features You Can Test

1. **Post a Comment**: Enter your email and ask Carlos about AI development
2. **AI Response**: Carlos will respond automatically (requires OpenAI API key)
3. **Reply System**: Click "Reply" to create threaded conversations
4. **Content Moderation**: Try posting inappropriate content to see moderation
5. **Real-time Updates**: Comments refresh automatically every 10 seconds

## Troubleshooting

### No AI Responses
- Ensure `OPENAI_API_KEY` is set correctly
- Check the console for error messages
- Verify your OpenAI account has credits

### Email Not Working
- Magic links require `RESEND_API_KEY`
- This is optional - the app works without it

### Database Issues
- Local development uses SQLite (no setup required)
- Docker uses PostgreSQL (automatic setup)

## Production Deployment

For production deployment, see the comprehensive README.md for:
- Environment variable configuration
- Database setup
- Security considerations
- Scaling recommendations

## Support

- **GitHub Issues**: Report bugs or request features
- **Pull Request**: https://github.com/happyherp/echo/pull/6
- **Documentation**: See README.md for complete documentation