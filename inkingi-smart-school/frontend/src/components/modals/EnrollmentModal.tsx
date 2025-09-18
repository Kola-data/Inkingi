import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from './Modal';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useUIStore } from '../../stores/uiStore';
import { useCreateEnrollment } from '../../hooks/useEnrollments';
import { useClasses } from '../../hooks/useClasses';
import type { EnrollmentCreate } from '../../types/api';

const enrollmentSchema = z.object({
  student_id: z.string().min(1, 'Student ID is required'),
  class_id: z.string().min(1, 'Class is required'),
});

type EnrollmentFormData = z.infer<typeof enrollmentSchema>;

const EnrollmentModal: React.FC = () => {
  const { isEnrollmentModalOpen, closeEnrollmentModal } = useUIStore();
  const createEnrollment = useCreateEnrollment();
  const { data: classes, isLoading: classesLoading } = useClasses();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<EnrollmentFormData>({
    resolver: zodResolver(enrollmentSchema),
  });

  const onSubmit = async (data: EnrollmentFormData) => {
    try {
      const enrollmentData: EnrollmentCreate = {
        student_id: Number(data.student_id),
        class_id: Number(data.class_id),
        // academic_year_id will be set to current year by backend if not provided
      };
      
      await createEnrollment.mutateAsync(enrollmentData);
      reset();
      closeEnrollmentModal();
    } catch (error) {
      // Error is handled by the mutation hook
    }
  };

  const handleClose = () => {
    reset();
    closeEnrollmentModal();
  };

  return (
    <Modal
      isOpen={isEnrollmentModalOpen}
      onClose={handleClose}
      title="Enroll Student"
      size="md"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="Student ID"
          type="number"
          placeholder="Enter student ID"
          error={errors.student_id?.message}
          {...register('student_id')}
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Class
          </label>
          <select
            className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            {...register('class_id')}
          >
            <option value="">Select a class</option>
            {classes?.map((cls) => (
              <option key={cls.id} value={cls.id}>
                {cls.name} {cls.level && `(${cls.level})`}
              </option>
            ))}
          </select>
          {errors.class_id && (
            <p className="mt-1 text-sm text-red-600">{errors.class_id.message}</p>
          )}
        </div>

        <div className="flex space-x-3 justify-end pt-4">
          <Button
            type="button"
            variant="ghost"
            onClick={handleClose}
            disabled={createEnrollment.isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            loading={createEnrollment.isPending || classesLoading}
          >
            Enroll Student
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export { EnrollmentModal };