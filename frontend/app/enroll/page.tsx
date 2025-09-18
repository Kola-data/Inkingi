'use client'

import { useState } from 'react'
import { toast } from '../../components/ui/Toaster'
import { confirmModal } from '../../components/ui/ConfirmModal'

export default function EnrollPage() {
  const [studentId, setStudentId] = useState('')
  const [classId, setClassId] = useState('')
  const [message, setMessage] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    const proceed = await confirmModal('Are you sure you want to enroll this student?')
    if (!proceed) return
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/enrollments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-School-ID': '1',
      },
      body: JSON.stringify({ student_id: Number(studentId), class_id: Number(classId) })
    })
    if (res.ok) {
      setMessage('Enrollment created')
      toast({ title: 'Enrollment created', type: 'success' })
    } else {
      setMessage('Error creating enrollment (ensure current academic year set)')
      toast({ title: 'Enrollment failed', type: 'error' })
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <h2 className="text-xl font-semibold">Enroll Student</h2>
      <input value={studentId} onChange={e=>setStudentId(e.target.value)} placeholder="Student ID" className="border p-2 rounded w-full" />
      <input value={classId} onChange={e=>setClassId(e.target.value)} placeholder="Class ID" className="border p-2 rounded w-full" />
      <button className="px-4 py-2 rounded bg-accent-600 text-white">Enroll</button>
      {message && <p className="text-sm text-gray-600">{message}</p>}
    </form>
  )
} 