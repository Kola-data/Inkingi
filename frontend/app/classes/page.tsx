'use client'

import { useState } from 'react'
import { toast } from '../../components/ui/Toaster'
import { openFormModal } from '../../components/ui/FormModal'

export default function ClassesPage() {
  const [name, setName] = useState('')
  const [level, setLevel] = useState('')
  const [message, setMessage] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/classes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-School-ID': '1',
      },
      body: JSON.stringify({ name, level: level || null })
    })
    if (res.ok) {
      setMessage('Class created')
      toast({ title: 'Class created', type: 'success' })
    } else {
      setMessage('Error creating class')
      toast({ title: 'Failed to create class', type: 'error' })
    }
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Create Class</h2>
      <form onSubmit={submit} className="space-y-4">
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Class name" className="border p-2 rounded w-full" />
        <input value={level} onChange={e=>setLevel(e.target.value)} placeholder="Level (optional)" className="border p-2 rounded w-full" />
        <button className="px-4 py-2 rounded bg-brand-600 text-white">Create</button>
        {message && <p className="text-sm text-gray-600">{message}</p>}
      </form>

      <div>
        <button
          className="px-4 py-2 rounded bg-accent-600 text-white"
          onClick={async () => {
            const values = await openFormModal({
              title: 'Create Class (Modal)',
              fields: [
                { name: 'name', label: 'Name' },
                { name: 'level', label: 'Level (optional)' },
              ],
              submitLabel: 'Create'
            })
            if (values) {
              setName(values.name ?? '')
              setLevel(values.level ?? '')
            }
          }}
        >
          Open Form Modal
        </button>
      </div>
    </div>
  )
} 