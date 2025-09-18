-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database if not exists
-- Note: This is handled by Docker, but included for reference
-- CREATE DATABASE inkingi_school;

-- Enable Row Level Security
ALTER DATABASE inkingi_school SET row_security = on;

-- Create custom types
CREATE TYPE school_status AS ENUM ('pending', 'active', 'suspended', 'inactive');
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended', 'deleted');
CREATE TYPE gender AS ENUM ('male', 'female', 'other');

-- Create initial roles
INSERT INTO roles (id, name, display_name, description, scope, is_system) VALUES
  (gen_random_uuid(), 'system_admin', 'System Administrator', 'Full system access', 'system', true),
  (gen_random_uuid(), 'school_admin', 'School Administrator', 'Full school access', 'school', true),
  (gen_random_uuid(), 'accountant', 'Accountant', 'Financial management access', 'school', true),
  (gen_random_uuid(), 'teacher', 'Teacher', 'Teaching and grading access', 'school', true),
  (gen_random_uuid(), 'parent', 'Parent', 'View child information', 'school', true)
ON CONFLICT DO NOTHING;

-- Create initial permissions
INSERT INTO permissions (id, name, display_name, resource, action) VALUES
  -- School permissions
  (gen_random_uuid(), 'school.create', 'Create School', 'school', 'create'),
  (gen_random_uuid(), 'school.read', 'View School', 'school', 'read'),
  (gen_random_uuid(), 'school.update', 'Update School', 'school', 'update'),
  (gen_random_uuid(), 'school.delete', 'Delete School', 'school', 'delete'),
  
  -- User permissions
  (gen_random_uuid(), 'user.create', 'Create User', 'user', 'create'),
  (gen_random_uuid(), 'user.read', 'View User', 'user', 'read'),
  (gen_random_uuid(), 'user.update', 'Update User', 'user', 'update'),
  (gen_random_uuid(), 'user.delete', 'Delete User', 'user', 'delete'),
  
  -- Class permissions
  (gen_random_uuid(), 'class.create', 'Create Class', 'class', 'create'),
  (gen_random_uuid(), 'class.read', 'View Class', 'class', 'read'),
  (gen_random_uuid(), 'class.update', 'Update Class', 'class', 'update'),
  (gen_random_uuid(), 'class.delete', 'Delete Class', 'class', 'delete'),
  
  -- Student permissions
  (gen_random_uuid(), 'student.create', 'Create Student', 'student', 'create'),
  (gen_random_uuid(), 'student.read', 'View Student', 'student', 'read'),
  (gen_random_uuid(), 'student.update', 'Update Student', 'student', 'update'),
  (gen_random_uuid(), 'student.delete', 'Delete Student', 'student', 'delete'),
  
  -- Fee permissions
  (gen_random_uuid(), 'fee.create', 'Create Fee', 'fee', 'create'),
  (gen_random_uuid(), 'fee.read', 'View Fee', 'fee', 'read'),
  (gen_random_uuid(), 'fee.update', 'Update Fee', 'fee', 'update'),
  (gen_random_uuid(), 'fee.delete', 'Delete Fee', 'fee', 'delete')
ON CONFLICT DO NOTHING;