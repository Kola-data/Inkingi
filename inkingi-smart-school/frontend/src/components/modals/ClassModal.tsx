import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from './Modal';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useUIStore } from '../../stores/uiStore';
import { useCreateClass } from '../../hooks/useClasses';
import type { ClassCreate } from '../../types/api';

const classSchema = z.object({
  name: z.string().min(1, 'Class name is required').max(100, 'Class name is too long'),
  level: z.string().optional(),
});

type ClassFormData = z.infer<typeof classSchema>;

const ClassModal: React.FC = () => {
  const { isClassModalOpen, closeClassModal } = useUIStore();
  const createClass = useCreateClass();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ClassFormData>({
    resolver: zodResolver(classSchema),
  });

  const onSubmit = async (data: ClassFormData) => {
    try {
      const classData: ClassCreate = {
        name: data.name,
        level: data.level || undefined,
      };
      
      await createClass.mutateAsync(classData);
      reset();
      closeClassModal();
    } catch (error) {
      // Error is handled by the mutation hook
    }
  };

  const handleClose = () => {
    reset();
    closeClassModal();
  };

  return (
    <Modal
      isOpen={isClassModalOpen}
      onClose={handleClose}
      title="Create New Class"
      size="md"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="Class Name"
          placeholder="e.g., P2, Grade 7A"
          error={errors.name?.message}
          {...register('name')}
        />

        <Input
          label="Level (Optional)"
          placeholder="e.g., Primary, Secondary"
          error={errors.level?.message}
          {...register('level')}
        />

        <div className="flex space-x-3 justify-end pt-4">
          <Button
            type="button"
            variant="ghost"
            onClick={handleClose}
            disabled={createClass.isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            loading={createClass.isPending}
          >
            Create Class
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export { ClassModal };