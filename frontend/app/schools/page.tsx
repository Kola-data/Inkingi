'use client'

import { useState, useEffect } from 'react'

export default function SchoolsPage() {
  const [schools, setSchools] = useState([])
  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState({ name: '', slug: '', contact_email: '', contact_phone: '' })
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchSchools()
  }, [])

  const fetchSchools = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/schools`)
      if (res.ok) {
        const data = await res.json()
        setSchools(data)
      }
    } catch (error) {
      console.error('Error fetching schools:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/schools`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      if (res.ok) {
        setMessage('School created successfully')
        setFormData({ name: '', slug: '', contact_email: '', contact_phone: '' })
        fetchSchools()
      } else {
        setMessage('Error creating school')
      }
    } catch (error) {
      setMessage('Error creating school')
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-brand-800">Schools Management</h1>
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg border space-y-4">
        <h2 className="text-lg font-semibold">Create New School</h2>
        <div className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="School Name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            className="border p-2 rounded"
            required
          />
          <input
            type="text"
            placeholder="Slug (URL-friendly)"
            value={formData.slug}
            onChange={(e) => setFormData({...formData, slug: e.target.value})}
            className="border p-2 rounded"
            required
          />
          <input
            type="email"
            placeholder="Contact Email"
            value={formData.contact_email}
            onChange={(e) => setFormData({...formData, contact_email: e.target.value})}
            className="border p-2 rounded"
          />
          <input
            type="tel"
            placeholder="Contact Phone"
            value={formData.contact_phone}
            onChange={(e) => setFormData({...formData, contact_phone: e.target.value})}
            className="border p-2 rounded"
          />
        </div>
        <button type="submit" className="bg-brand-600 text-white px-4 py-2 rounded hover:bg-brand-700">
          Create School
        </button>
        {message && <p className="text-sm text-gray-600">{message}</p>}
      </form>

      <div className="bg-white p-6 rounded-lg border">
        <h2 className="text-lg font-semibold mb-4">Existing Schools</h2>
        {schools.length === 0 ? (
          <p className="text-gray-500">No schools found</p>
        ) : (
          <div className="grid gap-4">
            {schools.map((school: any) => (
              <div key={school.id} className="border p-4 rounded">
                <h3 className="font-semibold">{school.name}</h3>
                <p className="text-sm text-gray-600">Slug: {school.slug}</p>
                <p className="text-sm text-gray-600">Email: {school.contact_email}</p>
                <p className="text-sm text-gray-600">Phone: {school.contact_phone}</p>
                <p className="text-sm text-gray-600">Status: {school.status}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
} 