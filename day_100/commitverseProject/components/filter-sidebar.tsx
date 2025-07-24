"use client"

import { useState } from "react"
import { Search, Filter, X, ArrowUpDown, Calendar, Code, GitCommit, Zap } from "lucide-react"
import type { FilterState, JourneyStats } from "@/types/journey"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface FilterSidebarProps {
  filters: FilterState
  onFiltersChange: (filters: FilterState) => void
  stats: JourneyStats | null
}

export function FilterSidebar({ filters, onFiltersChange, stats }: FilterSidebarProps) {
  const [searchQuery, setSearchQuery] = useState(filters.searchQuery)

  const handleSearchChange = (value: string) => {
    setSearchQuery(value)
    onFiltersChange({ ...filters, searchQuery: value })
  }

  const handleSortChange = (sortBy: string, sortOrder: string) => {
    onFiltersChange({ ...filters, sortBy, sortOrder })
  }

  const toggleTechnology = (tech: string) => {
    const newTechs = filters.technologies.includes(tech)
      ? filters.technologies.filter((t) => t !== tech)
      : [...filters.technologies, tech]
    onFiltersChange({ ...filters, technologies: newTechs })
  }

  const toggleCategory = (category: string) => {
    const newCategories = filters.categories.includes(category)
      ? filters.categories.filter((c) => c !== category)
      : [...filters.categories, category]
    onFiltersChange({ ...filters, categories: newCategories })
  }

  const clearFilters = () => {
    setSearchQuery("")
    onFiltersChange({
      technologies: [],
      categories: [],
      searchQuery: "",
      sortBy: "day",
      sortOrder: "desc",
    })
  }

  const hasActiveFilters = filters.technologies.length > 0 || filters.categories.length > 0 || filters.searchQuery

  const sortOptions = [
    { value: "day-desc", label: "Newest First (Day 99 → 1)", icon: Calendar, sortBy: "day", sortOrder: "desc" },
    { value: "day-asc", label: "Oldest First (Day 1 → 99)", icon: Calendar, sortBy: "day", sortOrder: "asc" },
    { value: "commits-desc", label: "Most Commits First", icon: GitCommit, sortBy: "commits", sortOrder: "desc" },
    { value: "commits-asc", label: "Least Commits First", icon: GitCommit, sortBy: "commits", sortOrder: "asc" },
    { value: "complexity-desc", label: "Advanced → Beginner", icon: Zap, sortBy: "complexity", sortOrder: "desc" },
    { value: "complexity-asc", label: "Beginner → Advanced", icon: Zap, sortBy: "complexity", sortOrder: "asc" },
    { value: "lines-desc", label: "Most Code First", icon: Code, sortBy: "lines", sortOrder: "desc" },
    { value: "lines-asc", label: "Least Code First", icon: Code, sortBy: "lines", sortOrder: "asc" },
  ]

  const currentSort = `${filters.sortBy || "day"}-${filters.sortOrder || "desc"}`

  return (
    <div className="space-y-6">
      {/* Search */}
      <Card className="bg-white/10 backdrop-blur-sm border-white/20">
        <CardHeader className="pb-3">
          <CardTitle className="text-white flex items-center gap-2">
            <Search className="w-5 h-5" />
            Search Projects
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <Input
              placeholder="Search by title or description..."
              value={searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
              className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
            />
            {searchQuery && (
              <button
                onClick={() => handleSearchChange("")}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Sort Options */}
      <Card className="bg-white/10 backdrop-blur-sm border-white/20">
        <CardHeader className="pb-3">
          <CardTitle className="text-white flex items-center gap-2">
            <ArrowUpDown className="w-5 h-5" />
            Sort Projects
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {sortOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => handleSortChange(option.sortBy, option.sortOrder)}
                className={`w-full text-left px-3 py-2 rounded text-sm transition-all flex items-center gap-2 ${
                  currentSort === option.value
                    ? "bg-purple-500/30 text-purple-200 border border-purple-300/50"
                    : "text-gray-300 hover:bg-white/10"
                }`}
              >
                <option.icon className="w-4 h-4" />
                {option.label}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Active Filters */}
      {hasActiveFilters && (
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-white flex items-center gap-2">
                <Filter className="w-5 h-5" />
                Active Filters
              </CardTitle>
              <Button size="sm" variant="ghost" onClick={clearFilters} className="text-gray-400 hover:text-white">
                Clear All
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {filters.technologies.map((tech) => (
                <Badge
                  key={tech}
                  variant="secondary"
                  className="bg-purple-500/20 text-purple-200 border-purple-300/30 cursor-pointer hover:bg-purple-500/30"
                  onClick={() => toggleTechnology(tech)}
                >
                  {tech} <X className="w-3 h-3 ml-1" />
                </Badge>
              ))}
              {filters.categories.map((category) => (
                <Badge
                  key={category}
                  variant="secondary"
                  className="bg-blue-500/20 text-blue-200 border-blue-300/30 cursor-pointer hover:bg-blue-500/30"
                  onClick={() => toggleCategory(category)}
                >
                  {category} <X className="w-3 h-3 ml-1" />
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Technologies Filter */}
      {stats && (
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader className="pb-3">
            <CardTitle className="text-white">Technologies</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {stats.technologiesUsed.map((tech) => (
                <button
                  key={tech}
                  onClick={() => toggleTechnology(tech)}
                  className={`w-full text-left px-3 py-2 rounded text-sm transition-all ${
                    filters.technologies.includes(tech)
                      ? "bg-purple-500/30 text-purple-200 border border-purple-300/50"
                      : "text-gray-300 hover:bg-white/10"
                  }`}
                >
                  {tech}
                </button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Categories Filter */}
      {stats && (
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardHeader className="pb-3">
            <CardTitle className="text-white">Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {stats.categoriesExplored.map((category) => (
                <button
                  key={category}
                  onClick={() => toggleCategory(category)}
                  className={`w-full text-left px-3 py-2 rounded text-sm transition-all ${
                    filters.categories.includes(category)
                      ? "bg-blue-500/30 text-blue-200 border border-blue-300/50"
                      : "text-gray-300 hover:bg-white/10"
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
