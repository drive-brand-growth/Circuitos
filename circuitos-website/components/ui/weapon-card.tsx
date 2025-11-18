"use client"

import { motion } from "framer-motion"
import { Button } from "./button"
import { cn } from "@/lib/utils"

interface WeaponCardProps {
  title: string
  description: string
  price: string
  features: string[]
  icon: string
  variant?: "free" | "pro" | "premium"
  cta: string
  onCTAClick?: () => void
}

export function WeaponCard({
  title,
  description,
  price,
  features,
  icon,
  variant = "pro",
  cta,
  onCTAClick,
}: WeaponCardProps) {
  const borderColor = {
    free: "border-[var(--circuit-green)]",
    pro: "border-[var(--circuit-red)]",
    premium: "border-[var(--circuit-gold)]",
  }[variant]

  const glowColor = {
    free: "group-hover:shadow-[0_0_40px_var(--circuit-green-glow)]",
    pro: "group-hover:shadow-[0_0_40px_var(--circuit-red-glow)]",
    premium: "group-hover:shadow-[0_0_40px_var(--circuit-gold-glow)]",
  }[variant]

  const badgeColor = {
    free: "bg-[var(--circuit-green)] text-[var(--circuit-black)]",
    pro: "bg-[var(--circuit-red)] text-[var(--circuit-black)]",
    premium: "bg-[var(--circuit-gold)] text-[var(--circuit-black)]",
  }[variant]

  return (
    <motion.div
      className="group relative h-full"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      whileHover={{
        y: -10,
        rotateY: 5,
        transition: { duration: 0.3 },
      }}
    >
      <div
        className={cn(
          "relative h-full flex flex-col bg-[var(--circuit-black-deep)]/50 backdrop-blur-sm border-2 rounded-lg p-6 transition-all duration-500",
          borderColor,
          glowColor
        )}
        style={{
          transformStyle: "preserve-3d",
        }}
      >
        {/* Icon/Emoji */}
        <div className="text-6xl mb-4">{icon}</div>

        {/* Price Badge */}
        <div className={cn("inline-flex items-center justify-center px-3 py-1 rounded-full text-xs font-bold uppercase mb-4 w-fit", badgeColor)}>
          {price}
        </div>

        {/* Title */}
        <h3 className="text-2xl font-bold uppercase mb-2 text-[var(--circuit-steel)]">
          {title}
        </h3>

        {/* Description */}
        <p className="text-[var(--circuit-steel-dark)] mb-6 flex-grow">
          {description}
        </p>

        {/* Features */}
        <ul className="space-y-2 mb-6">
          {features.map((feature, index) => (
            <li key={index} className="flex items-start gap-2 text-sm text-[var(--circuit-steel-dark)]">
              <span className="text-[var(--circuit-green)] mt-1">✓</span>
              <span>{feature}</span>
            </li>
          ))}
        </ul>

        {/* CTA Button */}
        <Button
          variant={variant === "free" ? "secondary" : "primary"}
          className="w-full"
          onClick={onCTAClick}
        >
          {cta}
        </Button>
      </div>
    </motion.div>
  )
}
