import { NextResponse } from "next/server"

const GITHUB_REPO = "ud-ai-journey/ud-ai-journey"
const GITHUB_API_BASE = "https://api.github.com"

interface GitHubCommit {
  sha: string
  commit: {
    message: string
    author: {
      date: string
    }
  }
  stats?: {
    additions: number
    deletions: number
  }
}

function generateStats(days: any[]) {
  const technologies = new Set()
  const categories = new Set()
  let totalCommits = 0

  days.forEach((day) => {
    day.technologies.forEach((tech: string) => technologies.add(tech))
    categories.add(day.category)
    totalCommits += day.commits.length
  })

  // More accurate project counting - count actual projects from day 2 onwards
  const actualProjects = days.filter((day) => {
    // Day 1 might be setup/intro, but from day 2 onwards you built projects
    if (day.day === 1) {
      // Only count day 1 if it has substantial project indicators
      return day.commits.some((commit) => {
        const msg = commit.message.toLowerCase()
        return (
          msg.includes("built") ||
          msg.includes("created") ||
          msg.includes("project") ||
          msg.includes("app") ||
          msg.includes("system")
        )
      })
    }

    // From day 2 onwards, count as projects unless they're clearly just documentation
    const isJustDocumentation = day.commits.every((commit) => {
      const msg = commit.message.toLowerCase()
      return (
        msg.includes("readme") ||
        msg.includes("update readme") ||
        msg.includes("added readme") ||
        msg.includes("documentation") ||
        msg.includes("docs") ||
        (msg.includes("update") && msg.length < 30) // Very short update messages
      )
    })

    // If it's just documentation, don't count it
    if (isJustDocumentation) {
      return false
    }

    // Everything else from day 2+ is a project
    return day.day >= 2
  }).length

  return {
    totalDays: days.length,
    totalProjects: actualProjects, // Much more accurate count
    totalCommits,
    totalLinesOfCode: days.reduce((sum, day) => sum + day.linesAdded, 0),
    technologiesUsed: Array.from(technologies),
    categoriesExplored: Array.from(categories),
    skillProgression: [
      { week: 1, level: "Beginner", projects: 7 },
      { week: 5, level: "Intermediate", projects: 28 },
      { week: 10, level: "Advanced", projects: 70 },
      { week: 14, level: "Expert", projects: actualProjects },
    ],
  }
}

export async function GET() {
  try {
    const headers: Record<string, string> = {
      Accept: "application/vnd.github.v3+json",
      "User-Agent": "CommitVerse-UdayKumar",
    }

    if (process.env.GITHUB_TOKEN) {
      headers["Authorization"] = `token ${process.env.GITHUB_TOKEN}`
    }

    // First, check if the repository exists
    const repoResponse = await fetch(`${GITHUB_API_BASE}/repos/${GITHUB_REPO}`, { headers })

    if (!repoResponse.ok) {
      console.warn(`Repository ${GITHUB_REPO} not accessible: ${repoResponse.status}`)
      return NextResponse.json(
        {
          error: `Repository not found or not accessible. Status: ${repoResponse.status}`,
          fallback: true,
        },
        { status: 200 },
      )
    }

    // Fetch ALL commits by paginating through multiple pages
    let allCommits: GitHubCommit[] = []
    let page = 1
    let hasMoreCommits = true

    while (hasMoreCommits && page <= 15) {
      console.log(`Fetching commits page ${page}...`)

      const commitsResponse = await fetch(`${GITHUB_API_BASE}/repos/${GITHUB_REPO}/commits?per_page=100&page=${page}`, {
        headers,
      })

      if (!commitsResponse.ok) {
        console.warn(`Commits page ${page} not accessible: ${commitsResponse.status}`)
        break
      }

      const commits: GitHubCommit[] = await commitsResponse.json()

      if (commits.length === 0) {
        hasMoreCommits = false
      } else {
        allCommits = [...allCommits, ...commits]
        page++
      }
    }

    console.log(`Fetched total of ${allCommits.length} commits from ${GITHUB_REPO}`)

    const days = await processDayData(allCommits)
    const stats = generateStats(days)

    console.log(
      `Processed ${days.length} days with ${stats.totalCommits} commits and ${stats.totalProjects} actual projects`,
    )

    return NextResponse.json({
      days,
      stats,
      metadata: {
        totalCommitsFetched: allCommits.length,
        daysProcessed: days.length,
        actualProjects: stats.totalProjects,
        projectsFromDay2: days.filter((d) => d.day >= 2 && !isJustDocumentation(d)).length,
        note: "Counting all days from day 2 onwards as projects (excluding pure documentation)",
      },
    })
  } catch (error) {
    console.error("GitHub API Error:", error)
    return NextResponse.json(
      {
        error: `GitHub API error: ${error.message}`,
        fallback: true,
      },
      { status: 200 },
    )
  }
}

function isJustDocumentation(day: any): boolean {
  return day.commits.every((commit) => {
    const msg = commit.message.toLowerCase()
    return (
      msg.includes("readme") ||
      msg.includes("update readme") ||
      msg.includes("added readme") ||
      msg.includes("documentation") ||
      msg.includes("docs") ||
      (msg.includes("update") && msg.length < 30)
    )
  })
}

async function processDayData(commits: GitHubCommit[]) {
  const dayMap = new Map()

  for (const commit of commits) {
    // Look for day patterns in commit messages - including day_100!
    const dayPatterns = [
      /day[_\s-]?(\d+)/i,
      /(\d+)[_\s-]?day/i,
      /project[_\s-]?(\d+)/i,
      /(\d+)[_\s-]?project/i,
      /Day\s+(\d+)/i,
      /🎯.*?Day\s+(\d+)/i,
      /Completed.*?Day\s+(\d+)/i,
    ]

    let dayNum = null
    for (const pattern of dayPatterns) {
      const match = commit.commit.message.match(pattern)
      if (match) {
        dayNum = Number.parseInt(match[1])
        break
      }
    }

    if (dayNum && dayNum >= 1 && dayNum <= 100) {
      if (!dayMap.has(dayNum)) {
        dayMap.set(dayNum, {
          day: dayNum,
          date: commit.commit.author.date,
          commits: [],
          title: extractProjectTitle(commit.commit.message),
          description: extractDescription(commit.commit.message),
          technologies: extractTechnologies(commit.commit.message),
          category: categorizeProject(commit.commit.message),
          complexity: determineComplexity(dayNum, commit.commit.message),
          highlights: extractHighlights(commit.commit.message),
          filesChanged: 0,
          linesAdded: 0,
          githubUrl: `https://github.com/${GITHUB_REPO}/tree/main/day_${dayNum}`,
          isActualProject: dayNum >= 2, // From day 2 onwards, all are projects
        })
      }

      dayMap.get(dayNum).commits.push({
        message: commit.commit.message,
        date: commit.commit.author.date,
        additions: commit.stats?.additions || 0,
        deletions: commit.stats?.deletions || 0,
      })

      // Update aggregated stats
      const dayData = dayMap.get(dayNum)
      dayData.filesChanged += 1
      dayData.linesAdded += commit.stats?.additions || 0
    }
  }

  return Array.from(dayMap.values()).sort((a, b) => a.day - b.b)
}

function extractProjectTitle(message: string): string {
  // Special case for day 100 CommitVerse
  if (message.toLowerCase().includes("commitverse") || message.toLowerCase().includes("day_100")) {
    return "CommitVerse - 100-Day Journey Visualizer"
  }

  const patterns = [
    /🎯.*?Day\s+\d+[:\-–]\s*(.+?)(?:\s*\||$)/i,
    /Day\s+\d+[:\-–]\s*(.+?)(?:\s*\||$)/i,
    /Completed\s+Day\s+\d+[:\-–]\s*(.+?)(?:\s*\||$)/i,
    /Built\s+(.+?)(?:\s*\||$)/i,
    /Added\s+(.+?)(?:\s*\||$)/i,
    /Created\s+(.+?)(?:\s*\||$)/i,
    /Implemented\s+(.+?)(?:\s*\||$)/i,
  ]

  for (const pattern of patterns) {
    const match = message.match(pattern)
    if (match) {
      return match[1].trim().replace(/[🎯]/gu, "").trim()
    }
  }

  return message.replace(/[🎯]/gu, "").trim().substring(0, 50)
}

function extractDescription(message: string): string {
  const cleanMessage = message.replace(/🎯|Day \d+[:\-–]?/gi, "").trim()
  return cleanMessage.length > 100 ? cleanMessage.substring(0, 100) + "..." : cleanMessage
}

function extractTechnologies(message: string): string[] {
  const techKeywords = [
    "Python",
    "FastAPI",
    "Streamlit",
    "OpenAI",
    "MongoDB",
    "Supabase",
    "Next.js",
    "React",
    "AI",
    "ML",
    "NLP",
    "Voice",
    "TTS",
    "Speech",
    "HuggingFace",
    "Transformers",
    "Flask",
    "Django",
    "PostgreSQL",
    "SQLite",
    "Redis",
    "Docker",
    "AWS",
    "JavaScript",
    "TypeScript",
    "Node.js",
    "Express",
    "Vue",
    "Angular",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Git",
    "GitHub",
    "Vercel",
    "Heroku",
    "Railway",
    "Render",
    "Jupyter",
    "requests",
    "beautifulsoup4",
    "selenium",
    "tkinter",
    "pygame",
    "opencv",
    "pillow",
    "qrcode",
    "email",
    "smtplib",
    "pyttsx3",
    "speech_recognition",
  ]

  const found = techKeywords.filter((tech) => message.toLowerCase().includes(tech.toLowerCase()))

  return found.length > 0 ? found : ["Python"]
}

function categorizeProject(message: string): string {
  // Special case for CommitVerse
  if (message.toLowerCase().includes("commitverse")) {
    return "Web Applications"
  }

  const categories = {
    "AI/ML Tools": [
      "ai",
      "ml",
      "openai",
      "huggingface",
      "transformers",
      "nlp",
      "voice",
      "speech",
      "emotion",
      "sentiment",
    ],
    "Web Applications": [
      "web",
      "app",
      "streamlit",
      "fastapi",
      "flask",
      "django",
      "next.js",
      "react",
      "dashboard",
      "ui",
    ],
    "CLI Applications": ["cli", "command", "terminal", "script", "console"],
    "Database Projects": ["database", "mongodb", "sql", "supabase", "postgres", "sqlite", "crud"],
    "SaaS Applications": ["saas", "multi-user", "admin", "dashboard", "subscription", "enterprise", "team"],
    "Data Analysis": ["data", "analysis", "pandas", "numpy", "visualization", "chart", "analytics"],
    "Utility Tools": ["tool", "utility", "helper", "generator", "converter", "calculator", "organizer"],
    "Games & Entertainment": ["game", "quiz", "puzzle", "entertainment", "fun", "play"],
  }

  const lowerMessage = message.toLowerCase()

  for (const [category, keywords] of Object.entries(categories)) {
    if (keywords.some((keyword) => lowerMessage.includes(keyword))) {
      return category
    }
  }

  return "Utility Tools"
}

function determineComplexity(dayNum: number, message: string): "Beginner" | "Intermediate" | "Advanced" {
  // Day 100 is definitely Advanced!
  if (dayNum === 100) return "Advanced"

  const advancedKeywords = ["saas", "multi-user", "admin", "enterprise", "ai", "ml", "api integration", "commitverse"]
  const intermediateKeywords = ["web app", "database", "authentication", "dashboard", "full-stack"]

  const lowerMessage = message.toLowerCase()

  if (dayNum >= 75 || advancedKeywords.some((keyword) => lowerMessage.includes(keyword))) {
    return "Advanced"
  } else if (dayNum >= 25 || intermediateKeywords.some((keyword) => lowerMessage.includes(keyword))) {
    return "Intermediate"
  }

  return "Beginner"
}

function extractHighlights(message: string): string[] {
  const highlights = []

  if (message.includes("AI")) highlights.push("AI Integration")
  if (message.includes("voice") || message.includes("speech")) highlights.push("Voice Processing")
  if (message.includes("real-time")) highlights.push("Real-time Features")
  if (message.includes("multi-user") || message.includes("admin")) highlights.push("Multi-user System")
  if (message.includes("dashboard")) highlights.push("Analytics Dashboard")
  if (message.includes("export")) highlights.push("Export Functionality")
  if (message.toLowerCase().includes("commitverse")) highlights.push("Portfolio Showcase")

  return highlights
}
