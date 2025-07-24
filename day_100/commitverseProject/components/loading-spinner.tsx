"use client"

import { motion } from "framer-motion"

export function LoadingSpinner() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
      <div className="text-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Number.POSITIVE_INFINITY, ease: "linear" }}
          className="w-16 h-16 border-4 border-white/20 border-t-white rounded-full mx-auto mb-4"
        />
        <motion.h2 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-2xl font-bold text-white mb-2">
          Loading CommitVerse
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-gray-300"
        >
          Analyzing your 100-day journey...
        </motion.p>
      </div>
    </div>
  )
}
