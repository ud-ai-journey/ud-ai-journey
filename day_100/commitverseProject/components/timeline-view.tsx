"use client"

import { motion } from "framer-motion"
import type { JourneyDay } from "@/types/journey"
import { DayCard } from "./day-card"

interface TimelineViewProps {
  days: JourneyDay[]
}

export function TimelineView({ days }: TimelineViewProps) {
  return (
    <div className="relative">
      {/* Timeline Line */}
      <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-400 via-blue-400 to-indigo-400"></div>

      {/* Timeline Items */}
      <div className="space-y-8">
        {days.map((day, index) => (
          <motion.div
            key={day.day}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className="relative pl-20"
          >
            {/* Timeline Dot */}
            <div className="absolute left-6 w-4 h-4 bg-gradient-to-r from-purple-400 to-blue-400 rounded-full border-4 border-white shadow-lg"></div>

            {/* Day Card */}
            <DayCard day={day} />
          </motion.div>
        ))}
      </div>
    </div>
  )
}
