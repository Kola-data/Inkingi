import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Search, MoreVertical, Edit, Trash2, CheckCircle } from 'lucide-react'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog'
import { Label } from '../components/ui/label'
import { api } from '../lib/api'
import toast from 'react-hot-toast'

interface School {
  id: number
  name: string
  slug: string
  contact_email: string
  contact_phone?: string
  status: string
  verified_at?: string
  created_at: string
}

export default function Schools() {
  const [searchTerm, setSearchTerm] = useState('')
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [editingSchool, setEditingSchool] = useState<School | null>(null)
  const queryClient = useQueryClient()

  const { data: schools = [], isLoading } = useQuery({
    queryKey: ['schools'],
    queryFn: async () => {
      const response = await api.get('/schools')
      return response.data
    },
  })

  const createSchoolMutation = useMutation({
    mutationFn: async (schoolData: any) => {
      const response = await api.post('/schools', schoolData)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schools'] })
      setIsCreateDialogOpen(false)
      toast.success('School created successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create school')
    },
  })

  const updateSchoolMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: any }) => {
      const response = await api.put(`/schools/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schools'] })
      setEditingSchool(null)
      toast.success('School updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update school')
    },
  })

  const filteredSchools = schools.filter((school: School) =>
    school.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    school.contact_email.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleCreateSchool = (data: any) => {
    createSchoolMutation.mutate(data)
  }

  const handleUpdateSchool = (data: any) => {
    if (editingSchool) {
      updateSchoolMutation.mutate({ id: editingSchool.id, data })
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Schools</h1>
          <p className="text-gray-600">Manage school information and settings</p>
        </div>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button className="flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Add School</span>
            </Button>
          </DialogTrigger>
          <CreateSchoolDialog onSubmit={handleCreateSchool} />
        </Dialog>
      </div>

      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search schools..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSchools.map((school: School) => (
          <Card key={school.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{school.name}</CardTitle>
                  <CardDescription>{school.contact_email}</CardDescription>
                </div>
                <div className="flex items-center space-x-2">
                  {school.status === 'active' && (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setEditingSchool(school)}
                  >
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Status:</span>
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    school.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {school.status}
                  </span>
                </div>
                {school.contact_phone && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Phone:</span>
                    <span>{school.contact_phone}</span>
                  </div>
                )}
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Created:</span>
                  <span>{new Date(school.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {editingSchool && (
        <Dialog open={!!editingSchool} onOpenChange={() => setEditingSchool(null)}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit School</DialogTitle>
              <DialogDescription>
                Update school information and settings.
              </DialogDescription>
            </DialogHeader>
            <EditSchoolDialog 
              school={editingSchool} 
              onSubmit={handleUpdateSchool}
              onCancel={() => setEditingSchool(null)}
            />
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}

function CreateSchoolDialog({ onSubmit }: { onSubmit: (data: any) => void }) {
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    contact_email: '',
    contact_phone: '',
    website: '',
    description: '',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Create New School</DialogTitle>
        <DialogDescription>
          Add a new school to the platform.
        </DialogDescription>
      </DialogHeader>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">School Name</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="slug">Slug</Label>
          <Input
            id="slug"
            value={formData.slug}
            onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="contact_email">Contact Email</Label>
          <Input
            id="contact_email"
            type="email"
            value={formData.contact_email}
            onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="contact_phone">Contact Phone</Label>
          <Input
            id="contact_phone"
            value={formData.contact_phone}
            onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="website">Website</Label>
          <Input
            id="website"
            value={formData.website}
            onChange={(e) => setFormData({ ...formData, website: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="description">Description</Label>
          <Input
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          />
        </div>
        <DialogFooter>
          <Button type="submit">Create School</Button>
        </DialogFooter>
      </form>
    </DialogContent>
  )
}

function EditSchoolDialog({ 
  school, 
  onSubmit, 
  onCancel 
}: { 
  school: School
  onSubmit: (data: any) => void
  onCancel: () => void
}) {
  const [formData, setFormData] = useState({
    name: school.name,
    contact_email: school.contact_email,
    contact_phone: school.contact_phone || '',
    status: school.status,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">School Name</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="contact_email">Contact Email</Label>
        <Input
          id="contact_email"
          type="email"
          value={formData.contact_email}
          onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="contact_phone">Contact Phone</Label>
        <Input
          id="contact_phone"
          value={formData.contact_phone}
          onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="status">Status</Label>
        <select
          id="status"
          value={formData.status}
          onChange={(e) => setFormData({ ...formData, status: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="pending">Pending</option>
          <option value="active">Active</option>
          <option value="suspended">Suspended</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
      <DialogFooter>
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">Update School</Button>
      </DialogFooter>
    </form>
  )
}