'use client'

import { useState } from 'react'
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

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsLoading(true)

        // Simulate API call
        setTimeout(() => {
            setIsLoading(false)
            onLogin()
        }, 500)
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <Card className="border-border/50 backdrop-blur-sm bg-card/80">
                    <div className="p-8 space-y-6">
                        {/* Header */}
                        <div className="space-y-2 text-center">
                            <div className="text-3xl font-bold bg-gradient-to-r from-primary via-primary to-accent bg-clip-text text-transparent">
                                Welcome
                            </div>
                            <p className="text-sm text-muted-foreground">
                                Sign in to access your dashboard
                            </p>
                        </div>

                        {/* Form */}
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {/* Email Input */}
                            <div className="space-y-2">
                                <Label htmlFor="email" className="text-sm font-medium">
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
                            <div className="space-y-2">
                                <Label htmlFor="password" className="text-sm font-medium">
                                    Password
                                </Label>
                                <Input
                                    id="password"
                                    type="password"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className="bg-input border-border/50 focus:border-primary"
                                />
                            </div>

                            <CustomButton
                                type="submit"
                                variant="primary"
                                size="md"
                                fullWidth
                                isLoading={isLoading}
                            >
                                {isLoading ? 'Signing in...' : 'Sign In'}
                            </CustomButton>
                        </form>

                        {/* Footer */}
                        <div className="text-center text-xs text-muted-foreground">
                            Demo account: Use Your given Credentials
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
