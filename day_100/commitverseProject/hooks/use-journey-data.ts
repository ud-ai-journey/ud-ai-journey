"use client"

import { useState, useEffect } from "react"
import type { JourneyDay, JourneyStats } from "@/types/journey"

export function useJourneyData() {
  const [journeyData, setJourneyData] = useState<JourneyDay[] | null>(null)
  const [stats, setStats] = useState<JourneyStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [usingMockData, setUsingMockData] = useState(false)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        setError(null)

        // Try to fetch from our API route
        const response = await fetch("/api/github-data")
        const data = await response.json()

        if (data.error || data.fallback) {
          // API returned an error or fallback flag, use mock data
          console.warn("Using mock data:", data.error || "Fallback mode")
          setUsingMockData(true)

          // Import and use the mock data function
          const { getEnhancedMockData } = await import("@/lib/github-parser")
          const mockData = getEnhancedMockData()
          setJourneyData(mockData.days)
          setStats(mockData.stats)
        } else {
          // Successfully got real data
          setJourneyData(data.days)
          setStats(data.stats)
          setUsingMockData(false)
        }
      } catch (err) {
        console.error("Failed to load journey data:", err)

        // Always fall back to mock data on any error
        try {
          console.log("Falling back to mock data...")
          const { getEnhancedMockData } = await import("@/lib/github-parser")
          const mockData = getEnhancedMockData()
          setJourneyData(mockData.days)
          setStats(mockData.stats)
          setUsingMockData(true)
          setError(null) // Clear error since we have fallback data
        } catch (mockError) {
          console.error("Even mock data failed:", mockError)
          setError("Unable to load any data. Please refresh the page.")
        }
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  return { journeyData, stats, loading, error, usingMockData }
}
