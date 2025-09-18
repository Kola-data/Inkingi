import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Package } from 'lucide-react'

export default function Inventory() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Inventory</h1>
        <p className="text-gray-600">Manage school inventory and assets</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Package className="h-5 w-5 mr-2" />
            Inventory Management
          </CardTitle>
          <CardDescription>
            Track school assets, manage stock levels, and monitor inventory movements
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Inventory Management</h3>
            <p className="text-gray-500">
              This section will allow you to manage school inventory, track assets, and monitor stock levels.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}