import React from 'react';
import { Plus, Edit, Trash2, Users, UserPlus, GraduationCap } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { useClasses, useDeleteClass } from '../hooks/useClasses';
import { useUIStore } from '../stores/uiStore';
import type { Class } from '../types/api';

const Classes: React.FC = () => {
  const { data: classes, isLoading } = useClasses();
  const deleteClass = useDeleteClass();
  const { openClassModal, openConfirmModal } = useUIStore();

  const handleDeleteClass = (classItem: Class) => {
    openConfirmModal({
      title: 'Delete Class',
      message: `Are you sure you want to delete "${classItem.name}"? This action cannot be undone.`,
      type: 'danger',
      confirmText: 'Delete',
      onConfirm: () => deleteClass.mutate(classItem.id),
    });
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Classes</h1>
          <Button onClick={openClassModal}>
            <Plus className="mr-2 h-4 w-4" />
            Add Class
          </Button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <div className="animate-pulse space-y-4">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  <div className="h-8 bg-gray-200 rounded w-full"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Classes</h1>
          <p className="text-gray-600">Manage your school classes and assignments</p>
        </div>
        <Button onClick={openClassModal}>
          <Plus className="mr-2 h-4 w-4" />
          Add Class
        </Button>
      </div>

      {/* Classes Grid */}
      {classes && classes.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {classes.map((classItem) => (
            <Card key={classItem.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {classItem.name}
                  </h3>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    classItem.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {classItem.status}
                  </span>
                </div>
                {classItem.level && (
                  <p className="text-sm text-gray-600">{classItem.level}</p>
                )}
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  {/* Stats */}
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center text-gray-600">
                      <Users className="mr-1 h-4 w-4" />
                      <span>{classItem.enrollment_count || 0} students</span>
                    </div>
                    {classItem.current_teacher && (
                      <div className="text-gray-600">
                        Teacher: {classItem.current_teacher}
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex-1"
                    >
                      <UserPlus className="mr-1 h-3 w-3" />
                      Enroll
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                    >
                      <Edit className="h-3 w-3" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteClass(classItem)}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="text-center py-12">
            <GraduationCap className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-4 text-lg font-medium text-gray-900">No classes found</h3>
            <p className="mt-2 text-gray-600">
              Get started by creating your first class.
            </p>
            <Button className="mt-4" onClick={openClassModal}>
              <Plus className="mr-2 h-4 w-4" />
              Add Class
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export { Classes };