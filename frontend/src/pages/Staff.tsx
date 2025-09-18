import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { UserCheck } from 'lucide-react'

export default function Staff() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Staff</h1>
        <p className="text-gray-600">Manage staff members and their information</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <UserCheck className="h-5 w-5 mr-2" />
            Staff Management
          </CardTitle>
          <CardDescription>
            Manage staff profiles, employment details, and assignments
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <UserCheck className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Staff Management</h3>
            <p className="text-gray-500">
              This section will allow you to manage staff members, their profiles, and employment information.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}