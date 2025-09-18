import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { BookOpen } from 'lucide-react'

export default function Classes() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Classes</h1>
        <p className="text-gray-600">Manage classes and student enrollment</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BookOpen className="h-5 w-5 mr-2" />
            Class Management
          </CardTitle>
          <CardDescription>
            Create and manage classes, assign teachers, and enroll students
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Class Management</h3>
            <p className="text-gray-500">
              This section will allow you to create classes, assign teachers, and manage student enrollment.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}