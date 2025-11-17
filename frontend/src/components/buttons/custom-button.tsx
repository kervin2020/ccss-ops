import React from 'react'
import { cn } from '@/lib/utils'

interface CustomButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  icon?: React.ReactNode
  fullWidth?: boolean
}

export const CustomButton = React.forwardRef<HTMLButtonElement, CustomButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      icon,
      fullWidth = false,
      className,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    // Base styles
    const baseStyles = 'inline-flex items-center justify-center gap-2 font-medium rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'

    // Size variants
    const sizeStyles = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2.5 text-base',
      lg: 'px-6 py-3 text-lg',
    }

    // Color variants
    const variantStyles = {
      primary:
        'bg-primary text-primary-foreground hover:bg-primary/90 active:bg-primary/80 shadow-md hover:shadow-lg',
      secondary:
        'bg-secondary text-secondary-foreground hover:bg-secondary/90 active:bg-secondary/80 border border-border/50',
      outline:
        'border-2 border-primary text-primary hover:bg-primary/10 active:bg-primary/20',
      ghost: 'text-foreground hover:bg-secondary/50 active:bg-secondary/70',
      danger:
        'bg-destructive text-destructive-foreground hover:bg-destructive/90 active:bg-destructive/80 shadow-md hover:shadow-lg',
      success:
        'bg-accent text-accent-foreground hover:bg-accent/90 active:bg-accent/80 shadow-md hover:shadow-lg',
    }

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          baseStyles,
          sizeStyles[size],
          variantStyles[variant],
          fullWidth && 'w-full',
          className
        )}
        {...props}
      >
        {isLoading ? (
          <>
            <svg
              className="h-4 w-4 animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span>Loading...</span>
          </>
        ) : (
          <>
            {icon && icon}
            {children}
          </>
        )}
      </button>
    )
  }
)

CustomButton.displayName = 'CustomButton'
