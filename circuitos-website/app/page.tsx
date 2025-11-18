"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { WeaponCard } from "@/components/ui/weapon-card"
import { useState, useEffect } from "react"

export default function Home() {
  const [typedText, setTypedText] = useState("")
  const fullText = "COMMAND REVENUE. ELIMINATE CHAOS."

  useEffect(() => {
    let index = 0
    const timer = setInterval(() => {
      if (index < fullText.length) {
        setTypedText(fullText.slice(0, index + 1))
        index++
      } else {
        clearInterval(timer)
      }
    }, 50)

    return () => clearInterval(timer)
  }, [])

  return (
    <main className="min-h-screen bg-[var(--circuit-black)]">
      {/* Animated Grid Background */}
      <div className="grid-background" />

      {/* HERO SECTION - StoryBrand: Character + Problem */}
      <section className="relative min-h-screen flex items-center justify-center px-4 py-20">
        <div className="max-w-6xl mx-auto text-center">
          {/* Typing Animation */}
          <motion.div
            className="mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold uppercase text-[var(--circuit-steel)] mb-4">
              {typedText}
              <span className="typing-cursor"></span>
            </h1>
          </motion.div>

          {/* Subtitle */}
          <motion.p
            className="text-xl md:text-2xl text-[var(--circuit-steel-dark)] mb-4 uppercase tracking-wide"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.5, duration: 0.5 }}
          >
            The Operator's Weapon System
          </motion.p>

          <motion.p
            className="text-lg md:text-xl text-[var(--circuit-steel-dark)] mb-12 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 3, duration: 0.5 }}
          >
            Show the truth gap in &lt;2 minutes. Built for VPs running deals at 2am, not executives reading dashboards.
          </motion.p>

          {/* CTAs */}
          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 3.5, duration: 0.5 }}
          >
            <Button size="lg" variant="primary">
              Try Free Tool →
            </Button>
            <Button size="lg" variant="secondary">
              Book 15-Min Demo
            </Button>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            className="mt-12 flex flex-wrap justify-center gap-8 text-sm text-[var(--circuit-steel-dark)]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 4, duration: 0.5 }}
          >
            <div>✓ No credit card required</div>
            <div>✓ 90-second setup</div>
            <div>✓ SOC 2 compliant</div>
          </motion.div>
        </div>
      </section>

      {/* PROBLEM SECTION - StoryBrand: Villain */}
      <section className="py-20 px-4 border-t border-[var(--circuit-steel-dark)]/20">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold uppercase text-[var(--circuit-steel)] mb-6">
              Your CRM Lies To You
            </h2>
            <p className="text-xl text-[var(--circuit-steel-dark)] max-w-3xl mx-auto">
              Every VP knows the feeling. It's 2am. Big deal on the line. You open your CRM and see...lies.
            </p>
          </motion.div>

          {/* Problem Grid */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {[
              {
                icon: "❌",
                title: "Forecast Drift",
                problem: "CRM says $2.3M. Reality is $1.8M. You find out Friday at 4pm.",
              },
              {
                icon: "⏰",
                title: "Stalled Deals",
                problem: "34 deals haven't moved in 30+ days. Reps say they're 'warm'. They're dead.",
              },
              {
                icon: "🎭",
                title: "Rep Theater",
                problem: "Everyone's pipeline is '80% close rate'. Math doesn't lie. They do.",
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                className="bg-[var(--circuit-black-deep)]/50 backdrop-blur-sm border border-[var(--circuit-red)]/30 rounded-lg p-6 text-center"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2, duration: 0.5 }}
              >
                <div className="text-5xl mb-4">{item.icon}</div>
                <h3 className="text-xl font-bold uppercase text-[var(--circuit-steel)] mb-2">
                  {item.title}
                </h3>
                <p className="text-[var(--circuit-steel-dark)]">{item.problem}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* THE 4 WEAPONS SECTION - StoryBrand: Plan */}
      <section className="py-20 px-4 border-t border-[var(--circuit-steel-dark)]/20">
        <div className="max-w-7xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold uppercase text-[var(--circuit-steel)] mb-6">
              The 4 Weapons
            </h2>
            <p className="text-xl text-[var(--circuit-steel-dark)] max-w-3xl mx-auto">
              Your arsenal for commanding revenue. Each weapon built for operators, not executives.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <WeaponCard
              title="Pipeline Truth Detector"
              description="Upload your pipeline CSV. See the truth in 90 seconds. No login required."
              price="FREE"
              icon="🔍"
              variant="free"
              features={[
                "CSV upload analysis",
                "Stalled deal detection",
                "90-second action plan",
                "No credit card needed",
              ]}
              cta="Try Free Now"
            />

            <WeaponCard
              title="Deal Defibrillator"
              description="AI-powered revival strategies for deals stalled 30+ days. Shock them back to life."
              price="$497/mo"
              icon="⚡"
              variant="pro"
              features={[
                "Stalled deal revival",
                "Objection handling AI",
                "Schwartz awareness scoring",
                "Multi-framework coaching",
              ]}
              cta="Get Deal Defibrillator"
            />

            <WeaponCard
              title="Forecast Reality Check"
              description="Real-time Salesforce sync showing forecast drift. Know the truth before Friday at 4pm."
              price="$497/mo"
              icon="📊"
              variant="pro"
              features={[
                "Real-time CRM sync",
                "Forecast accuracy scoring",
                "Drift alerts (Slack/email)",
                "Historical trending",
              ]}
              cta="Get Forecast Check"
            />

            <WeaponCard
              title="Quota Kill Switch"
              description="Live rep performance scoreboard. See who's hitting quota, who's faking it."
              price="$997/mo"
              icon="🎯"
              variant="premium"
              features={[
                "Rep performance dashboard",
                "Quota attainment tracking",
                "Activity vs. results scoring",
                "Manager alerts",
              ]}
              cta="Get Kill Switch"
            />
          </div>
        </div>
      </section>

      {/* SPEED METRICS SECTION - StoryBrand: Success */}
      <section className="py-20 px-4 border-t border-[var(--circuit-steel-dark)]/20">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold uppercase text-[var(--circuit-steel)] mb-6">
              Built for Speed
            </h2>
            <p className="text-xl text-[var(--circuit-steel-dark)]">
              Because operators don't have time for 8-hour BI tool training sessions.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-12">
            {[
              { metric: "<2min", label: "To Truth", description: "Upload CSV → See insights" },
              { metric: "90sec", label: "Action Plan", description: "AI-generated next steps" },
              { metric: "<1.5s", label: "Page Load", description: "No waiting. Ever." },
            ].map((item, index) => (
              <motion.div
                key={index}
                className="text-center"
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2, duration: 0.5 }}
              >
                <div className="text-6xl md:text-7xl font-bold text-[var(--circuit-red)] mb-2">
                  {item.metric}
                </div>
                <div className="text-2xl font-bold uppercase text-[var(--circuit-steel)] mb-2">
                  {item.label}
                </div>
                <div className="text-[var(--circuit-steel-dark)]">
                  {item.description}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* TESTIMONIALS SECTION - StoryBrand: Success Stories */}
      <section className="py-20 px-4 border-t border-[var(--circuit-steel-dark)]/20">
        <div className="max-w-4xl mx-auto">
          <motion.div
            className="text-center"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <blockquote className="text-2xl md:text-3xl font-medium text-[var(--circuit-steel)] mb-6 italic">
              "Finally, a tool built for 2am war rooms, not boardroom presentations."
            </blockquote>
            <div className="text-[var(--circuit-steel-dark)]">
              <p className="font-semibold">VP of Sales</p>
              <p>$50M ARR SaaS Company</p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* FINAL CTA SECTION - StoryBrand: Call to Action */}
      <section className="py-32 px-4 border-t border-[var(--circuit-steel-dark)]/20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-6xl font-bold uppercase text-[var(--circuit-steel)] mb-6">
              Command Revenue in 90 Seconds
            </h2>
            <p className="text-xl text-[var(--circuit-steel-dark)] mb-12">
              Try the Pipeline Truth Detector free. No credit card. No BS. Just truth.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="primary">
                Start Free →
              </Button>
              <Button size="lg" variant="secondary">
                Book Demo (15 min)
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-[var(--circuit-steel-dark)]/20 py-12 px-4">
        <div className="max-w-6xl mx-auto text-center text-[var(--circuit-steel-dark)]">
          <p className="mb-4">© 2025 CircuitOS. Built for operators.</p>
          <div className="flex justify-center gap-8 text-sm">
            <a href="#" className="hover:text-[var(--circuit-red)] transition-colors">Privacy</a>
            <a href="#" className="hover:text-[var(--circuit-red)] transition-colors">Terms</a>
            <a href="#" className="hover:text-[var(--circuit-red)] transition-colors">Security</a>
          </div>
        </div>
      </footer>
    </main>
  )
}
