"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Copy, Sparkles, Target, TrendingUp, Zap, Youtube, Lightbulb, BarChart3 } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface OptimizationResult {
  improvedTitle: string
  alternates: string[]
  reason: string
  seoScore: number
  emotionalHooks: string[]
}

export default function YouTubeTitleOptimizer() {
  const [originalTitle, setOriginalTitle] = useState("")
  const [description, setDescription] = useState("")
  const [category, setCategory] = useState("")
  const [targetEmotion, setTargetEmotion] = useState("")
  const [contentType, setContentType] = useState("")
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [result, setResult] = useState<OptimizationResult | null>(null)
  const { toast } = useToast()
  const [rateLimitHit, setRateLimitHit] = useState(false)

  const categories = [
    "Tech & Programming",
    "Lifestyle & Vlog",
    "Gaming",
    "Education & Tutorial",
    "Entertainment",
    "Business & Finance",
    "Health & Fitness",
    "Travel",
    "Food & Cooking",
  ]

  const emotions = ["Curiosity", "Urgency", "Excitement", "Surprise", "FOMO", "Achievement", "Transformation"]

  const contentTypes = ["Tutorial", "Review", "Vlog", "Reaction", "Challenge", "Tips & Tricks", "Behind the Scenes"]

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      toast({
        title: "Copied!",
        description: "Title copied to clipboard",
      })
    } catch (err) {
      toast({
        title: "Failed to copy",
        description: "Please copy manually",
        variant: "destructive",
      })
    }
  }

  const optimizeTitle = async () => {
    if (!originalTitle.trim() || !description.trim()) {
      toast({
        title: "Missing Information",
        description: "Please provide both title and description",
        variant: "destructive",
      })
      return
    }

    setIsOptimizing(true)

    try {
      const response = await fetch("/api/optimize-title", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          originalTitle,
          description,
          category,
          targetEmotion,
          contentType,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        if (response.status === 429) {
          setRateLimitHit(true)
          toast({
            title: "Rate Limit Reached",
            description: data.error || "Please wait a minute before trying again",
            variant: "destructive",
          })
          return
        }

        if (data.fallback) {
          // Show fallback suggestions
          setResult(generateFallbackSuggestions(originalTitle, category, targetEmotion))
          toast({
            title: "Using Offline Mode",
            description: "AI temporarily unavailable - showing rule-based suggestions",
          })
          return
        }

        throw new Error(data.error || "Optimization failed")
      }

      setResult(data)
      toast({
        title: "Title Optimized!",
        description: "Your title has been enhanced with AI",
      })
    } catch (error: any) {
      console.error("Optimization error:", error)

      // Show fallback suggestions
      setResult(generateFallbackSuggestions(originalTitle, category, targetEmotion))
      toast({
        title: "Using Offline Mode",
        description: "Showing rule-based suggestions while AI recovers",
      })
    } finally {
      setIsOptimizing(false)
    }
  }

  // Add this fallback function before the return statement
  const generateFallbackSuggestions = (title: string, category: string, emotion: string): OptimizationResult => {
    const powerWords = ["Ultimate", "Secret", "Proven", "Amazing", "Shocking", "Incredible"]
    const emotionWords = {
      Curiosity: ["Why", "How", "Secret", "Hidden", "Unknown"],
      Urgency: ["Now", "Today", "Fast", "Quick", "Instant"],
      Excitement: ["Amazing", "Incredible", "Epic", "Awesome", "Mind-Blowing"],
      Surprise: ["Shocking", "Unexpected", "Surprising", "Unbelievable"],
      FOMO: ["Don't Miss", "Limited", "Exclusive", "Only", "Before It's Gone"],
      Achievement: ["Master", "Pro", "Expert", "Success", "Win"],
      Transformation: ["Transform", "Change", "Upgrade", "Improve", "Revolution"],
    }

    const categoryPrefixes = {
      "Tech & Programming": "🔥 ",
      Gaming: "🎮 ",
      "Lifestyle & Vlog": "✨ ",
      "Education & Tutorial": "📚 ",
      Entertainment: "🎬 ",
    }

    const prefix = categoryPrefixes[category as keyof typeof categoryPrefixes] || ""
    const emotionWordList = emotionWords[emotion as keyof typeof emotionWords] || ["Amazing"]
    const powerWord = powerWords[Math.floor(Math.random() * powerWords.length)]
    const emotionWord = emotionWordList[Math.floor(Math.random() * emotionWordList.length)]

    return {
      improvedTitle: `${prefix}${emotionWord} ${title} (${powerWord} Results!)`,
      alternates: [
        `${powerWord} ${title} - You Won't Believe This!`,
        `${emotionWord} ${title} | ${category} Guide`,
        `${title} - ${powerWord} Tips Inside! 🚀`,
      ],
      reason: `Added emotional triggers (${emotionWord}), power words (${powerWord}), and category-specific elements to increase click-through rates. This fallback uses proven YouTube optimization techniques.`,
      seoScore: 75,
      emotionalHooks: [emotionWord, powerWord, "Results"],
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-orange-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Youtube className="h-8 w-8 text-red-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent">
              YouTube Title Optimizer
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Transform your video titles with AI-powered optimization. Get clickable, SEO-friendly titles that beat the
            algorithm.
          </p>
        </div>

        {rateLimitHit && (
          <Card className="mb-6 border-yellow-200 bg-yellow-50">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-yellow-800">
                <Zap className="h-5 w-5" />
                <p className="font-medium">Rate limit reached - using offline mode for now</p>
              </div>
              <p className="text-sm text-yellow-700 mt-1">
                AI optimization will be available again in a few minutes. Meanwhile, enjoy our rule-based suggestions!
              </p>
            </CardContent>
          </Card>
        )}

        {/* Input Form */}
        <Card className="mb-8 shadow-lg border-0 bg-white/80 backdrop-blur">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-yellow-500" />
              Title Optimization Studio
            </CardTitle>
            <CardDescription>Enter your video details and let AI craft the perfect title</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium">Current Video Title</label>
              <Input
                placeholder="e.g., My First Coding Tutorial"
                value={originalTitle}
                onChange={(e) => setOriginalTitle(e.target.value)}
                className="text-base"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Video Description</label>
              <Textarea
                placeholder="Describe what your video is about..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="text-base resize-none"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Category</label>
                <Select value={category} onValueChange={setCategory}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Target Emotion</label>
                <Select value={targetEmotion} onValueChange={setTargetEmotion}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose emotion" />
                  </SelectTrigger>
                  <SelectContent>
                    {emotions.map((emotion) => (
                      <SelectItem key={emotion} value={emotion}>
                        {emotion}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Content Type</label>
                <Select value={contentType} onValueChange={setContentType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {contentTypes.map((type) => (
                      <SelectItem key={type} value={type}>
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <Button
              onClick={optimizeTitle}
              disabled={isOptimizing}
              className="w-full bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-semibold py-3 text-lg"
            >
              {isOptimizing ? (
                <>
                  <Zap className="mr-2 h-4 w-4 animate-spin" />
                  Optimizing with AI...
                </>
              ) : (
                <>
                  <Target className="mr-2 h-4 w-4" />
                  Optimize Title
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Main Optimized Title */}
            <Card className="shadow-lg border-0 bg-gradient-to-r from-green-50 to-emerald-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-green-800">
                  <TrendingUp className="h-5 w-5" />
                  Optimized Title
                  <Badge variant="secondary" className="ml-auto">
                    SEO Score: {result.seoScore}/100
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between p-4 bg-white rounded-lg border-2 border-green-200">
                  <p className="text-lg font-semibold text-gray-800 flex-1">{result.improvedTitle}</p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(result.improvedTitle)}
                    className="ml-4"
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                </div>

                {result.emotionalHooks.length > 0 && (
                  <div className="mt-4">
                    <p className="text-sm font-medium text-gray-700 mb-2">Emotional Hooks:</p>
                    <div className="flex flex-wrap gap-2">
                      {result.emotionalHooks.map((hook, index) => (
                        <Badge key={index} variant="secondary" className="bg-green-100 text-green-800">
                          {hook}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Alternative Suggestions */}
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lightbulb className="h-5 w-5 text-yellow-500" />
                  Alternative Suggestions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {result.alternates.map((alt, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-800 flex-1">{alt}</span>
                    <Button variant="ghost" size="sm" onClick={() => copyToClipboard(alt)}>
                      <Copy className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* AI Reasoning */}
            <Card className="shadow-lg border-0 bg-blue-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-blue-800">
                  <BarChart3 className="h-5 w-5" />
                  Why This Title Works
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">{result.reason}</p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Footer */}
        <Separator className="my-8" />
        <div className="text-center text-gray-600">
          <p className="font-medium">Built by Uday Kumar</p>
          <p className="text-sm">Part of 100 Days of Python + AI Challenge | Powered by Gemini AI</p>
        </div>
      </div>
    </div>
  )
}
