import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { GraduationCap } from 'lucide-react'

export default function Students() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Students</h1>
        <p className="text-gray-600">Manage student records and enrollment</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <GraduationCap className="h-5 w-5 mr-2" />
            Student Management
          </CardTitle>
          <CardDescription>
            Enroll students, manage their information, and track academic progress
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <GraduationCap className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Student Management</h3>
            <p className="text-gray-500">
              This section will allow you to manage student records, enrollment, and academic information.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}