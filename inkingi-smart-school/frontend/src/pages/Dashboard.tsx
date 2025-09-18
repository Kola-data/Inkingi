import React from 'react';
import { GraduationCap, Users, UserCheck, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader } from '../components/ui/Card';
import { useClasses } from '../hooks/useClasses';
import { useEnrollments } from '../hooks/useEnrollments';

const Dashboard: React.FC = () => {
  const { data: classes, isLoading: classesLoading } = useClasses();
  const { data: enrollments, isLoading: enrollmentsLoading } = useEnrollments();

  const stats = [
    {
      name: 'Total Classes',
      value: classes?.length || 0,
      icon: GraduationCap,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      loading: classesLoading,
    },
    {
      name: 'Active Enrollments',
      value: enrollments?.filter(e => e.status === 'active').length || 0,
      icon: UserCheck,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      loading: enrollmentsLoading,
    },
    {
      name: 'Total Students',
      value: new Set(enrollments?.filter(e => e.status === 'active').map(e => e.student_id)).size || 0,
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      loading: enrollmentsLoading,
    },
    {
      name: 'Growth Rate',
      value: '12%',
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
      loading: false,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to your school management dashboard</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stat.loading ? '...' : stat.value}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Classes */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium text-gray-900">Recent Classes</h3>
          </CardHeader>
          <CardContent>
            {classesLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  </div>
                ))}
              </div>
            ) : classes && classes.length > 0 ? (
              <div className="space-y-3">
                {classes.slice(0, 5).map((cls) => (
                  <div key={cls.id} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{cls.name}</p>
                      <p className="text-sm text-gray-500">
                        {cls.level} • {cls.enrollment_count || 0} students
                      </p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      cls.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {cls.status}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No classes found</p>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <button className="w-full text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="font-medium text-gray-900">Create New Class</div>
                <div className="text-sm text-gray-500">Add a new class to your school</div>
              </button>
              <button className="w-full text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="font-medium text-gray-900">Enroll Student</div>
                <div className="text-sm text-gray-500">Enroll a student in a class</div>
              </button>
              <button className="w-full text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="font-medium text-gray-900">Generate Report</div>
                <div className="text-sm text-gray-500">Create attendance and grade reports</div>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export { Dashboard };