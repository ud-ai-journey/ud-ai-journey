"use client"

import { motion } from "framer-motion"
import { ExternalLink, Github } from "lucide-react"
import Image from "next/image"

export function PersonalHeader() {
  return (
    <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
      {/* Profile Section */}
      <div className="flex flex-col items-center mb-8">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="relative mb-6"
        >
          <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-white/20 shadow-2xl">
            <Image
              src="/images/uday-profile.jpg"
              alt="Uday Kumar"
              width={128}
              height={128}
              className="w-full h-full object-cover"
            />
          </div>
          <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-green-500 rounded-full border-4 border-white/20 flex items-center justify-center">
            <span className="text-white text-xs font-bold">✓</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-center"
        >
          <h2 className="text-2xl font-bold text-white mb-2">Uday Kumar</h2>
          <p className="text-gray-300 mb-4">Python + AI Developer | 100-Day Journey Completed</p>

          {/* Links */}
          <div className="flex justify-center gap-4">
            <a
              href="https://ud-ai-kumar.vercel.app/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 px-4 py-2 rounded-full text-white transition-all"
            >
              <ExternalLink className="w-4 h-4" />
              Portfolio
            </a>
            <a
              href="https://github.com/ud-ai-journey"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 px-4 py-2 rounded-full text-white transition-all"
            >
              <Github className="w-4 h-4" />
              GitHub
            </a>
          </div>
        </motion.div>
      </div>

      {/* Main Title */}
      <h1 className="text-6xl font-bold text-white mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
        CommitVerse
      </h1>
      <p className="text-xl text-gray-300 max-w-2xl mx-auto">
        My visual journey through 100 days of Python + AI mastery
      </p>
    </motion.div>
  )
}
