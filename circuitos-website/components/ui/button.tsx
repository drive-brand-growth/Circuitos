"use client"

import { ButtonHTMLAttributes, forwardRef } from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost"
  size?: "sm" | "md" | "lg"
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          // Base styles
          "relative inline-flex items-center justify-center font-semibold uppercase tracking-wider transition-all duration-300 ease-out disabled:opacity-50 disabled:cursor-not-allowed",

          // Size variants
          {
            "px-4 py-2 text-sm": size === "sm",
            "px-6 py-3 text-base": size === "md",
            "px-8 py-4 text-lg": size === "lg",
          },

          // Variant styles
          {
            // Primary: Red glow button
            "bg-[var(--circuit-red)] text-[var(--circuit-black)] hover:shadow-[0_0_30px_var(--circuit-red-glow)] hover:-translate-y-1 active:translate-y-0":
              variant === "primary",

            // Secondary: Steel outline
            "border-2 border-[var(--circuit-steel-dark)] text-[var(--circuit-steel)] hover:border-[var(--circuit-red)] hover:text-[var(--circuit-red)] hover:shadow-[0_0_20px_var(--circuit-red-glow)]":
              variant === "secondary",

            // Ghost: Minimal
            "text-[var(--circuit-steel)] hover:text-[var(--circuit-red)]":
              variant === "ghost",
          },

          className
        )}
        {...props}
      >
        {children}
      </button>
    )
  }
)

Button.displayName = "Button"

export { Button }
