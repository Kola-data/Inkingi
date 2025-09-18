'use client'

import { useState } from 'react'

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
    if (res.ok) setMessage('Class created')
    else setMessage('Error creating class')
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <h2 className="text-xl font-semibold">Create Class</h2>
      <input value={name} onChange={e=>setName(e.target.value)} placeholder="Class name" className="border p-2 rounded w-full" />
      <input value={level} onChange={e=>setLevel(e.target.value)} placeholder="Level (optional)" className="border p-2 rounded w-full" />
      <button className="px-4 py-2 rounded bg-brand-600 text-white">Create</button>
      {message && <p className="text-sm text-gray-600">{message}</p>}
    </form>
  )
} 