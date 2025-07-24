"use client"

import { motion } from "framer-motion"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { JourneyDay, JourneyStats } from "@/types/journey"

interface AnalyticsDashboardProps {
  stats: JourneyStats | null
  days: JourneyDay[]
}

export function AnalyticsDashboard({ stats, days }: AnalyticsDashboardProps) {
  // Use real stats if available, otherwise use realistic fallback based on your actual journey
  const actualStats = stats || {
    totalDays: 99,
    totalProjects: 99, // Each day was a project/learning milestone
    totalCommits: 150, // More realistic commit count
    technologiesUsed: [
      "Python",
      "Streamlit",
      "OpenAI",
      "FastAPI",
      "MongoDB",
      "Next.js",
      "React",
      "AI/ML",
      "Voice/TTS",
      "Supabase",
      "HuggingFace",
      "Transformers",
    ],
  }

  // Use real data if available, otherwise realistic fallback
  const weeklyProgress =
    days && days.length > 0
      ? days.reduce(
          (acc, day) => {
            const week = Math.ceil(day.day / 7)
            const existing = acc.find((w) => w.week === week)
            if (existing) {
              existing.projects += 1
              existing.commits += day.commits.length
            } else {
              acc.push({
                week,
                projects: 1,
                commits: day.commits.length,
              })
            }
            return acc
          },
          [] as Array<{ week: number; projects: number; commits: number }>,
        )
      : [
          { week: 1, projects: 7, commits: 12 },
          { week: 2, projects: 7, commits: 11 },
          { week: 3, projects: 7, commits: 10 },
          { week: 4, projects: 7, commits: 13 },
          { week: 5, projects: 7, commits: 9 },
          { week: 6, projects: 7, commits: 12 },
          { week: 7, projects: 7, commits: 11 },
          { week: 8, projects: 7, commits: 10 },
          { week: 9, projects: 7, commits: 14 },
          { week: 10, projects: 7, commits: 8 },
          { week: 11, projects: 7, commits: 12 },
          { week: 12, projects: 7, commits: 9 },
          { week: 13, projects: 7, commits: 11 },
          { week: 14, projects: 1, commits: 8 },
        ]

  const technologyUsage =
    actualStats.technologiesUsed.length > 0
      ? actualStats.technologiesUsed.slice(0, 10).map((tech) => ({
          name: tech,
          count:
            days.length > 0
              ? days.filter((day) => day.technologies.includes(tech)).length
              : Math.floor(Math.random() * 50) + 10, // Realistic random for demo
        }))
      : [
          { name: "Python", count: 99 },
          { name: "Streamlit", count: 45 },
          { name: "OpenAI", count: 35 },
          { name: "FastAPI", count: 25 },
          { name: "MongoDB", count: 20 },
          { name: "Next.js", count: 15 },
          { name: "React", count: 12 },
          { name: "AI/ML", count: 40 },
          { name: "Voice/TTS", count: 18 },
          { name: "Supabase", count: 10 },
        ]

  const complexityData =
    days && days.length > 0
      ? [
          { name: "Beginner", value: days.filter((d) => d.complexity === "Beginner").length, color: "#10B981" },
          { name: "Intermediate", value: days.filter((d) => d.complexity === "Intermediate").length, color: "#F59E0B" },
          { name: "Advanced", value: days.filter((d) => d.complexity === "Advanced").length, color: "#EF4444" },
        ]
      : [
          { name: "Beginner", value: 35, color: "#10B981" },
          { name: "Intermediate", value: 45, color: "#F59E0B" },
          { name: "Advanced", value: 19, color: "#EF4444" },
        ]

  const categoryData =
    stats && stats.categoriesExplored.length > 0
      ? stats.categoriesExplored.map((category) => ({
          name: category,
          value: days.filter((d) => d.category === category).length,
        }))
      : [
          { name: "AI/ML Tools", value: 25 },
          { name: "Web Applications", value: 30 },
          { name: "CLI Applications", value: 15 },
          { name: "Database Projects", value: 12 },
          { name: "SaaS Applications", value: 8 },
          { name: "Data Analysis", value: 6 },
          { name: "Utility Tools", value: 3 },
        ]

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        {/* Weekly Progress */}
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader>
            <CardTitle className="text-white">Weekly Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center">
              <div className="w-full">
                <div className="space-y-4">
                  <div className="flex justify-between text-sm text-gray-300">
                    <span>Week</span>
                    <span>Projects</span>
                    <span>Commits</span>
                  </div>
                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {weeklyProgress.map((week) => (
                      <div key={week.week} className="flex justify-between items-center p-2 bg-white/5 rounded">
                        <span className="text-white font-medium">Week {week.week}</span>
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-2">
                            <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                            <span className="text-purple-300">{week.projects}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                            <span className="text-blue-300">{week.commits}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Technology Usage */}
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader>
            <CardTitle className="text-white">Top Technologies</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] overflow-y-auto">
              <div className="space-y-3">
                {technologyUsage.map((tech, index) => (
                  <div key={tech.name} className="flex items-center justify-between">
                    <span className="text-white font-medium">{tech.name}</span>
                    <div className="flex items-center gap-3 flex-1 ml-4">
                      <div className="flex-1 bg-white/10 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all duration-1000"
                          style={{ width: `${(tech.count / Math.max(...technologyUsage.map((t) => t.count))) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-gray-300 text-sm w-8">{tech.count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Project Complexity */}
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader>
            <CardTitle className="text-white">Project Complexity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center">
              <div className="w-full space-y-4">
                {complexityData.map((item) => {
                  const total = complexityData.reduce((sum, d) => sum + d.value, 0)
                  return (
                    <div key={item.name} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-4 h-4 rounded-full" style={{ backgroundColor: item.color }}></div>
                        <span className="text-white font-medium">{item.name}</span>
                      </div>
                      <div className="flex items-center gap-3 flex-1 ml-4">
                        <div className="flex-1 bg-white/10 rounded-full h-3">
                          <div
                            className="h-3 rounded-full transition-all duration-1000"
                            style={{
                              backgroundColor: item.color,
                              width: `${(item.value / total) * 100}%`,
                            }}
                          ></div>
                        </div>
                        <span className="text-gray-300 text-sm w-12">
                          {item.value} ({Math.round((item.value / total) * 100)}%)
                        </span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Project Categories */}
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader>
            <CardTitle className="text-white">Project Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] overflow-y-auto">
              <div className="space-y-3">
                {categoryData.map((category, index) => {
                  const colors = ["#8B5CF6", "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#EC4899", "#6B7280"]
                  const color = colors[index % colors.length]
                  const maxValue = Math.max(...categoryData.map((c) => c.value))
                  return (
                    <div key={category.name} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-4 h-4 rounded-full" style={{ backgroundColor: color }}></div>
                        <span className="text-white font-medium text-sm">{category.name}</span>
                      </div>
                      <div className="flex items-center gap-3 flex-1 ml-4">
                        <div className="flex-1 bg-white/10 rounded-full h-2">
                          <div
                            className="h-2 rounded-full transition-all duration-1000"
                            style={{
                              backgroundColor: color,
                              width: `${(category.value / maxValue) * 100}%`,
                            }}
                          ></div>
                        </div>
                        <span className="text-gray-300 text-sm w-8">{category.value}</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Skill Progression Timeline */}
      <Card className="bg-white/10 backdrop-blur-sm border-white/20">
        <CardHeader>
          <CardTitle className="text-white">Learning Journey Milestones</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { day: 1, milestone: "First Python Script", description: "Hello World - The beginning of the journey" },
              { day: 10, milestone: "Student Report System", description: "Built first data management system" },
              {
                day: 25,
                milestone: "AI Integration",
                description: "Started working with AI APIs and voice processing",
              },
              {
                day: 50,
                milestone: "Advanced Projects",
                description: "Complex applications with multiple integrations",
              },
              { day: 75, milestone: "SaaS Development", description: "Full-stack applications with databases" },
              { day: 99, milestone: "Enterprise Solutions", description: "Multi-user systems with admin controls" },
            ].map((milestone, index) => (
              <motion.div
                key={milestone.day}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-4 p-4 bg-white/5 rounded-lg"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                  {milestone.day}
                </div>
                <div>
                  <h3 className="text-white font-semibold">{milestone.milestone}</h3>
                  <p className="text-gray-300 text-sm">{milestone.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Accurate Journey Summary */}
      <Card className="bg-white/10 backdrop-blur-sm border-white/20">
        <CardHeader>
          <CardTitle className="text-white">Journey Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">{actualStats.totalDays}</div>
              <div className="text-gray-300 text-sm">Days Completed</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-400 mb-2">{actualStats.totalProjects}</div>
              <div className="text-gray-300 text-sm">Learning Milestones</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400 mb-2">{actualStats.totalCommits}</div>
              <div className="text-gray-300 text-sm">Total Commits</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-400 mb-2">{actualStats.technologiesUsed.length}</div>
              <div className="text-gray-300 text-sm">Technologies</div>
            </div>
          </div>

          {/* Data Source Note */}
          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              {stats
                ? "📊 Live data from your GitHub repository"
                : "📊 Demo data - will show live stats when connected to GitHub"}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
