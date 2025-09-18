import Link from 'next/link'

export default function HomePage() {
  const features = [
    { name: 'Schools', href: '/schools', color: 'bg-brand-600 hover:bg-brand-700' },
    { name: 'Staff', href: '/staff', color: 'bg-accent-600 hover:bg-accent-700' },
    { name: 'Students', href: '/students', color: 'bg-brand-600 hover:bg-brand-700' },
    { name: 'Parents', href: '/parents', color: 'bg-accent-600 hover:bg-accent-700' },
    { name: 'Calendar', href: '/calendar', color: 'bg-brand-600 hover:bg-brand-700' },
    { name: 'Classes', href: '/classes', color: 'bg-accent-600 hover:bg-accent-700' },
    { name: 'Courses', href: '/courses', color: 'bg-brand-600 hover:bg-brand-700' },
    { name: 'Enrollments', href: '/enroll', color: 'bg-accent-600 hover:bg-accent-700' },
    { name: 'Timetable', href: '/timetable', color: 'bg-brand-600 hover:bg-brand-700' },
    { name: 'Marks', href: '/marks', color: 'bg-accent-600 hover:bg-accent-700' },
    { name: 'Finance', href: '/finance', color: 'bg-brand-600 hover:bg-brand-700' },
    { name: 'Inventory', href: '/inventory', color: 'bg-accent-600 hover:bg-accent-700' },
    { name: 'Messages', href: '/messages', color: 'bg-brand-600 hover:bg-brand-700' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-brand-800 mb-2">Inkingi Smart School</h1>
        <p className="text-gray-700 text-lg">Multi-tenant school management platform</p>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {features.map((feature) => (
          <Link
            key={feature.name}
            href={feature.href}
            className={`${feature.color} text-white px-4 py-3 rounded-lg text-center font-medium transition-colors`}
          >
            {feature.name}
          </Link>
        ))}
      </div>

      <div className="bg-brand-50 p-6 rounded-lg">
        <h2 className="text-xl font-semibold text-brand-800 mb-4">Quick Start</h2>
        <div className="space-y-2 text-sm text-gray-700">
          <p>1. Create an academic year and set it as current</p>
          <p>2. Add staff members and create classes</p>
          <p>3. Register students and enroll them in classes</p>
          <p>4. Set up courses and assign teachers</p>
          <p>5. Create timetables and manage marks</p>
        </div>
      </div>
    </div>
  )
} 