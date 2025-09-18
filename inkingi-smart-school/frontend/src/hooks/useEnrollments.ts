import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import type { Enrollment, EnrollmentCreate } from '../types/api';
import { toast } from 'sonner';

// Enrollments API functions
const enrollmentsApi = {
  getEnrollments: async (params?: {
    class_id?: number;
    student_id?: number;
    academic_year_id?: number;
  }): Promise<Enrollment[]> => {
    const response = await api.get('/enrollments', { params });
    return response.data;
  },

  getEnrollment: async (enrollmentId: number): Promise<Enrollment> => {
    const response = await api.get(`/enrollments/${enrollmentId}`);
    return response.data;
  },

  createEnrollment: async (enrollmentData: EnrollmentCreate): Promise<Enrollment> => {
    const response = await api.post('/enrollments', enrollmentData);
    return response.data;
  },

  deleteEnrollment: async (enrollmentId: number): Promise<void> => {
    await api.delete(`/enrollments/${enrollmentId}`);
  },
};

// Hooks
export const useEnrollments = (params?: {
  class_id?: number;
  student_id?: number;
  academic_year_id?: number;
}) => {
  return useQuery({
    queryKey: ['enrollments', params],
    queryFn: () => enrollmentsApi.getEnrollments(params),
  });
};

export const useEnrollment = (enrollmentId: number) => {
  return useQuery({
    queryKey: ['enrollments', enrollmentId],
    queryFn: () => enrollmentsApi.getEnrollment(enrollmentId),
    enabled: !!enrollmentId,
  });
};

export const useCreateEnrollment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: enrollmentsApi.createEnrollment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['enrollments'] });
      queryClient.invalidateQueries({ queryKey: ['classes'] }); // Update class enrollment counts
      toast.success('Student enrolled successfully!');
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Failed to enroll student';
      toast.error(message);
    },
  });
};

export const useDeleteEnrollment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: enrollmentsApi.deleteEnrollment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['enrollments'] });
      queryClient.invalidateQueries({ queryKey: ['classes'] });
      toast.success('Student withdrawn successfully!');
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Failed to withdraw student';
      toast.error(message);
    },
  });
};