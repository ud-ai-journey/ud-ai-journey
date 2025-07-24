"use client"

import { motion } from "framer-motion"
import { Calendar, Code, GitCommit, Zap } from "lucide-react"
import type { JourneyStats } from "@/types/journey"
import { CountUpAnimation } from "./count-up-animation"

interface HeroSectionProps {
  stats: JourneyStats
}

export function HeroSection({ stats }: HeroSectionProps) {
  const statCards = [
    {
      icon: Calendar,
      label: "Days of Learning",
      value: stats.totalDays,
      color: "from-purple-500 to-pink-500",
    },
    {
      icon: Code,
      label: "Projects Built", // Back to original since you built projects from day 2
      value: stats.totalProjects,
      color: "from-blue-500 to-cyan-500",
    },
    {
      icon: GitCommit,
      label: "Total Commits",
      value: stats.totalCommits,
      color: "from-green-500 to-emerald-500",
    },
    {
      icon: Zap,
      label: "Technologies",
      value: stats.technologiesUsed.length,
      color: "from-orange-500 to-red-500",
    },
  ]

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="mb-16"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all"
          >
            <div
              className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.color} flex items-center justify-center mb-4`}
            >
              <stat.icon className="w-6 h-6 text-white" />
            </div>
            <div className="text-3xl font-bold text-white mb-2">
              <CountUpAnimation end={stat.value} duration={2000} />
            </div>
            <div className="text-gray-300 text-sm">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Updated Clarification Banner */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="mt-8 bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-center"
      >
        <p className="text-green-200 text-sm">
          🎯 <strong>Accurate Count:</strong> Projects built from Day 2 onwards (excluding pure documentation updates).
          <br />
          Each project represents real development work and learning milestones in your journey.
        </p>
      </motion.div>

      {/* Journey Highlights */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.0 }}
        className="mt-12 text-center"
      >
        <h2 className="text-2xl font-bold text-white mb-6">Journey Highlights</h2>
        <div className="flex flex-wrap justify-center gap-3">
          {stats.technologiesUsed.slice(0, 12).map((tech, index) => (
            <motion.span
              key={tech}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.1 + index * 0.05 }}
              className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 backdrop-blur-sm border border-purple-300/30 px-4 py-2 rounded-full text-white text-sm"
            >
              {tech}
            </motion.span>
          ))}
        </div>
      </motion.div>
    </motion.section>
  )
}
