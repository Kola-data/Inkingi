import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { MessageSquare } from 'lucide-react'

export default function Communication() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Communication</h1>
        <p className="text-gray-600">Send messages and notifications</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <MessageSquare className="h-5 w-5 mr-2" />
            Communication Center
          </CardTitle>
          <CardDescription>
            Send emails, SMS, and notifications to students, parents, and staff
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Communication Center</h3>
            <p className="text-gray-500">
              This section will allow you to send messages, emails, and SMS notifications to various stakeholders.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}