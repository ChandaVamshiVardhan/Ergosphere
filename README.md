# Smart Todo - AI-Powered Task Management

A full-stack web application that combines intelligent task management with AI-powered features for enhanced productivity. The system uses daily context (messages, emails, notes) to provide intelligent task management suggestions.

## 📁 Project Structure

```
smart_todo/
├── 📁 ai_module/                    # AI and ML functionality
│   └── task_ai.py                  # Main AI class with NLP and ML features
├── 📁 frontend/                     # Next.js frontend application
│   ├── 📁 public/                  # Static assets
│   ├── 📁 src/
│   │   ├── 📁 app/                 # Next.js App Router pages
│   │   │   ├── layout.tsx          # Root layout component
│   │   │   ├── page.tsx            # Main dashboard page
│   │   │   ├── globals.css         # Global styles
│   │   │   └── favicon.ico         # App icon
│   │   ├── 📁 components/          # React components
│   │   │   ├── TaskCard.tsx        # Individual task display
│   │   │   └── TaskForm.tsx        # Task creation/editing form
│   │   ├── 📁 hooks/               # Custom React hooks
│   │   │   └── useTasks.ts         # Task management hook
│   │   ├── 📁 types/               # TypeScript type definitions
│   │   │   └── index.ts            # All app types and interfaces
│   │   └── 📁 utils/               # Utility functions
│   │       └── api.ts              # API client functions
│   ├── package.json                # Frontend dependencies
│   ├── next.config.ts              # Next.js configuration
│   └── tailwind.config.js          # Tailwind CSS configuration
├── 📁 smart_todo/                  # Django project settings
│   ├── __init__.py                 # Project package
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Main URL configuration
│   └── wsgi.py                     # WSGI configuration
├── 📁 tasks/                       # Main Django app
│   ├── 📁 migrations/              # Database migrations
│   ├── __init__.py                 # App package
│   ├── admin.py                    # Django admin configuration
│   ├── models.py                   # Database models
│   ├── serializers.py              # DRF serializers
│   ├── tests.py                    # Test suite
│   ├── urls.py                     # App URL patterns
│   ├── utils.py                    # Utility functions
│   └── views.py                    # API views and endpoints
├── 📁 venv10/                      # Python virtual environment
├── .env                            # Environment variables
├── config.py                       # Configuration file
├── db.sqlite3                      # SQLite database
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Features

### Core Features
- **Task Management**: Create, edit, delete, and organize tasks with categories and priorities
- **AI-Powered Prioritization**: Intelligent task ranking based on urgency and context
- **Smart Categorization**: Auto-suggest task categories and tags
- **Deadline Suggestions**: AI-recommended realistic deadlines based on task complexity
- **Context Integration**: Process daily context (WhatsApp, emails, notes) for task suggestions
- **Enhanced Descriptions**: AI-improved task descriptions with context-aware details

### AI Features
- **Context Processing**: Analyze daily context to understand user's schedule and priorities
- **Priority Scoring**: Generate task priority scores based on context analysis
- **Smart Recommendations**: Provide optimal deadlines considering workload and context
- **Category Suggestions**: Recommend task categories and tags automatically
- **Sentiment Analysis**: Analyze context sentiment and urgency
- **Keyword Extraction**: Extract relevant keywords using TF-IDF
- **Time Mention Detection**: Identify deadlines and time references

### User Interface
- **Modern Design**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Real-time Updates**: Instant task updates and AI suggestions
- **Advanced Filtering**: Filter tasks by status, priority, category, and search
- **Task Analytics**: View task statistics and AI insights
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Interactive Forms**: AI-powered suggestions in task creation

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7**: Python web framework
- **Django REST Framework**: API development
- **SQLite**: Database (can be easily switched to PostgreSQL/Supabase)
- **Python 3.8+**: Core programming language
- **NLTK**: Natural language processing
- **scikit-learn**: Machine learning utilities
- **TextBlob**: Text processing and sentiment analysis

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API calls
- **date-fns**: Date manipulation utilities

### AI Integration
- **OpenAI API**: Primary AI service (configurable)
- **Custom NLP Pipeline**: Keyword extraction, sentiment analysis, urgency detection
- **Regex Pattern Matching**: Time and deadline extraction
- **TF-IDF Vectorization**: Keyword importance scoring

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn package manager
- OpenAI API key (optional, for AI features)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd smart_todo
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

#### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: Create admin user
```

#### Run Backend Server
```bash
python manage.py runserver
```
The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```

#### Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### Run Frontend Development Server
```bash
npm run dev
```
The frontend will be available at `http://localhost:3000`

## 🔧 Development Workflow

### Backend Development
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django admin
# Visit http://localhost:8000/admin
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

## 📖 API Documentation

### Task Endpoints
- `GET /api/tasks/` - Retrieve all tasks with optional filters
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

### Category Endpoints
- `GET /api/categories/` - Get all categories
- `POST /api/categories/` - Create new category

### Daily Context Endpoints
- `GET /api/context/` - Get all context entries
- `POST /api/context/` - Add new context entry

### AI Endpoints
- `POST /api/ai/suggestions/` - Get AI-powered suggestions
- `GET /api/ai/analytics/` - Get task analytics and insights

### Task Suggestions
- `GET /api/suggestions/` - Get AI-generated task suggestions
- `POST /api/suggestions/{id}/accept/` - Accept a task suggestion

## 📚 Interactive API Documentation

The backend provides interactive API documentation for all endpoints using **Swagger UI** and **Redoc**. These tools allow you to explore, test, and understand the API directly in your browser.

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

> **How to use:**
> - Start the backend server: `python manage.py runserver`
> - Visit the above URLs in your browser.
> - You can view all available endpoints, see request/response formats, and try out API calls interactively.

These docs are auto-generated from the backend code and update automatically as endpoints change.

### Frontend URL
- The frontend app runs at: [http://localhost:3000](http://localhost:3000)
- Make sure the backend is running at [http://localhost:8000](http://localhost:8000) for full functionality.

## 🎯 Usage Examples

### Creating a Task with AI Suggestions
1. Click "New Task" button
2. Enter task title and description
3. Click "Get AI Suggestions" to receive category and priority recommendations
4. Apply suggestions or customize manually
5. Save the task

### Adding Daily Context
1. Navigate to "Daily Context" tab
2. Add context entries (WhatsApp messages, emails, notes)
3. AI will automatically analyze and generate task suggestions
4. Review and accept relevant suggestions

### Viewing Analytics
1. Navigate to "Analytics" tab
2. View task completion rates, priority distribution
3. Check AI insights and recommendations

## 🔧 Configuration

### AI Service Configuration
The application supports multiple AI services:

#### OpenAI (Default)
```python
# In settings.py
OPENAI_API_KEY = 'your-openai-api-key'
```

#### LM Studio (Local)
```python
# Configure for local LLM hosting
LM_STUDIO_URL = 'http://localhost:1234/v1'
```

### Database Configuration
Switch from SQLite to PostgreSQL/Supabase:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Running Specific Tests
```bash
# Run specific test file
python manage.py test tasks.tests.TaskAPITest

# Run with verbose output
python manage.py test -v 2
```

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
```bash
# Database migration errors
python manage.py migrate --run-syncdb

# Import errors
pip install -r requirements.txt

# Port already in use
python manage.py runserver 8001
```

#### Frontend Issues
```bash
# Node modules issues
rm -rf node_modules package-lock.json
npm install

# Build errors
npm run build

# Port conflicts
npm run dev -- -p 3001
```

#### AI Module Issues
```bash
# NLTK data missing
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# OpenAI API issues
# Check your API key in .env file
# Verify API quota and billing
```

### Environment Variables
Make sure these are set correctly:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEXT_PUBLIC_API_URL`: Frontend API URL

## 📦 Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure production database
3. Set up static file serving
4. Use WSGI server (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn smart_todo.wsgi:application
```

### Frontend Deployment
```bash
cd frontend
npm run build
npm start
```

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🔒 Security Considerations

- Change default `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use HTTPS in production
- Implement proper authentication
- Validate all user inputs
- Keep dependencies updated

## 📈 Performance Optimization

### Backend
- Use database indexing for frequently queried fields
- Implement caching for AI analysis results
- Optimize database queries
- Use connection pooling for production

### Frontend
- Implement lazy loading for components
- Use React.memo for expensive components
- Optimize bundle size
- Implement proper error boundaries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: devgods99@gmail.com
- Create an issue in the repository
- Check the troubleshooting section above

## 🎉 Acknowledgments

- Django REST Framework for the robust API framework
- Next.js team for the excellent React framework
- OpenAI for AI capabilities
- Tailwind CSS for the beautiful styling system
- NLTK and scikit-learn for NLP capabilities

## 📊 Project Status

- ✅ Backend API complete
- ✅ Frontend UI complete
- ✅ AI integration working
- ✅ Database models implemented
- ✅ Testing framework set up
- ✅ Documentation complete
- 🔄 Continuous improvement

---

**Note**: This is a technical assignment for a full-stack developer position. The application demonstrates advanced AI integration, modern web development practices, and comprehensive task management features. The codebase is well-documented and follows best practices for maintainability and scalability. 