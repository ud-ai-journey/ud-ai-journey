"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Calendar, Code, GitCommit, ExternalLink, ChevronDown, ChevronUp } from "lucide-react"
import type { JourneyDay } from "@/types/journey"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"

interface DayCardProps {
  day: JourneyDay
}

export function DayCard({ day }: DayCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const complexityColors = {
    Beginner: "bg-green-500",
    Intermediate: "bg-yellow-500",
    Advanced: "bg-red-500",
  }

  const categoryColors = {
    "AI/ML Tools": "bg-purple-500",
    "Web Applications": "bg-blue-500",
    "CLI Applications": "bg-green-500",
    "Database Projects": "bg-orange-500",
    "UI/UX Projects": "bg-pink-500",
    "Utility Tools": "bg-gray-500",
    "Data Analysis": "bg-indigo-500",
    "SaaS Applications": "bg-red-500",
  }

  return (
    <Card className="bg-white/10 backdrop-blur-sm border-white/20 hover:bg-white/20 transition-all">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl font-bold text-white">Day {day.day}</span>
              <Badge className={`${complexityColors[day.complexity]} text-white border-0`}>{day.complexity}</Badge>
              <Badge
                className={`${categoryColors[day.category as keyof typeof categoryColors] || "bg-gray-500"} text-white border-0`}
              >
                {day.category}
              </Badge>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">{day.title}</h3>
            <p className="text-gray-300 text-sm mb-3">{day.description}</p>

            {/* Tech Stack */}
            <div className="flex flex-wrap gap-2 mb-4">
              {day.technologies.map((tech) => (
                <span key={tech} className="bg-white/20 text-white px-2 py-1 rounded text-xs">
                  {tech}
                </span>
              ))}
            </div>

            {/* Quick Stats */}
            <div className="flex items-center gap-4 text-sm text-gray-300">
              <div className="flex items-center gap-1">
                <GitCommit className="w-4 h-4" />
                <span>{day.commits.length} commits</span>
              </div>
              <div className="flex items-center gap-1">
                <Code className="w-4 h-4" />
                <span>{day.filesChanged} files</span>
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <span>{new Date(day.date).toLocaleDateString()}</span>
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            {day.demoUrl && (
              <Button
                size="sm"
                variant="outline"
                className="border-white/20 text-white hover:bg-white/20 bg-transparent"
              >
                <ExternalLink className="w-4 h-4 mr-1" />
                Demo
              </Button>
            )}
            <Button
              size="sm"
              variant="outline"
              className="border-white/20 text-white hover:bg-white/20 bg-transparent"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </Button>
          </div>
        </div>
      </CardHeader>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <CardContent className="pt-0">
              <div className="border-t border-white/20 pt-4">
                {/* Highlights */}
                {day.highlights.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-white font-semibold mb-2">Key Highlights:</h4>
                    <ul className="text-gray-300 text-sm space-y-1">
                      {day.highlights.map((highlight, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <span className="text-purple-400 mt-1">•</span>
                          <span>{highlight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Commit Details */}
                <div>
                  <h4 className="text-white font-semibold mb-2">Commits:</h4>
                  <div className="space-y-2 max-h-40 overflow-y-auto">
                    {day.commits.map((commit, index) => (
                      <div key={index} className="bg-white/5 rounded p-2">
                        <div className="text-sm text-gray-300">{commit.message}</div>
                        <div className="text-xs text-gray-400 mt-1">
                          {new Date(commit.date).toLocaleTimeString()} • +{commit.additions} -{commit.deletions}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  )
}
