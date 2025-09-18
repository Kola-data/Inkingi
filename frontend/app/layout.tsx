import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900">
        <div className="mx-auto max-w-5xl p-6">
          <header className="mb-6">
            <h1 className="text-2xl font-semibold text-brand-700">Inkingi Smart School</h1>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  )
} 