# Inkingi Smart School App

A comprehensive multi-tenant school management platform with role-based access control, communication tools, and AI-powered features.

## Features

- **Multi-Tenancy**: Row-Level Security (RLS) with PostgreSQL for complete data isolation
- **Role-Based Access Control**: System Admin, School Admin, Accountant, Teacher, and Parent roles
- **Class Management**: Create and manage classes with teacher assignments
- **Student Enrollment**: Enroll students in classes for academic years
- **Communication**: Email and SMS capabilities (via Celery tasks)
- **Modern UI**: Beautiful, responsive interface built with React + Tailwind CSS
- **Real-time Updates**: Using TanStack Query for efficient data fetching and caching

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Database with Row-Level Security for multi-tenancy
- **SQLAlchemy 2.x**: Modern ORM with async support
- **Redis**: Caching and message broker
- **Celery**: Distributed task queue for background jobs
- **JWT**: Secure authentication

### Frontend
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast development server and build tool
- **Tailwind CSS**: Utility-first CSS framework
- **TanStack Query**: Data fetching and state management
- **Zustand**: Lightweight state management
- **React Hook Form + Zod**: Form handling with validation

### Infrastructure
- **Docker**: Containerization for all services
- **Nginx**: Reverse proxy and load balancer
- **Docker Compose**: Local development orchestration

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inkingi-smart-school
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   
   # Frontend
   cp frontend/.env.example frontend/.env
   ```

3. **Start all services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Nginx (production-like): http://localhost

### Manual Setup (Alternative)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Run the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
inkingi-smart-school/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── tasks/          # Celery tasks
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # Utilities and configuration
│   │   ├── pages/          # Page components
│   │   ├── stores/         # Zustand stores
│   │   └── types/          # TypeScript type definitions
│   └── package.json
├── docker/                 # Docker configuration
└── docker-compose.yml
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token

### Classes
- `GET /api/v1/classes` - List classes
- `POST /api/v1/classes` - Create class
- `GET /api/v1/classes/{id}` - Get class details
- `PUT /api/v1/classes/{id}` - Update class
- `DELETE /api/v1/classes/{id}` - Delete class
- `POST /api/v1/classes/{id}/assign-teacher` - Assign teacher

### Enrollments
- `GET /api/v1/enrollments` - List enrollments
- `POST /api/v1/enrollments` - Create enrollment
- `GET /api/v1/enrollments/{id}` - Get enrollment details
- `DELETE /api/v1/enrollments/{id}` - Withdraw student

## Multi-Tenancy

The application uses Row-Level Security (RLS) in PostgreSQL for complete data isolation between schools:

1. **Tenant Resolution**: Extracted from subdomain (`school.app.com`) or JWT token
2. **Database Context**: `SET app.tenant_id = 'school_id'` for each request
3. **RLS Policies**: Automatically filter queries by tenant_id
4. **API Layer**: Middleware sets tenant context before processing requests

## Role-Based Access Control

### Roles
- **System Admin**: Platform management, cross-tenant operations
- **School Admin**: Full school management capabilities
- **Accountant**: Financial operations and reporting
- **Teacher**: Class and student management (limited scope)
- **Parent**: Read-only access to child's information

### Permissions
Granular permissions for each resource (create, read, update, delete) with optional scope restrictions.

## Development

### Adding New Features

1. **Backend**: Add models, schemas, services, and API endpoints
2. **Frontend**: Create hooks, components, and pages
3. **Database**: Create Alembic migrations for schema changes

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black .
isort .
flake8

# Frontend linting
cd frontend
npm run lint
```

## Production Deployment

1. **Environment Variables**: Set production values
2. **Database**: Use managed PostgreSQL service
3. **Redis**: Use managed Redis service
4. **Container Registry**: Build and push images
5. **Orchestration**: Deploy with Kubernetes or Docker Swarm
6. **Monitoring**: Set up logging and monitoring
7. **SSL**: Configure HTTPS with Let's Encrypt

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For support and questions, please contact the development team.