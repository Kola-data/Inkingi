# Inkingi Smart School - Multi-Tenant School Management Platform

A comprehensive, modern school management system built with FastAPI, React, and PostgreSQL. Features multi-tenancy, role-based access control, real-time communication, and AI-powered insights.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.2-blue.svg)

## 🚀 Features

### Core Functionality
- **Multi-Tenant Architecture**: Row-level security with PostgreSQL for complete data isolation
- **Role-Based Access Control**: System Admin, School Admin, Accountant, Teacher, and Parent roles
- **School Management**: Register, verify, and manage multiple schools
- **User Management**: Comprehensive user profiles with staff-first approach
- **Academic Calendar**: Define academic years and terms with locking capabilities
- **Class Management**: Create classes, assign teachers, and enroll students
- **Course Management**: Create courses and assign teachers
- **Timetable Management**: Generate conflict-free timetables with room allocation
- **Marks Management**: Track assignments and exams with automatic report generation
- **Fees Management**: Flexible fee structures with payment tracking
- **Inventory Management**: Track school resources and supplies
- **Communication**: Email and SMS capabilities for mass communication
- **AI Agent**: Per-school AI assistant for Q&A and report generation

### Technical Features
- **Beautiful UI**: Modern, responsive design with dark mode support
- **Real-time Updates**: WebSocket support for live notifications
- **Background Jobs**: Celery for async tasks (emails, reports, data processing)
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Security**: JWT authentication, rate limiting, and input validation
- **Monitoring**: Integrated with Sentry, Prometheus, and Grafana

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.x** - ORM with async support
- **PostgreSQL** - Primary database with RLS
- **Redis** - Caching and session management
- **Celery** - Distributed task queue
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TanStack Query** - Data fetching
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD
- **Terraform** - Infrastructure as Code

## 📋 Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)
- Redis 7+ (for local development)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/inkingi-smart-school.git
cd inkingi-smart-school
```

2. **Set up environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs
- Flower (Celery monitoring): http://localhost:5555

### Local Development

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the backend server**
```bash
uvicorn app.main:app --reload --port 8000
```

6. **Start Celery worker (in another terminal)**
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

7. **Start Celery beat (in another terminal)**
```bash
celery -A app.workers.celery_app beat --loglevel=info
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install --legacy-peer-deps
```

2. **Start development server**
```bash
npm run dev
```

## 📚 API Documentation

Once the backend is running, you can access:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🔧 Configuration

### Environment Variables

Key environment variables for backend (see `backend/.env.example` for full list):

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - Email configuration
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` - SMS configuration
- `OPENAI_API_KEY` - AI features configuration

### Multi-Tenancy Setup

The system uses subdomain-based tenant identification:
- Format: `schoolslug.yourdomain.com`
- Alternative: Pass `X-Tenant-ID` header in API requests

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Project Structure

```
inkingi-smart-school/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── workers/      # Celery tasks
│   │   └── utils/        # Utilities
│   ├── migrations/       # Alembic migrations
│   ├── tests/           # Test files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── stores/      # Zustand stores
│   │   ├── hooks/       # Custom hooks
│   │   └── utils/       # Utilities
│   ├── public/          # Static files
│   └── package.json
├── infrastructure/
│   ├── docker/          # Docker configurations
│   ├── nginx/           # Nginx configurations
│   └── terraform/       # Terraform files
└── docker-compose.yml
```

## 🔒 Security

- JWT-based authentication
- Role-based access control (RBAC)
- Row-level security in PostgreSQL
- Rate limiting on API endpoints
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection in React
- HTTPS enforcement in production

## 🚀 Deployment

### Production Deployment

1. **Update environment variables for production**
2. **Build Docker images**
```bash
docker-compose -f docker-compose.prod.yml build
```

3. **Deploy using Docker Swarm or Kubernetes**
4. **Set up SSL certificates with Let's Encrypt**
5. **Configure monitoring and logging**

## 📊 Monitoring

- **Application Monitoring**: Sentry
- **Metrics**: Prometheus + Grafana
- **Logs**: Loki
- **Celery Monitoring**: Flower

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing Python framework
- React team for the excellent UI library
- shadcn for the beautiful component library
- All contributors and open-source projects that made this possible

## 📞 Support

For support, email support@inkingischool.com or open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Mobile applications (React Native)
- [ ] Advanced analytics dashboard
- [ ] Video conferencing integration
- [ ] Blockchain-based certificate verification
- [ ] Multi-language support
- [ ] Advanced AI features (predictive analytics, personalized learning)
- [ ] Integration with popular LMS platforms
- [ ] Biometric attendance system

---

**Made with ❤️ by the Inkingi Team**