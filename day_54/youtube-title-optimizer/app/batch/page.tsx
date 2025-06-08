"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Upload, Download, Zap, FileText } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface BatchResult {
  original: string
  optimized: string
  seoScore: number
}

export default function BatchOptimizer() {
  const [inputTitles, setInputTitles] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [results, setResults] = useState<BatchResult[]>([])
  const { toast } = useToast()

  const processBatch = async () => {
    const titles = inputTitles.split("\n").filter((title) => title.trim())

    if (titles.length === 0) {
      toast({
        title: "No titles found",
        description: "Please enter at least one title",
        variant: "destructive",
      })
      return
    }

    if (titles.length > 10) {
      toast({
        title: "Too many titles",
        description: "Please limit to 10 titles per batch to avoid rate limits",
        variant: "destructive",
      })
      return
    }

    setIsProcessing(true)
    const batchResults: BatchResult[] = []
    let rateLimitHit = false

    try {
      for (let i = 0; i < titles.length; i++) {
        const title = titles[i]

        // Add delay between requests to avoid rate limits
        if (i > 0) {
          await new Promise((resolve) => setTimeout(resolve, 2000)) // 2 second delay
        }

        try {
          const response = await fetch("/api/optimize-title", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              originalTitle: title.trim(),
              description: "Batch optimization request",
              category: "General",
              targetEmotion: "Curiosity",
              contentType: "General",
            }),
          })

          if (response.status === 429) {
            rateLimitHit = true
            break
          }

          if (response.ok) {
            const data = await response.json()
            batchResults.push({
              original: title.trim(),
              optimized: data.improvedTitle,
              seoScore: data.seoScore || 75,
            })
          }
        } catch (error) {
          console.error(`Failed to process title: ${title}`, error)
        }
      }

      setResults(batchResults)

      if (rateLimitHit) {
        toast({
          title: "Rate limit reached",
          description: `Processed ${batchResults.length} titles before hitting limits`,
        })
      } else {
        toast({
          title: "Batch processing complete!",
          description: `Optimized ${batchResults.length} titles`,
        })
      }
    } catch (error) {
      toast({
        title: "Batch processing failed",
        description: "Some titles may not have been processed",
        variant: "destructive",
      })
    } finally {
      setIsProcessing(false)
    }
  }

  const downloadResults = () => {
    const csv = [
      "Original Title,Optimized Title,SEO Score",
      ...results.map((r) => `"${r.original}","${r.optimized}",${r.seoScore}`),
    ].join("\n")

    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "optimized-titles.csv"
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
            Batch Title Optimizer
          </h1>
          <p className="text-lg text-gray-600">
            Optimize multiple YouTube titles at once. Perfect for content creators with lots of videos.
          </p>
        </div>

        <Card className="mb-8 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5 text-purple-500" />
              Batch Input
            </CardTitle>
            <CardDescription>Enter one title per line. We'll optimize each one individually.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="My First Tutorial&#10;How to Code in Python&#10;Best Gaming Setup 2024"
              value={inputTitles}
              onChange={(e) => setInputTitles(e.target.value)}
              rows={8}
              className="text-base resize-none"
            />

            <div className="flex gap-4">
              <Button
                onClick={processBatch}
                disabled={isProcessing}
                className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                {isProcessing ? (
                  <>
                    <Zap className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <FileText className="mr-2 h-4 w-4" />
                    Optimize All Titles
                  </>
                )}
              </Button>

              {results.length > 0 && (
                <Button variant="outline" onClick={downloadResults}>
                  <Download className="mr-2 h-4 w-4" />
                  Download CSV
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {results.length > 0 && (
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle>Optimization Results</CardTitle>
              <CardDescription>{results.length} titles optimized successfully</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {results.map((result, index) => (
                  <div key={index} className="p-4 border rounded-lg bg-gray-50">
                    <div className="space-y-2">
                      <div>
                        <span className="text-sm font-medium text-gray-500">Original:</span>
                        <p className="text-gray-700">{result.original}</p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-500">Optimized:</span>
                        <p className="text-gray-900 font-medium">{result.optimized}</p>
                      </div>
                      <Badge variant="secondary" className="w-fit">
                        SEO Score: {result.seoScore}/100
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
