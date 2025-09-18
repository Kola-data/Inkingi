import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { authService } from '@/services/auth-service'

const registerSchema = z.object({
  schoolName: z.string().min(3, 'School name must be at least 3 characters'),
  schoolSlug: z.string()
    .min(3, 'School code must be at least 3 characters')
    .regex(/^[a-z0-9-]+$/, 'School code must contain only lowercase letters, numbers, and hyphens'),
  email: z.string().email('Invalid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string(),
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  phone: z.string().optional(),
  address: z.string().min(5, 'Address is required'),
  city: z.string().min(2, 'City is required'),
  country: z.string().min(2, 'Country is required'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function RegisterPage() {
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState(1)
  const navigate = useNavigate()
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    trigger,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterFormData) => {
    setLoading(true)
    try {
      const response = await authService.register({
        schoolName: data.schoolName,
        schoolSlug: data.schoolSlug,
        email: data.email,
        password: data.password,
        firstName: data.firstName,
        lastName: data.lastName,
        phone: data.phone,
        address: data.address,
        city: data.city,
        country: data.country,
      })
      
      toast.success(response.message)
      navigate('/login')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const nextStep = async () => {
    const fieldsToValidate = step === 1 
      ? ['schoolName', 'schoolSlug', 'address', 'city', 'country'] as const
      : ['firstName', 'lastName', 'email', 'phone'] as const
    
    const isValid = await trigger(fieldsToValidate)
    if (isValid) {
      setStep(step + 1)
    }
  }

  const prevStep = () => {
    setStep(step - 1)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-center mb-2">Register Your School</h2>
      <p className="text-center text-gray-600 dark:text-gray-400 mb-6">
        Step {step} of 3
      </p>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {step === 1 && (
          <>
            <div>
              <label htmlFor="schoolName" className="block text-sm font-medium mb-1">
                School Name
              </label>
              <Input
                id="schoolName"
                type="text"
                placeholder="Inkingi High School"
                {...register('schoolName')}
              />
              {errors.schoolName && (
                <p className="text-red-500 text-sm mt-1">{errors.schoolName.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="schoolSlug" className="block text-sm font-medium mb-1">
                School Code
              </label>
              <Input
                id="schoolSlug"
                type="text"
                placeholder="inkingi-high"
                {...register('schoolSlug')}
              />
              <p className="text-xs text-gray-500 mt-1">
                This will be used as your school's unique identifier
              </p>
              {errors.schoolSlug && (
                <p className="text-red-500 text-sm mt-1">{errors.schoolSlug.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="address" className="block text-sm font-medium mb-1">
                Address
              </label>
              <Input
                id="address"
                type="text"
                placeholder="123 School Street"
                {...register('address')}
              />
              {errors.address && (
                <p className="text-red-500 text-sm mt-1">{errors.address.message}</p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="city" className="block text-sm font-medium mb-1">
                  City
                </label>
                <Input
                  id="city"
                  type="text"
                  placeholder="Kigali"
                  {...register('city')}
                />
                {errors.city && (
                  <p className="text-red-500 text-sm mt-1">{errors.city.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="country" className="block text-sm font-medium mb-1">
                  Country
                </label>
                <Input
                  id="country"
                  type="text"
                  placeholder="Rwanda"
                  {...register('country')}
                />
                {errors.country && (
                  <p className="text-red-500 text-sm mt-1">{errors.country.message}</p>
                )}
              </div>
            </div>

            <Button
              type="button"
              className="w-full"
              onClick={nextStep}
            >
              Next
            </Button>
          </>
        )}

        {step === 2 && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="firstName" className="block text-sm font-medium mb-1">
                  First Name
                </label>
                <Input
                  id="firstName"
                  type="text"
                  placeholder="John"
                  {...register('firstName')}
                />
                {errors.firstName && (
                  <p className="text-red-500 text-sm mt-1">{errors.firstName.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="lastName" className="block text-sm font-medium mb-1">
                  Last Name
                </label>
                <Input
                  id="lastName"
                  type="text"
                  placeholder="Doe"
                  {...register('lastName')}
                />
                {errors.lastName && (
                  <p className="text-red-500 text-sm mt-1">{errors.lastName.message}</p>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-1">
                Admin Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="admin@school.com"
                {...register('email')}
              />
              {errors.email && (
                <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium mb-1">
                Phone Number (Optional)
              </label>
              <Input
                id="phone"
                type="tel"
                placeholder="+250 788 123 456"
                {...register('phone')}
              />
              {errors.phone && (
                <p className="text-red-500 text-sm mt-1">{errors.phone.message}</p>
              )}
            </div>

            <div className="flex gap-4">
              <Button
                type="button"
                variant="outline"
                className="flex-1"
                onClick={prevStep}
              >
                Back
              </Button>
              <Button
                type="button"
                className="flex-1"
                onClick={nextStep}
              >
                Next
              </Button>
            </div>
          </>
        )}

        {step === 3 && (
          <>
            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-1">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                {...register('password')}
              />
              {errors.password && (
                <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
                Confirm Password
              </label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="••••••••"
                {...register('confirmPassword')}
              />
              {errors.confirmPassword && (
                <p className="text-red-500 text-sm mt-1">{errors.confirmPassword.message}</p>
              )}
            </div>

            <div className="flex gap-4">
              <Button
                type="button"
                variant="outline"
                className="flex-1"
                onClick={prevStep}
                disabled={loading}
              >
                Back
              </Button>
              <Button
                type="submit"
                className="flex-1"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Registering...
                  </>
                ) : (
                  'Register'
                )}
              </Button>
            </div>
          </>
        )}
      </form>

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Already have an account?{' '}
          <Link to="/login" className="text-primary hover:underline font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}