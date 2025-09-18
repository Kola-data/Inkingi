import { 
  Users, 
  GraduationCap, 
  BookOpen, 
  DollarSign,
  TrendingUp,
  TrendingDown,
  Calendar,
  Bell
} from 'lucide-react'

const stats = [
  { 
    name: 'Total Students', 
    value: '2,345', 
    icon: Users, 
    change: '+12%', 
    trend: 'up',
    color: 'bg-blue-500'
  },
  { 
    name: 'Total Teachers', 
    value: '142', 
    icon: GraduationCap, 
    change: '+5%', 
    trend: 'up',
    color: 'bg-green-500'
  },
  { 
    name: 'Active Courses', 
    value: '89', 
    icon: BookOpen, 
    change: '-2%', 
    trend: 'down',
    color: 'bg-purple-500'
  },
  { 
    name: 'Revenue', 
    value: '$125,430', 
    icon: DollarSign, 
    change: '+18%', 
    trend: 'up',
    color: 'bg-yellow-500'
  },
]

const recentActivities = [
  { id: 1, type: 'enrollment', message: 'John Doe enrolled in Grade 10', time: '2 hours ago' },
  { id: 2, type: 'payment', message: 'Payment received from Jane Smith', time: '3 hours ago' },
  { id: 3, type: 'course', message: 'New course "Advanced Mathematics" created', time: '5 hours ago' },
  { id: 4, type: 'teacher', message: 'Mr. Johnson joined as Math Teacher', time: '1 day ago' },
]

const upcomingEvents = [
  { id: 1, title: 'Parent-Teacher Meeting', date: 'Dec 15, 2023', time: '10:00 AM' },
  { id: 2, title: 'Mid-term Examinations', date: 'Dec 20, 2023', time: '9:00 AM' },
  { id: 3, title: 'School Annual Day', date: 'Dec 25, 2023', time: '4:00 PM' },
  { id: 4, title: 'Sports Day', date: 'Jan 5, 2024', time: '8:00 AM' },
]

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">Welcome back! Here's what's happening at your school.</p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <div className={`flex items-center text-sm ${
                stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
              }`}>
                {stat.trend === 'up' ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
                {stat.change}
              </div>
            </div>
            <div className="mt-4">
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{stat.value}</p>
              <p className="text-gray-600 dark:text-gray-400">{stat.name}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activities */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Bell className="h-5 w-5 mr-2" />
              Recent Activities
            </h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                      <div className="h-2 w-2 rounded-full bg-primary" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900 dark:text-white">
                      {activity.message}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {activity.time}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Upcoming Events */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Upcoming Events
            </h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {upcomingEvents.map((event) => (
                <div key={event.id} className="border-l-2 border-primary pl-4">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {event.title}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {event.date} at {event.time}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <Users className="h-6 w-6 mx-auto mb-2 text-primary" />
            <p className="text-sm">Add Student</p>
          </button>
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <GraduationCap className="h-6 w-6 mx-auto mb-2 text-primary" />
            <p className="text-sm">Add Teacher</p>
          </button>
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <BookOpen className="h-6 w-6 mx-auto mb-2 text-primary" />
            <p className="text-sm">Create Course</p>
          </button>
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <DollarSign className="h-6 w-6 mx-auto mb-2 text-primary" />
            <p className="text-sm">Record Payment</p>
          </button>
        </div>
      </div>
    </div>
  )
}