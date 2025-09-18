// Auth types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  id: number;
  email: string;
  phone?: string;
  school_id: number;
  staff_id?: number;
  status: string;
  roles: string[];
}

// School types
export interface School {
  id: number;
  name: string;
  slug: string;
  status: string;
  contact_email: string;
  contact_phone?: string;
  address_json?: Record<string, any>;
  verified_at?: string;
  created_at: string;
  updated_at: string;
}

export interface SchoolCreate {
  name: string;
  slug: string;
  contact_email: string;
  contact_phone?: string;
  address_json?: Record<string, any>;
}

// Class types
export interface Class {
  id: number;
  school_id: number;
  name: string;
  level?: string;
  status: string;
  created_at: string;
  updated_at: string;
  current_teacher?: string;
  enrollment_count?: number;
}

export interface ClassCreate {
  name: string;
  level?: string;
}

export interface ClassUpdate {
  name?: string;
  level?: string;
  status?: string;
}

export interface ClassTeacherAssign {
  staff_id: number;
}

// Enrollment types
export interface Enrollment {
  id: number;
  school_id: number;
  student_id: number;
  class_id: number;
  academic_year_id: number;
  enrolled_at: string;
  status: string;
  class_name?: string;
  academic_year_name?: string;
}

export interface EnrollmentCreate {
  student_id: number;
  class_id: number;
  academic_year_id?: number;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}