'use client'

import { useEffect, useState } from 'react'

export type Toast = { id: number; title: string; description?: string; type?: 'success' | 'error' | 'info' }

export const Toaster: React.FC = () => {
  const [toasts, setToasts] = useState<Toast[]>([])

  useEffect(() => {
    const handler = (e: any) => {
      const toast: Omit<Toast, 'id'> = e.detail
      setToasts((prev) => [...prev, { id: Date.now(), ...toast }])
      setTimeout(() => setToasts((prev) => prev.slice(1)), 3500)
    }
    window.addEventListener('app:toast', handler as any)
    return () => window.removeEventListener('app:toast', handler as any)
  }, [])

  const bg = (t: Toast) => t.type === 'error' ? 'bg-red-600' : t.type === 'success' ? 'bg-green-600' : 'bg-gray-800'

  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {toasts.map((t) => (
        <div key={t.id} className={`text-white px-4 py-3 rounded shadow ${bg(t)}`}>
          <div className="font-semibold">{t.title}</div>
          {t.description && <div className="text-sm opacity-90">{t.description}</div>}
        </div>
      ))}
    </div>
  )
}

export function toast(input: Omit<Toast, 'id'>) {
  window.dispatchEvent(new CustomEvent('app:toast', { detail: input }))
}