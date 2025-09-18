import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Bot } from 'lucide-react'

export default function AI() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
        <p className="text-gray-600">Chat with your school's AI assistant</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bot className="h-5 w-5 mr-2" />
            AI Assistant
          </CardTitle>
          <CardDescription>
            Get insights, answer questions, and get help with school data using AI
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <Bot className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">AI Assistant</h3>
            <p className="text-gray-500">
              This section will provide an AI-powered assistant to help with school data analysis and insights.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}