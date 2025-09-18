import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { BookOpen } from 'lucide-react'

export default function Courses() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Courses</h1>
        <p className="text-gray-600">Manage courses and curriculum</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BookOpen className="h-5 w-5 mr-2" />
            Course Management
          </CardTitle>
          <CardDescription>
            Create and manage courses, assign teachers, and set up curriculum
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Course Management</h3>
            <p className="text-gray-500">
              This section will allow you to create courses, assign teachers, and manage curriculum.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}