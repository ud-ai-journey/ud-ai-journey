export interface GitCommit {
  message: string
  date: string
  additions: number
  deletions: number
}

export interface JourneyDay {
  day: number
  date: string
  title: string
  description: string
  technologies: string[]
  category: string
  complexity: "Beginner" | "Intermediate" | "Advanced"
  commits: GitCommit[]
  filesChanged: number
  linesAdded: number
  highlights: string[]
  demoUrl?: string
  githubUrl: string
}

export interface JourneyStats {
  totalDays: number
  totalProjects: number
  totalCommits: number
  totalLinesOfCode: number
  technologiesUsed: string[]
  categoriesExplored: string[]
  skillProgression: SkillLevel[]
}

export interface SkillLevel {
  week: number
  level: string
  projects: number
}

export interface FilterState {
  technologies: string[]
  categories: string[]
  searchQuery: string
  sortBy?: string
  sortOrder?: string
}
