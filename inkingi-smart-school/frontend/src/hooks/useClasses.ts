import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import type { Class, ClassCreate, ClassUpdate, ClassTeacherAssign } from '../types/api';
import { toast } from 'sonner';

// Classes API functions
const classesApi = {
  getClasses: async (): Promise<Class[]> => {
    const response = await api.get('/classes');
    return response.data;
  },

  getClass: async (classId: number): Promise<Class> => {
    const response = await api.get(`/classes/${classId}`);
    return response.data;
  },

  createClass: async (classData: ClassCreate): Promise<Class> => {
    const response = await api.post('/classes', classData);
    return response.data;
  },

  updateClass: async ({ classId, data }: { classId: number; data: ClassUpdate }): Promise<Class> => {
    const response = await api.put(`/classes/${classId}`, data);
    return response.data;
  },

  deleteClass: async (classId: number): Promise<void> => {
    await api.delete(`/classes/${classId}`);
  },

  assignTeacher: async ({ classId, staffId }: { classId: number; staffId: number }): Promise<void> => {
    const data: ClassTeacherAssign = { staff_id: staffId };
    await api.post(`/classes/${classId}/assign-teacher`, data);
  },
};

// Hooks
export const useClasses = () => {
  return useQuery({
    queryKey: ['classes'],
    queryFn: classesApi.getClasses,
  });
};

export const useClass = (classId: number) => {
  return useQuery({
    queryKey: ['classes', classId],
    queryFn: () => classesApi.getClass(classId),
    enabled: !!classId,
  });
};

export const useCreateClass = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: classesApi.createClass,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['classes'] });
      toast.success('Class created successfully!');
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Failed to create class';
      toast.error(message);
    },
  });
};

export const useUpdateClass = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: classesApi.updateClass,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['classes'] });
      queryClient.invalidateQueries({ queryKey: ['classes', variables.classId] });
      toast.success('Class updated successfully!');
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Failed to update class';
      toast.error(message);
    },
  });
};

export const useDeleteClass = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: classesApi.deleteClass,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['classes'] });
      toast.success('Class deleted successfully!');
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Failed to delete class';
      toast.error(message);
    },
  });
};

export const useAssignTeacher = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: classesApi.assignTeacher,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['classes'] });
      queryClient.invalidateQueries({ queryKey: ['classes', variables.classId] });
      toast.success('Teacher assigned successfully!');
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Failed to assign teacher';
      toast.error(message);
    },
  });
};