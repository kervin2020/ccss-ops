'use client'

import { useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'

interface LoginPageProps {
  onLogin: () => void
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const { authAPI } = await import('@/lib/api')
      await authAPI.login(email, password)
      onLogin()
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Card className="border-border/50 backdrop-blur-sm bg-card/80">
          <div className="p-8 space-y-6">
            {/* Header */}
            <div className="space-y-2 text-center">
              <div className="text-3xl font-bold bg-gradient-to-r from-primary via-primary to-accent bg-clip-text text-transparent">
                <p className="text-gray-800">Welcome </p>
                <p>to</p>
                <span className="text-gray-800">CCSS</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Sign in to access your workspace
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email Input */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-sm font-bold">
                  Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="bg-input border-border/50 focus:border-primary"
                />
              </div>

              {/* Password Input */}
              <div className="space-y-2 relative">
                <Label htmlFor="password" className="text-sm font-bold">
                  Password
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="bg-input border-border/50 focus:border-primary pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-2 flex items-center justify-center text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              </div>

              <CustomButton
                type="submit"
                variant="primary"
                size="md"
                fullWidth
                isLoading={isLoading}
                className="bg-red-600 hover:bg-[#cd2517] text-white"
              >
                {isLoading ? 'Signing in...' : 'Sign In'}
              </CustomButton>
            </form>

            {/* Footer */}
            <div className="text-center text-xs text-muted-foreground">
              Demo account: Use your given credentials
            </div>
          </div>
        </Card>

        {/* Decorative elements */}
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full blur-3xl -z-10" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent/10 rounded-full blur-3xl -z-10" />
      </div>
    </div>
  )
}
