# Inkingi Smart School App

A comprehensive multi-tenant school management platform with role-based access control, communication tools, fees and inventory tracking, and an AI agent powered by each school's private data.

## 🚀 Features

### Core Features (MVP)
- **School Management**: Register, verify, and manage schools
- **User Management**: Role-based access control (System Admin, School Admin, Accountant, Teacher, Parent)
- **People Management**: Staff, students, and parents with rich profiles
- **Academic Calendar**: Define academic years and terms per school
- **Class Management**: Create classes, assign teachers, enroll students
- **Course Management**: Create courses and assign teachers
- **Timetable Management**: Generate weekly timetables with conflict detection
- **Marks Management**: Assignment and exam marks with reporting
- **Fees Management**: Fee structures, payments, and financial tracking
- **Inventory Management**: School assets and stock management
- **Communication**: Email and SMS to users/parents
- **AI Agent**: Chat with school data, generate insights, and reports

### Technology Stack

**Backend:**
- FastAPI (Python) with Pydantic v2 for validation
- SQLAlchemy 2.x + Alembic for ORM and migrations
- PostgreSQL with Row-Level Security (RLS) for multi-tenancy
- Redis for caching and background jobs
- Celery for async tasks (email/SMS, reports, AI processing)
- JWT authentication with role-based access control

**Frontend:**
- React 18 with Vite and TypeScript
- Tailwind CSS for styling
- shadcn/ui + Radix UI for accessible components
- Zustand for state management
- TanStack Query for data fetching and caching
- React Router for navigation

**Infrastructure:**
- Docker + Docker Compose for local development
- Nginx for reverse proxy
- Redis for caching and message queuing

## 🏗️ Architecture

### Multi-Tenancy Design
- **Isolation Strategy**: Row-Level Security (RLS) in PostgreSQL on `tenant_id`
- **Domain Strategy**: `schoolSlug.app.com` or custom domain mapping
- **Access Control**: Fine-grained permissions with role-based access

### Database Design
- Multi-tenant tables with `tenant_id` for data isolation
- Comprehensive RBAC system with roles, permissions, and access scopes
- Academic calendar, class management, and enrollment tracking
- Financial management with fees and payments
- Communication system with email/SMS capabilities
- AI chat sessions and message history

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inkingi-smart-school
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your configuration
   npm run dev
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/inkingi_school
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
SMTP_HOST=your-smtp-host
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-smtp-password
OPENAI_API_KEY=your-openai-api-key
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📱 Usage

### Demo Credentials
- Email: admin@school.com
- Password: password123

### Key Features

1. **Dashboard**: Overview of school statistics and recent activities
2. **School Management**: Create and manage multiple schools
3. **User Management**: Add users with different roles and permissions
4. **Student Management**: Enroll students and manage their information
5. **Class Management**: Create classes and assign teachers
6. **Timetable**: Generate and manage class schedules
7. **Marks**: Record and track student grades
8. **Fees**: Manage fee structures and payments
9. **Inventory**: Track school assets and supplies
10. **Communication**: Send emails and SMS to stakeholders
11. **AI Assistant**: Chat with school data and get insights

## 🏛️ Multi-Tenancy

The platform supports multiple schools with complete data isolation:

- Each school has its own data space identified by `tenant_id`
- Row-Level Security ensures data isolation at the database level
- Schools can have custom domains or use subdomains
- System administrators can manage all schools
- School administrators can only access their school's data

## 🔐 Security

- JWT-based authentication with configurable expiration
- Role-based access control with fine-grained permissions
- Password hashing using bcrypt
- CORS protection and input validation
- SQL injection protection through SQLAlchemy ORM
- XSS protection through React's built-in escaping

## 📊 API Documentation

The API is fully documented using FastAPI's automatic OpenAPI generation:

- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   - Set up PostgreSQL and Redis servers
   - Configure environment variables
   - Set up SSL certificates

2. **Database Migration**
   ```bash
   alembic upgrade head
   ```

3. **Start Services**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Cloud Deployment

The application is designed to be deployed on cloud platforms:

- **AWS**: ECS, RDS, ElastiCache, S3
- **Google Cloud**: Cloud Run, Cloud SQL, Memorystore
- **Azure**: Container Instances, Azure Database, Redis Cache

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the API docs at `/docs`

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core school management
- ✅ User authentication and authorization
- ✅ Basic CRUD operations
- ✅ Multi-tenant architecture

### Phase 2 (Next)
- 🔄 Advanced reporting and analytics
- 🔄 Mobile app (React Native)
- 🔄 Advanced AI features
- 🔄 Integration with external services

### Phase 3 (Future)
- 📋 Advanced analytics dashboard
- 📋 Mobile app for parents and students
- 📋 Advanced AI-powered insights
- 📋 Third-party integrations (payment gateways, SMS providers)

---

Built with ❤️ for educational institutions worldwide.