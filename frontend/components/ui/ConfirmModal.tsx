'use client'

import { useEffect, useState } from 'react'

export function confirmModal(message: string): Promise<boolean> {
  return new Promise((resolve) => {
    window.dispatchEvent(new CustomEvent('app:confirm', { detail: { message, resolve } }))
  })
}

export default function ConfirmModal() {
  const [open, setOpen] = useState(false)
  const [message, setMessage] = useState('')
  const [resolver, setResolver] = useState<(value: boolean) => void>(() => () => {})

  useEffect(() => {
    const handler = (e: any) => {
      setMessage(e.detail.message)
      setResolver(() => e.detail.resolve)
      setOpen(true)
    }
    window.addEventListener('app:confirm', handler as any)
    return () => window.removeEventListener('app:confirm', handler as any)
  }, [])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow p-6 w-full max-w-md">
        <div className="text-lg font-semibold mb-3">Confirm</div>
        <div className="text-gray-700 mb-5">{message}</div>
        <div className="flex justify-end gap-3">
          <button
            className="px-4 py-2 rounded border"
            onClick={() => { setOpen(false); resolver(false) }}
          >
            Cancel
          </button>
          <button
            className="px-4 py-2 rounded bg-brand-600 text-white"
            onClick={() => { setOpen(false); resolver(true) }}
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  )
}