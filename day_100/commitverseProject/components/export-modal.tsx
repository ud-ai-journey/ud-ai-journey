"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Download, FileText, Share2, X, Copy, Check } from "lucide-react"
import type { JourneyDay, JourneyStats } from "@/types/journey"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { generatePDFPortfolio, generateMarkdownResume, generateLinkedInPost } from "@/lib/export-utils"

interface ExportModalProps {
  onClose: () => void
  journeyData: JourneyDay[]
  stats: JourneyStats | null
}

export function ExportModal({ onClose, journeyData, stats }: ExportModalProps) {
  const [isExporting, setIsExporting] = useState(false)
  const [copiedLinkedIn, setCopiedLinkedIn] = useState(false)

  const handlePDFExport = async () => {
    if (!stats) return
    setIsExporting(true)
    try {
      await generatePDFPortfolio(journeyData, stats)
    } catch (error) {
      console.error("PDF export failed:", error)
    }
    setIsExporting(false)
  }

  const handleMarkdownExport = () => {
    if (!stats) return
    const markdown = generateMarkdownResume(journeyData, stats)
    const blob = new Blob([markdown], { type: "text/markdown" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "journey-portfolio.md"
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleLinkedInCopy = async () => {
    if (!stats) return
    const linkedInPost = generateLinkedInPost(journeyData, stats)
    await navigator.clipboard.writeText(linkedInPost)
    setCopiedLinkedIn(true)
    setTimeout(() => setCopiedLinkedIn(false), 2000)
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-gradient-to-br from-purple-900/90 to-blue-900/90 backdrop-blur-sm border border-white/20 rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Export Portfolio</h2>
          <Button variant="ghost" size="sm" onClick={onClose} className="text-white hover:bg-white/20">
            <X className="w-5 h-5" />
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* PDF Portfolio */}
          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <FileText className="w-5 h-5" />
                PDF Portfolio
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-300 text-sm mb-4">
                Generate a professional PDF portfolio with project summaries, statistics, and timeline.
              </p>
              <Button
                onClick={handlePDFExport}
                disabled={isExporting}
                className="w-full bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600"
              >
                <Download className="w-4 h-4 mr-2" />
                {isExporting ? "Generating..." : "Download PDF"}
              </Button>
            </CardContent>
          </Card>

          {/* Markdown Resume */}
          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Markdown Resume
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-300 text-sm mb-4">
                Export a structured markdown file perfect for GitHub README or technical documentation.
              </p>
              <Button
                onClick={handleMarkdownExport}
                className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
              >
                <Download className="w-4 h-4 mr-2" />
                Download Markdown
              </Button>
            </CardContent>
          </Card>

          {/* LinkedIn Post */}
          <Card className="bg-white/10 backdrop-blur-sm border-white/20 md:col-span-2">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Share2 className="w-5 h-5" />
                LinkedIn Post Template
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-300 text-sm mb-4">
                Copy a ready-to-post LinkedIn update showcasing your 100-day journey with impressive metrics.
              </p>
              <div className="bg-black/30 rounded-lg p-4 mb-4 text-sm text-gray-300 max-h-40 overflow-y-auto">
                {stats && generateLinkedInPost(journeyData, stats)}
              </div>
              <Button
                onClick={handleLinkedInCopy}
                className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600"
              >
                {copiedLinkedIn ? (
                  <>
                    <Check className="w-4 h-4 mr-2" />
                    Copied to Clipboard!
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4 mr-2" />
                    Copy LinkedIn Post
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Journey Stats Preview */}
        {stats && (
          <Card className="bg-white/10 backdrop-blur-sm border-white/20 mt-6">
            <CardHeader>
              <CardTitle className="text-white">Journey Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-white">{stats.totalDays}</div>
                  <div className="text-gray-300 text-sm">Days</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.totalProjects}</div>
                  <div className="text-gray-300 text-sm">Projects</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.totalCommits}</div>
                  <div className="text-gray-300 text-sm">Commits</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.technologiesUsed.length}</div>
                  <div className="text-gray-300 text-sm">Technologies</div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </motion.div>
    </motion.div>
  )
}
