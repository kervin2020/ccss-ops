'use client'

import { type ReactNode } from 'react'

interface ThemeProviderProps {
  children: ReactNode
  defaultTheme?: string
  attribute?: string
  enableSystem?: boolean
  disableTransitionOnChange?: boolean
}

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  // Simple theme provider - can be enhanced later
  return <div {...props}>{children}</div>
}
