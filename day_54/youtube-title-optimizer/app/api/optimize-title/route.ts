import { GoogleGenerativeAI } from "@google/generative-ai"
import { type NextRequest, NextResponse } from "next/server"

const genAI = new GoogleGenerativeAI("AIzaSyD3jowK2a6akj4YhXLeb_Q18hJS3pz7OAA")

// Rate limiting - simple in-memory store (use Redis in production)
const rateLimitMap = new Map<string, { count: number; resetTime: number }>()

function checkRateLimit(ip: string): boolean {
  const now = Date.now()
  const windowMs = 60 * 1000 // 1 minute window
  const maxRequests = 5 // Max 5 requests per minute

  const current = rateLimitMap.get(ip)

  if (!current || now > current.resetTime) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + windowMs })
    return true
  }

  if (current.count >= maxRequests) {
    return false
  }

  current.count++
  return true
}

async function optimizeWithRetry(prompt: string, retries = 2): Promise<any> {
  for (let i = 0; i <= retries; i++) {
    try {
      // Use gemini-1.5-flash instead of pro - much higher rate limits
      const model = genAI.getGenerativeModel({
        model: "gemini-1.5-flash",
        generationConfig: {
          maxOutputTokens: 500,
          temperature: 0.7,
        },
      })

      const result = await model.generateContent(prompt)
      return result.response.text()
    } catch (error: any) {
      console.log(`Attempt ${i + 1} failed:`, error.message)

      if (i === retries) throw error

      // Wait before retry (exponential backoff)
      await new Promise((resolve) => setTimeout(resolve, Math.pow(2, i) * 1000))
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    // Get client IP for rate limiting
    const ip = request.ip || request.headers.get("x-forwarded-for") || "unknown"

    // Check rate limit
    if (!checkRateLimit(ip)) {
      return NextResponse.json(
        { error: "Rate limit exceeded. Please wait a minute before trying again." },
        { status: 429 },
      )
    }

    const { originalTitle, description, category, targetEmotion, contentType } = await request.json()

    // Shorter, more efficient prompt to reduce token usage
    const prompt = `Transform this YouTube title for maximum clicks and SEO:

TITLE: "${originalTitle}"
DESC: "${description}"
CATEGORY: ${category || "General"}
EMOTION: ${targetEmotion || "Curiosity"}

Create 1 optimized title + 3 alternatives. Keep under 60 chars each.

Respond ONLY in this JSON format:
{
  "improvedTitle": "Main optimized title",
  "alternates": ["Alt 1", "Alt 2", "Alt 3"],
  "reason": "Brief explanation why it works",
  "seoScore": 85,
  "emotionalHooks": ["Hook1", "Hook2"]
}`

    const text = await optimizeWithRetry(prompt)

    // Parse JSON response
    const jsonMatch = text.match(/\{[\s\S]*\}/)
    if (!jsonMatch) {
      throw new Error("Invalid AI response format")
    }

    const parsedResult = JSON.parse(jsonMatch[0])

    // Validate required fields
    if (!parsedResult.improvedTitle || !parsedResult.alternates) {
      throw new Error("Incomplete AI response")
    }

    return NextResponse.json(parsedResult)
  } catch (error: any) {
    console.error("Title optimization error:", error)

    // Handle specific quota errors
    if (error.message?.includes("quota") || error.message?.includes("429")) {
      return NextResponse.json(
        {
          error: "AI service temporarily unavailable due to high demand. Please try again in a few minutes.",
          retryAfter: 60,
        },
        { status: 429 },
      )
    }

    // Fallback response for other errors
    return NextResponse.json(
      {
        error: "Optimization temporarily unavailable. Please try again.",
        fallback: true,
      },
      { status: 500 },
    )
  }
}
