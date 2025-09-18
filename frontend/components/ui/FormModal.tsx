'use client'

import { useEffect, useState } from 'react'

type Field = { name: string; label: string; type?: 'text' | 'number' }

export function openFormModal(options: { title: string; fields: Field[]; submitLabel?: string }): Promise<Record<string, any> | null> {
  return new Promise((resolve) => {
    window.dispatchEvent(new CustomEvent('app:form', { detail: { ...options, resolve } }))
  })
}

export default function FormModal() {
  const [open, setOpen] = useState(false)
  const [title, setTitle] = useState('')
  const [fields, setFields] = useState<Field[]>([])
  const [values, setValues] = useState<Record<string, any>>({})
  const [resolver, setResolver] = useState<(value: Record<string, any> | null) => void>(() => () => {})
  const [submitLabel, setSubmitLabel] = useState('Save')

  useEffect(() => {
    const handler = (e: any) => {
      setTitle(e.detail.title)
      setFields(e.detail.fields)
      setValues({})
      setSubmitLabel(e.detail.submitLabel || 'Save')
      setResolver(() => e.detail.resolve)
      setOpen(true)
    }
    window.addEventListener('app:form', handler as any)
    return () => window.removeEventListener('app:form', handler as any)
  }, [])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow p-6 w-full max-w-md">
        <div className="text-lg font-semibold mb-4">{title}</div>
        <div className="space-y-3">
          {fields.map((f) => (
            <div key={f.name} className="space-y-1">
              <label className="text-sm text-gray-700">{f.label}</label>
              <input
                className="w-full border rounded px-3 py-2"
                type={f.type || 'text'}
                value={values[f.name] ?? ''}
                onChange={(e) => setValues((v) => ({ ...v, [f.name]: e.target.value }))}
              />
            </div>
          ))}
        </div>
        <div className="flex justify-end gap-3 mt-5">
          <button className="px-4 py-2 rounded border" onClick={() => { setOpen(false); resolver(null) }}>Cancel</button>
          <button className="px-4 py-2 rounded bg-accent-600 text-white" onClick={() => { setOpen(false); resolver(values) }}>{submitLabel}</button>
        </div>
      </div>
    </div>
  )
}