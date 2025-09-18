'use client'

import { useState, useEffect } from 'react'

export default function StaffPage() {
  const [staff, setStaff] = useState([])
  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState({ 
    first_name: '', 
    last_name: '', 
    email: '', 
    phone: '', 
    position: '' 
  })
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchStaff()
  }, [])

  const fetchStaff = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/staff`, {
        headers: { 'X-School-ID': '1' }
      })
      if (res.ok) {
        const data = await res.json()
        setStaff(data)
      }
    } catch (error) {
      console.error('Error fetching staff:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/staff`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-School-ID': '1'
        },
        body: JSON.stringify(formData)
      })
      if (res.ok) {
        setMessage('Staff member created successfully')
        setFormData({ first_name: '', last_name: '', email: '', phone: '', position: '' })
        fetchStaff()
      } else {
        setMessage('Error creating staff member')
      }
    } catch (error) {
      setMessage('Error creating staff member')
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-brand-800">Staff Management</h1>
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg border space-y-4">
        <h2 className="text-lg font-semibold">Add New Staff Member</h2>
        <div className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="First Name"
            value={formData.first_name}
            onChange={(e) => setFormData({...formData, first_name: e.target.value})}
            className="border p-2 rounded"
            required
          />
          <input
            type="text"
            placeholder="Last Name"
            value={formData.last_name}
            onChange={(e) => setFormData({...formData, last_name: e.target.value})}
            className="border p-2 rounded"
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className="border p-2 rounded"
          />
          <input
            type="tel"
            placeholder="Phone"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            className="border p-2 rounded"
          />
          <input
            type="text"
            placeholder="Position"
            value={formData.position}
            onChange={(e) => setFormData({...formData, position: e.target.value})}
            className="border p-2 rounded col-span-2"
          />
        </div>
        <button type="submit" className="bg-brand-600 text-white px-4 py-2 rounded hover:bg-brand-700">
          Add Staff Member
        </button>
        {message && <p className="text-sm text-gray-600">{message}</p>}
      </form>

      <div className="bg-white p-6 rounded-lg border">
        <h2 className="text-lg font-semibold mb-4">Staff Members</h2>
        {staff.length === 0 ? (
          <p className="text-gray-500">No staff members found</p>
        ) : (
          <div className="grid gap-4">
            {staff.map((member: any) => (
              <div key={member.id} className="border p-4 rounded">
                <h3 className="font-semibold">{member.first_name} {member.last_name}</h3>
                <p className="text-sm text-gray-600">Position: {member.position}</p>
                <p className="text-sm text-gray-600">Email: {member.email}</p>
                <p className="text-sm text-gray-600">Phone: {member.phone}</p>
                <p className="text-sm text-gray-600">Status: {member.status}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
} 