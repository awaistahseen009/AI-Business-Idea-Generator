# AI Business Idea Generator

A powerful Flask-based web application that uses AI to generate innovative startup ideas for any niche or industry. Built with LangGraph for AI workflow orchestration and enhanced with optional web search capabilities.

## 🚀 Features

- **AI-Powered Idea Generation**: Generate 3 unique startup ideas with detailed pitches, target audiences, and revenue models
- **Web Search Enhancement**: Optional integration with Tavily API for current market trend analysis
- **User Authentication**: Secure registration and login system
- **Idea History**: Store and browse all previously generated ideas
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Processing**: LangGraph workflow for efficient AI processing

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **AI Orchestration**: LangGraph
- **Database**: Supabase PostgreSQL
- **LLM Provider**: OpenAI via `langchain-openai` (configurable by `OPENAI_MODEL`)
- **Web Search**: Tavily via `langchain-community` wrapper
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-WTF with CSRF protection

## 📋 Prerequisites

- Python 3.10+
- Supabase account and project
- OpenAI API key (`OPENAI_API_KEY`)
- Tavily API key (`TAVILY_API_KEY`) if using web search

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-business-idea-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your actual API keys and configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4o-mini
   TAVILY_API_KEY=your-tavily-api-key  # Optional
   ```

5. **Set up Supabase database**
   
   Run the following SQL commands in your Supabase SQL editor:
   
   ```sql
   -- Create users table
   CREATE TABLE IF NOT EXISTS public.users (
       id SERIAL PRIMARY KEY,
       email VARCHAR(255) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Create business_ideas table
   CREATE TABLE IF NOT EXISTS public.business_ideas (
       id SERIAL PRIMARY KEY,
       user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
       niche VARCHAR(255) NOT NULL,
       ideas JSONB NOT NULL,
       web_search_used BOOLEAN DEFAULT FALSE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Create indexes for better performance
   CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
   CREATE INDEX IF NOT EXISTS idx_business_ideas_user_id ON public.business_ideas(user_id);
   CREATE INDEX IF NOT EXISTS idx_business_ideas_created_at ON public.business_ideas(created_at DESC);
   ```

6. **Run the application (dev)**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

## 🎯 Usage

### Getting Started

1. **Register**: Create a new account with your email and password
2. **Login**: Sign in to access the idea generation features
3. **Generate Ideas**: 
   - Enter your niche or industry of interest
   - Optionally enable web search for enhanced market insights
   - Click "Generate Ideas" to create 3 unique startup concepts
4. **View History**: Browse all your previously generated ideas
5. **Copy Ideas**: Use the copy functionality to save ideas for external use

### Example Niches

- "Sustainable fashion for millennials"
- "AI-powered healthcare diagnostics"
- "Remote work productivity tools"
- "Fintech solutions for small businesses"
- "EdTech for professional development"

## 🏗 Project Structure

```
ai-business-idea-generator/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
│
├── routes/                 # Flask Blueprints
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   └── ideas.py            # Business idea generation & history
│
├── services/               # Business Logic
│   ├── __init__.py
│   ├── ai_workflow.py      # LangGraph workflow definition
│   ├── web_search.py       # Web search functionality
│   └── idea_storage.py     # Database operations
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── ideas/
│       ├── generate.html
│       ├── history.html
│       └── view.html
│
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── uploads/                # Runtime uploads directory
```

## 🔄 AI Workflow

The application uses LangGraph to orchestrate the AI workflow:

1. **Start Node**: Accept niche and web search toggle from user
2. **Conditional Node**: If web search is enabled, call Tavily via LangChain wrapper
3. **Prompt Node**: Send niche (and optional search results) to OpenAI
4. **Storage Node**: Save generated ideas to Supabase
5. **Output Node**: Return formatted results to user

## 🎨 Features in Detail

### AI Idea Generation
- Uses OpenAI chat models via `langchain-openai`
- Structured output with Pydantic models ensures consistent formatting
- Each idea includes: name, pitch, target audience, and revenue model

### Web Search Enhancement
- Optional Tavily integration via `langchain-community` wrapper for current market trends
- Enhances AI prompts with real-time market data
- Improves relevance and timeliness of generated ideas

### User Management
- Secure password hashing with Werkzeug
- Session-based authentication
- CSRF protection with Flask-WTF

### Database Design
- PostgreSQL with JSONB for flexible idea storage
- Efficient indexing for fast queries
- User-based data isolation

## 🔒 Security Features

- CSRF protection on all forms
- Secure password hashing
- Environment-based configuration
- Input validation and sanitization
- SQL injection prevention through ORM

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production` and `FLASK_DEBUG=False`.
2. Run with Uvicorn (ASGI) using the wrapper in `app.py`:
   ```bash
   pip install -r requirements.txt
   uvicorn app:asgi_app --host 0.0.0.0 --port 8000 --workers 2
   # Open in browser: http://127.0.0.1:8000
   ```
3. Optionally place Uvicorn behind Nginx for TLS/HTTP/2 and static caching.
4. Use environment variables for all sensitive configuration.

### Docker
Build and run with Docker (Uvicorn serves `app:asgi_app`):
```bash
docker build -t ai-idea-generator .
docker run --rm -p 8000:8000 --env-file .env ai-idea-generator
# Open in browser: http://127.0.0.1:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Keys Setup

### OpenAI API Key
1. Create an API key at OpenAI
2. Add it to your `.env` file as `OPENAI_API_KEY`

### Supabase Setup
1. Create a new project at [Supabase](https://supabase.com)
2. Get your project URL and anon key from Settings > API
3. Add them to your `.env` file

### Tavily API Key (Optional)
1. Sign up at [Tavily](https://tavily.com)
2. Get your API key from the dashboard
3. Add it to your `.env` file as `TAVILY_API_KEY`

## Highlights

![](images/1.PNG)
![](images/2.PNG)
![](images/3.PNG)
![](images/4.PNG)

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify Supabase URL and keys are correct
   - Check if database tables are created

2. **AI Generation Fails**
   - Verify Google API key is valid and has quota
   - Check internet connection for API calls

3. **Web Search Not Working**
   - Ensure Tavily API key is set (optional feature)
   - Check if web search toggle is enabled

4. **CSS/JS Not Loading**
   - Check if static files are in correct directories
   - Verify Flask static file serving is working

## 📊 Performance

- Average idea generation time: 3-5 seconds
- With web search: 5-8 seconds
- Database queries optimized with proper indexing
- Responsive design works on all device sizes

## 🔮 Future Enhancements

- [ ] Export ideas to PDF/Word documents
- [ ] Idea collaboration and sharing
- [ ] Advanced filtering and search
- [ ] Integration with more LLM providers
- [ ] Business plan generation
- [ ] Market analysis reports
- [ ] User feedback and rating system

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google AI for Gemini Pro API
- Supabase for database hosting
- Tavily for web search capabilities
- LangChain/LangGraph for AI orchestration
- Bootstrap for UI components

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using Flask, LangGraph, and AI**
