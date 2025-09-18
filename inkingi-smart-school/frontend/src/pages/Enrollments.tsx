import React from 'react';
import { Plus, Trash2, UserCheck } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { useEnrollments, useDeleteEnrollment } from '../hooks/useEnrollments';
import { useUIStore } from '../stores/uiStore';
import type { Enrollment } from '../types/api';

const Enrollments: React.FC = () => {
  const { data: enrollments, isLoading } = useEnrollments();
  const deleteEnrollment = useDeleteEnrollment();
  const { openEnrollmentModal, openConfirmModal } = useUIStore();

  const handleWithdrawStudent = (enrollment: Enrollment) => {
    openConfirmModal({
      title: 'Withdraw Student',
      message: `Are you sure you want to withdraw student ${enrollment.student_id} from ${enrollment.class_name || 'this class'}?`,
      type: 'warning',
      confirmText: 'Withdraw',
      onConfirm: () => deleteEnrollment.mutate(enrollment.id),
    });
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Enrollments</h1>
          <Button onClick={openEnrollmentModal}>
            <Plus className="mr-2 h-4 w-4" />
            Enroll Student
          </Button>
        </div>
        
        <Card>
          <CardContent className="p-6">
            <div className="animate-pulse space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Enrollments</h1>
          <p className="text-gray-600">Manage student enrollments in classes</p>
        </div>
        <Button onClick={openEnrollmentModal}>
          <Plus className="mr-2 h-4 w-4" />
          Enroll Student
        </Button>
      </div>

      {/* Enrollments Table */}
      {enrollments && enrollments.length > 0 ? (
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium text-gray-900">All Enrollments</h3>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Student ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Class
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Academic Year
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Enrolled Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {enrollments.map((enrollment) => (
                    <tr key={enrollment.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="font-medium text-gray-900">
                          {enrollment.student_id}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-gray-900">
                          {enrollment.class_name || `Class ID: ${enrollment.class_id}`}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-gray-900">
                          {enrollment.academic_year_name || `Year ID: ${enrollment.academic_year_id}`}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-gray-900">
                          {new Date(enrollment.enrolled_at).toLocaleDateString()}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          enrollment.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : enrollment.status === 'withdrawn'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {enrollment.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {enrollment.status === 'active' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleWithdrawStudent(enrollment)}
                            className="text-red-600 hover:text-red-700 hover:bg-red-50"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="text-center py-12">
            <UserCheck className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-4 text-lg font-medium text-gray-900">No enrollments found</h3>
            <p className="mt-2 text-gray-600">
              Start by enrolling students in classes.
            </p>
            <Button className="mt-4" onClick={openEnrollmentModal}>
              <Plus className="mr-2 h-4 w-4" />
              Enroll Student
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export { Enrollments };