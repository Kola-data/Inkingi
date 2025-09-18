import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Users as UsersIcon } from 'lucide-react'

export default function Users() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Users</h1>
        <p className="text-gray-600">Manage user accounts and permissions</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <UsersIcon className="h-5 w-5 mr-2" />
            User Management
          </CardTitle>
          <CardDescription>
            Create, edit, and manage user accounts with role-based access control
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <UsersIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">User Management</h3>
            <p className="text-gray-500">
              This section will allow you to manage user accounts, assign roles, and control access permissions.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}