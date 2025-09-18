# Inkingi Smart School App

A multi-tenant school management platform with role-based access control, communication tools (email/SMS), fees and inventory tracking, and an AI agent powered by each school's private data. Designed for many schools, each with isolated data, and roles including: System Admin, School Admin, Accountant, Teacher (plus Parent as a limited role).


## Why these technologies

- Backend: FastAPI (Python)
  - Pydantic v2 for robust validation, automatic OpenAPI, high performance
  - SQLAlchemy 2.x + Alembic for ORM and migrations
  - PostgreSQL with Row-Level Security (RLS) for multi-tenancy
  - Redis for caching, rate limiting, and background jobs queue
  - Celery (required) for async tasks (email/SMS, reports, ingestion) with Redis broker
- Frontend: React + Vite + TypeScript with Tailwind CSS
  - App Router for routing, SSR/ISR, excellent DX
  - TanStack Query for data fetching/caching
  - shadcn/ui + Radix UI for accessible components
  - Zustand (required) for client state

- Infra & DevOps
  - Docker + Docker Compose for local dev; Terraform + GitHub Actions for cloud
  - Nginx for reverse proxy; HTTPS with Let's Encrypt
  - Observability: Sentry (errors), OpenTelemetry + Prometheus + Grafana (metrics), Loki (logs)

This stack balances speed, maintainability, and scalability with clear choices you requested: Celery, Zustand, open-source AI, and Nginx.


## Core Features (MVP scope)

- School Management
  - Register school, verify school, grant access to school
  - Modify school details and status
- User Management (RBAC)
  - Register user, modify details and status
  - Roles: System Admin, School Admin, Accountant, Teacher (+ Parent limited)
- People Management
  - Staff-first creation (rich staff profile), then create user account with role/scopes
  - Parents and Students with meaningful personal/contact data
- Academic Calendar
  - Define academic years and terms/semesters per school
  - Set current year/term; lock past terms; copy structures across years
- Class Management
  - Create class (e.g., P2)
  - Assign class to a teacher (homeroom)
  - Enroll students into class for the current academic year
- Course Management
  - Create course, assign course to teacher (by staff)
- Timetable Management
  - Define periods/slots, rooms; generate weekly timetable per class and course
  - Assign teachers and rooms to periods; conflict detection (teacher/room/student)
  - Publish timetable to web and PDF/ICS export
- Marks Management
  - Assignment marks and Exam marks as separate entities
  - Report table combines assignment and exam marks per student/course/term
  - Modify marks and recompute reports
- Fees Management
  - Create fee structure, modify status, record fee for student
- Inventory Management
  - Create inventory, modify inventory, create item, modify status
- Communication
  - Email and SMS to one or many users/parents
- AI Agent (per-tenant)
  - Chat with school data (Q&A), summarize reports, draft communications


## Multi-Tenancy Design

- Isolation Strategy: Row-Level Security (RLS) in PostgreSQL on `tenant_id` (a.k.a. `school_id`).
  - Every row in multi-tenant tables includes `tenant_id`.
  - DB policies enforce `current_setting('app.tenant_id') = tenant_id`.
  - API layer sets `app.tenant_id` per request after domain/subdomain or token claims are validated.
- Domain Strategy: `schoolSlug.app.com` or custom domain mapping table.
- Super Admin (System Admin) can query across tenants but only through privileged services/functions.
- Optional: If required in the future, support schema-per-tenant for heavy isolation.


## RBAC and Access Control Model

- Tables: `roles`, `permissions`, `role_permissions`, `user_roles`, optional `user_permissions` overrides.
- Access scope table for fine-grained restrictions (optional, per user):
  - `access_control_entries(id, school_id, user_id, scope_type, scope_id, created_at)`
  - `scope_type` ∈ {`school`, `class`, `course`}
- Default Roles and high-level capabilities:
  - System Admin: manage platform, verify schools, billing, cross-tenant ops
  - School Admin: manage school setup, staff, classes, courses, fees, inventory, communications
  - Accountant: fees, payments, invoices, financial reports
  - Teacher: classes, courses, marks, timetable, communicate with assigned students/parents
  - Parent: view child progress, fees, communications (read + limited actions)


## High-Level Architecture

- Client (Next.js) → API Gateway/Proxy → FastAPI services
- FastAPI services split by bounded contexts:
  - Identity & Access (auth, RBAC, tenants, access scopes)
  - Academic Calendar (years, terms)
  - Academics (classes, courses, marks, enrollment, timetable)
  - People (staff, users, parents, students)
  - Finance (fees, payments, invoices)
  - Inventory (warehouses, items, stock movements)
  - Communication (email, SMS, notifications)
  - AI Agent (RAG pipelines, chat sessions)
- Data: PostgreSQL (with pgvector), Redis, S3-compatible storage (file uploads)
- Workers: Celery consumers for async tasks


## Data Model (indicative)

- Tenancy & Identity
  - `schools(id, name, slug, status, verified_at, contact_email, contact_phone, address_json, created_at, updated_at)`
  - `staff(id, school_id, first_name, last_name, other_names, gender, dob, national_id, phone, email, address_json, employment_no, position, department, qualification, hire_date, contract_type, status, created_at, updated_at)`
  - `users(id, school_id, staff_id NULLABLE, email, phone, password_hash, status, last_login_at, created_at, updated_at)`
  - `roles(id, name, scope)` and `user_roles(user_id, role_id, school_id)`
  - `access_control_entries(id, school_id, user_id, scope_type, scope_id, created_at)`
- Academic Calendar
  - `academic_years(id, school_id, name, start_date, end_date, is_current, created_at, updated_at)`  # e.g., 2025/2026
  - `terms(id, school_id, academic_year_id, name, start_date, end_date, order_index, is_current, locked, created_at, updated_at)`  # e.g., Term 1, 2, 3
- Academics (classes only per your request)
  - `classes(id, school_id, name, level, status, created_at, updated_at)`  # e.g., P2
  - `class_teachers(id, school_id, class_id, staff_id, assigned_at)`
  - `enrollments(student_id, class_id, school_id, academic_year_id, enrolled_at, status)`  # defaults to current academic year

Notes:
- Enrollment must reference the current `academic_year_id` by default if not provided.


## API Surface (focused on your scope)

- Classes
  - POST `/classes` (create class)
  - POST `/classes/{classId}/assign-teacher` (assign class to teacher)
- Enrollments
  - POST `/enrollments` with `student_id`, `class_id`
    - If `academic_year_id` omitted, server resolves to current year for the school

Server behavior:
- Current academic year is resolved from `academic_years.is_current = true` for the tenant; if none, 409 error until set.
- Assigning class teacher creates or updates a single active assignment; historical entries kept with timestamps.


## Local Development, Security, and other sections

Unchanged from earlier sections; see above for full details on setup, security, and roadmap. 