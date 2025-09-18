import { useQuery } from '@tanstack/react-query'
import { 
  Users, 
  GraduationCap, 
  BookOpen, 
  DollarSign, 
  TrendingUp, 
  Calendar,
  Award,
  MessageSquare
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { api } from '../lib/api'

const stats = [
  {
    name: 'Total Students',
    value: '1,234',
    change: '+12%',
    changeType: 'positive',
    icon: GraduationCap,
  },
  {
    name: 'Active Staff',
    value: '89',
    change: '+5%',
    changeType: 'positive',
    icon: Users,
  },
  {
    name: 'Classes',
    value: '24',
    change: '+2',
    changeType: 'positive',
    icon: BookOpen,
  },
  {
    name: 'Revenue',
    value: '$45,678',
    change: '+18%',
    changeType: 'positive',
    icon: DollarSign,
  },
]

const recentActivities = [
  {
    id: 1,
    type: 'enrollment',
    message: 'New student John Doe enrolled in Grade 5A',
    time: '2 hours ago',
  },
  {
    id: 2,
    type: 'payment',
    message: 'Payment received from Jane Smith - $500',
    time: '4 hours ago',
  },
  {
    id: 3,
    type: 'assignment',
    message: 'Math assignment graded for Grade 6B',
    time: '6 hours ago',
  },
  {
    id: 4,
    type: 'communication',
    message: 'Parent meeting scheduled for tomorrow',
    time: '8 hours ago',
  },
]

export default function Dashboard() {
  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const response = await api.get('/auth/me')
      return response.data
    },
  })

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Welcome back, {user?.email?.split('@')[0]}!
        </h1>
        <p className="text-indigo-100">
          Here's what's happening at your school today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <Card key={stat.name} className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                {stat.name}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-green-600 flex items-center">
                <TrendingUp className="h-3 w-3 mr-1" />
                {stat.change} from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activities */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Recent Activities
            </CardTitle>
            <CardDescription>
              Latest updates from your school
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="h-2 w-2 bg-indigo-600 rounded-full mt-2"></div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Award className="h-5 w-5 mr-2" />
              Quick Actions
            </CardTitle>
            <CardDescription>
              Common tasks and shortcuts
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
                <Users className="h-6 w-6 text-indigo-600 mb-2" />
                <div className="font-medium">Add Student</div>
                <div className="text-sm text-gray-500">Enroll new student</div>
              </button>
              <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
                <BookOpen className="h-6 w-6 text-indigo-600 mb-2" />
                <div className="font-medium">Create Class</div>
                <div className="text-sm text-gray-500">Set up new class</div>
              </button>
              <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
                <DollarSign className="h-6 w-6 text-indigo-600 mb-2" />
                <div className="font-medium">Record Payment</div>
                <div className="text-sm text-gray-500">Process fee payment</div>
              </button>
              <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
                <MessageSquare className="h-6 w-6 text-indigo-600 mb-2" />
                <div className="font-medium">Send Message</div>
                <div className="text-sm text-gray-500">Communicate with parents</div>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Upcoming Events */}
      <Card>
        <CardHeader>
          <CardTitle>Upcoming Events</CardTitle>
          <CardDescription>
            Important dates and deadlines
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium">Parent-Teacher Conference</h3>
                <p className="text-sm text-gray-500">Tomorrow, 2:00 PM</p>
              </div>
              <div className="text-sm text-indigo-600 font-medium">24 hours</div>
            </div>
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium">End of Term Exams</h3>
                <p className="text-sm text-gray-500">Next week</p>
              </div>
              <div className="text-sm text-indigo-600 font-medium">7 days</div>
            </div>
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium">School Holiday</h3>
                <p className="text-sm text-gray-500">December 25-26</p>
              </div>
              <div className="text-sm text-indigo-600 font-medium">15 days</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}