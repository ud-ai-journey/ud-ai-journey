"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { PersonalHeader } from "@/components/personal-header"
import { HeroSection } from "@/components/hero-section"
import { TimelineView } from "@/components/timeline-view"
import { AnalyticsDashboard } from "@/components/analytics-dashboard"
import { FilterSidebar } from "@/components/filter-sidebar"
import { ExportModal } from "@/components/export-modal"
import { LoadingSpinner } from "@/components/loading-spinner"
import { useJourneyData } from "@/hooks/use-journey-data"
import type { FilterState } from "@/types/journey"

export default function CommitVerse() {
  const [activeView, setActiveView] = useState<"timeline" | "analytics">("timeline")
  const [filters, setFilters] = useState<FilterState>({
    technologies: [],
    categories: [],
    searchQuery: "",
    sortBy: "day",
    sortOrder: "desc",
  })
  const [showExportModal, setShowExportModal] = useState(false)

  const { journeyData, stats, loading, error, usingMockData } = useJourneyData()

  // Apply filters and sorting
  const filteredAndSortedDays = journeyData
    ?.filter((day) => {
      const matchesSearch =
        !filters.searchQuery ||
        day.title.toLowerCase().includes(filters.searchQuery.toLowerCase()) ||
        day.description.toLowerCase().includes(filters.searchQuery.toLowerCase())

      const matchesTech =
        filters.technologies.length === 0 || filters.technologies.some((tech) => day.technologies.includes(tech))

      const matchesCategory = filters.categories.length === 0 || filters.categories.includes(day.category)

      return matchesSearch && matchesTech && matchesCategory
    })
    ?.sort((a, b) => {
      const sortBy = filters.sortBy || "day"
      const sortOrder = filters.sortOrder || "desc"
      const multiplier = sortOrder === "asc" ? 1 : -1

      switch (sortBy) {
        case "day":
          return (a.day - b.day) * multiplier
        case "commits":
          return (a.commits.length - b.commits.length) * multiplier
        case "lines":
          return (a.linesAdded - b.linesAdded) * multiplier
        case "complexity":
          const complexityOrder = { Beginner: 1, Intermediate: 2, Advanced: 3 }
          return (complexityOrder[a.complexity] - complexityOrder[b.complexity]) * multiplier
        default:
          return (a.day - b.day) * multiplier
      }
    })

  if (loading) return <LoadingSpinner />
  if (error) return <div className="text-center text-red-500 p-8">Error loading journey data: {error}</div>

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        {/* Personal Header */}
        <PersonalHeader />

        {/* Dynamic Data Banner */}
        <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-4 mb-8 text-center">
          <p className="text-green-200">
            🔄 <strong>Live & Dynamic:</strong>{" "}
            {usingMockData
              ? "Demo mode - will show live data when deployed"
              : "Real-time data from my ud-ai-journey/ud-ai-journey repository"}
          </p>
          {stats && (
            <p className="text-green-300 text-sm mt-2">
              This app updates automatically with every new commit to my repository.
              {stats.totalDays >= 100 && " 🎉 My 100-day journey is complete!"}
            </p>
          )}
        </div>

        {/* Journey Completion Status */}
        {stats && stats.totalDays >= 100 && (
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-300/30 rounded-lg p-6 mb-8 text-center"
          >
            <h2 className="text-2xl font-bold text-white mb-2">🎉 100-Day Challenge COMPLETED! 🎉</h2>
            <p className="text-gray-300">
              My incredible dedication and consistency over {stats.totalDays} days of coding and learning!
            </p>
          </motion.div>
        )}

        {/* Data Source Info */}
        <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-4 mb-8 text-center">
          <p className="text-blue-200">
            📊 <strong>Repository:</strong> ud-ai-journey/ud-ai-journey
          </p>
          {stats && (
            <p className="text-blue-300 text-sm mt-2">
              {stats.totalDays} days of learning • {stats.totalCommits} commits • {stats.technologiesUsed.length}{" "}
              technologies mastered
            </p>
          )}
        </div>

        {/* Hero Stats */}
        {stats && <HeroSection stats={stats} />}

        {/* Navigation */}
        <div className="flex justify-center mb-8">
          <div className="bg-white/10 backdrop-blur-sm rounded-full p-1">
            <button
              onClick={() => setActiveView("timeline")}
              className={`px-6 py-2 rounded-full transition-all ${
                activeView === "timeline" ? "bg-white text-purple-900 shadow-lg" : "text-white hover:bg-white/20"
              }`}
            >
              Timeline View
            </button>
            <button
              onClick={() => setActiveView("analytics")}
              className={`px-6 py-2 rounded-full transition-all ${
                activeView === "analytics" ? "bg-white text-purple-900 shadow-lg" : "text-white hover:bg-white/20"
              }`}
            >
              Analytics
            </button>
          </div>
        </div>

        {/* Export Button */}
        <div className="fixed top-4 right-4 z-50">
          <button
            onClick={() => setShowExportModal(true)}
            className="bg-gradient-to-r from-purple-500 to-blue-500 text-white px-6 py-3 rounded-full shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            Export Portfolio
          </button>
        </div>

        {/* Results Count */}
        {filteredAndSortedDays && (
          <div className="mb-6 text-center">
            <p className="text-gray-300">
              Showing <span className="text-white font-semibold">{filteredAndSortedDays.length}</span> of{" "}
              <span className="text-white font-semibold">{journeyData?.length || 0}</span> projects
              {filters.sortBy && (
                <span className="ml-2 text-purple-300">
                  • Sorted by{" "}
                  {filters.sortBy === "day"
                    ? "Day"
                    : filters.sortBy === "commits"
                      ? "Commits"
                      : filters.sortBy === "lines"
                        ? "Lines of Code"
                        : "Complexity"}{" "}
                  ({filters.sortOrder === "asc" ? "ascending" : "descending"})
                </span>
              )}
            </p>
          </div>
        )}

        {/* Main Content */}
        <div className="flex gap-8">
          {/* Sidebar */}
          <div className="w-80 flex-shrink-0">
            <FilterSidebar filters={filters} onFiltersChange={setFilters} stats={stats} />
          </div>

          {/* Main View */}
          <div className="flex-1">
            {activeView === "timeline" ? (
              <TimelineView days={filteredAndSortedDays || []} />
            ) : (
              <AnalyticsDashboard stats={stats} days={journeyData || []} />
            )}
          </div>
        </div>

        {/* Export Modal */}
        {showExportModal && (
          <ExportModal onClose={() => setShowExportModal(false)} journeyData={journeyData || []} stats={stats} />
        )}
      </div>
    </div>
  )
}
