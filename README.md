# 🎯 Echo - AI Chat Application

A modern AI-powered chat application featuring threaded comments, content moderation, and magic link authentication. Built with FastAPI, Alpine.js, and OpenAI integration.

## ✨ Features

- **AI Integration**: Carlos, an AI developer, responds to every user comment
- **Threaded Comments**: Reddit-style nested comment system (up to 5 levels)
- **Content Moderation**: Automatic flagging of inappropriate content
- **Magic Link Auth**: Passwordless authentication via email
- **Rate Limiting**: 100 comments per hour per email address
- **Real-time Updates**: Comments refresh automatically
- **Responsive Design**: Works on desktop and mobile
- **Docker Ready**: Easy deployment with Docker Compose

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- (Optional) Resend API key for email functionality

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/happyherp/echo.git
   cd echo
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   export RESEND_API_KEY="your_resend_api_key_here"  # Optional
   ```

4. **Run the application**
   ```bash
   python run_local.py
   ```

5. **Open your browser**
   Visit http://localhost:8000

### Docker Deployment

1. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## 🧪 Demo Script

Run the interactive demo to see all features in action:

```bash
export OPENAI_API_KEY="your_key_here"
python demo.py
```

The demo will:
- Start the server
- Create sample conversations
- Test content moderation
- Show the complete conversation tree

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with PostgreSQL/SQLite support
- **LiteLLM**: Universal LLM API for OpenAI integration
- **Resend**: Email service for magic links
- **SlowAPI**: Rate limiting middleware

### Frontend (Alpine.js)
- **Alpine.js**: Lightweight reactive framework
- **Vanilla CSS**: Custom responsive design
- **No build process**: Direct browser compatibility

### Database Schema
```sql
comments (
  id: Primary Key
  content: Text content
  email: User email
  parent_id: Foreign key for threading
  is_ai: Boolean flag for AI responses
  is_flagged: Boolean flag for moderated content
  created_at: Timestamp
)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI responses | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `RESEND_API_KEY` | Resend API key for emails | No |
| `SECRET_KEY` | JWT secret key | No (auto-generated) |

### Example .env file
```bash
OPENAI_API_KEY=sk-proj-your_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/echo
RESEND_API_KEY=re_your_key_here
SECRET_KEY=your_secret_key_here
```

## 🧪 Testing

Run the test suite:

```bash
cd backend
pytest app/tests/
```

Tests cover:
- API endpoints
- Database models
- AI integration
- Content moderation
- Authentication

## 📁 Project Structure

```
echo/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # Main application
│   │   ├── models.py       # Database models
│   │   ├── ai.py           # AI integration
│   │   ├── auth.py         # Authentication
│   │   ├── database.py     # Database configuration
│   │   └── tests/          # Unit tests
│   ├── Dockerfile          # Backend container
│   └── requirements.txt    # Python dependencies
├── frontend/               # Alpine.js frontend
│   ├── static/
│   │   ├── app.js          # JavaScript application
│   │   └── style.css       # Responsive styles
│   └── templates/
│       └── index.html      # Main page template
├── postgres/               # Database initialization
├── docker-compose.yml      # Docker orchestration
├── run_local.py           # Local development server
├── demo.py                # Interactive demo script
└── README.md              # This file
```

## 🤖 AI Integration

### Carlos - The AI Developer

Carlos is an AI character designed to:
- Help users learn about AI development
- Provide programming guidance
- Maintain a friendly, encouraging tone
- Respond contextually to user questions

### Content Moderation

- Uses OpenAI's moderation API
- Automatically flags inappropriate content
- AI responds appropriately to flagged content
- Maintains a respectful community environment

## 🔒 Security Features

- **Rate Limiting**: Prevents spam and abuse
- **Content Moderation**: Automatic inappropriate content detection
- **Input Validation**: Pydantic models for data validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Secure cross-origin requests

## 🚀 Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Configure PostgreSQL database
- [ ] Set up Resend for email delivery
- [ ] Configure reverse proxy (nginx)
- [ ] Set up SSL certificates
- [ ] Configure monitoring and logging
- [ ] Set up backup strategy

### Scaling Considerations

- Use Redis for session storage and rate limiting
- Implement database connection pooling
- Add CDN for static assets
- Consider horizontal scaling with load balancer
- Monitor OpenAI API usage and costs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Check the code comments and docstrings
- **Community**: Join discussions in the GitHub repository

---

Built with ❤️ using FastAPI, Alpine.js, and OpenAI
