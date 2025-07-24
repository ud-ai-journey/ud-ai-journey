import type { JourneyDay, JourneyStats } from "@/types/journey"

export async function generatePDFPortfolio(days: JourneyDay[], stats: JourneyStats) {
  // This would use a library like jsPDF or Puppeteer
  // For now, we'll create a simple HTML version and trigger print
  const htmlContent = generatePortfolioHTML(days, stats)

  const printWindow = window.open("", "_blank")
  if (printWindow) {
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    printWindow.print()
  }
}

export function generateMarkdownResume(days: JourneyDay[], stats: JourneyStats): string {
  return `# 100-Day Python + AI Journey Portfolio

## Journey Overview
- **Duration**: ${stats.totalDays} days of consistent learning
- **Projects Built**: ${stats.totalProjects} unique applications
- **Total Commits**: ${stats.totalCommits}
- **Technologies Mastered**: ${stats.technologiesUsed.length}

## Technologies Used
${stats.technologiesUsed.map((tech) => `- ${tech}`).join("\n")}

## Project Categories
${stats.categoriesExplored.map((category) => `- ${category}`).join("\n")}

## Key Milestones

${days
  .filter((_, i) => i % 10 === 9)
  .map(
    (day) => `
### Day ${day.day}: ${day.title}
- **Category**: ${day.category}
- **Complexity**: ${day.complexity}
- **Technologies**: ${day.technologies.join(", ")}
- **Description**: ${day.description}
- **GitHub**: [View Project](${day.githubUrl})
`,
  )
  .join("\n")}

## Skills Progression
- **Week 1-4**: Python Fundamentals & Basic Projects
- **Week 5-8**: Web Development & API Integration
- **Week 9-12**: AI/ML Tools & Advanced Applications
- **Week 13-14**: SaaS Development & Enterprise Solutions

---
*Generated from CommitVerse - Journey Visualizer*
`
}

export function generateLinkedInPost(days: JourneyDay[], stats: JourneyStats): string {
  const topTechnologies = stats.technologiesUsed.slice(0, 8).join(" • ")
  const advancedProjects = days.filter((d) => d.complexity === "Advanced").length

  return `🎯 100 DAYS. ${stats.totalProjects} PROJECTS. 1 INCREDIBLE JOURNEY.

I just completed my 100-day Python + AI transformation and built "CommitVerse" - an app that reads my entire GitHub history and turns it into an interactive portfolio.

📊 The Numbers:
• ${stats.totalDays} consecutive days of coding
• ${stats.totalProjects} projects built from scratch  
• ${stats.technologiesUsed.length} different technologies mastered
• ${stats.totalCommits} commits pushed to GitHub
• ${advancedProjects} advanced-level applications

🚀 My Evolution:
Day 1: "Hello World" script
Day 100: Full-stack SaaS with AI integration

🛠️ Tech Stack I Mastered:
${topTechnologies}

The best part? CommitVerse itself showcases the skills I learned during this journey - from basic Python scripts to sophisticated web applications with real-time AI processing.

My key projects include:
✅ AI-powered voice assistants
✅ Multi-user SaaS applications  
✅ Real-time sentiment analysis tools
✅ Enterprise-grade admin dashboards
✅ Advanced data visualization systems

This journey taught me that consistency beats perfection. Every single day of coding, no matter how small, compounds into something extraordinary.

🔗 Explore my complete journey: [Your deployed app URL]
💻 Source code: https://github.com/ud-ai-journey/ud-ai-journey

#100DaysOfCode #Python #AI #WebDevelopment #LearningInPublic #TechJourney #SoftwareDeveloper #MachineLearning #FullStack`
}

function generatePortfolioHTML(days: JourneyDay[], stats: JourneyStats): string {
  return `
<!DOCTYPE html>
<html>
<head>
    <title>100-Day Journey Portfolio</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .header { text-align: center; margin-bottom: 40px; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
        .stat-card { background: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center; }
        .project { margin-bottom: 30px; padding: 20px; border-left: 4px solid #007acc; background: #f9f9f9; }
        .tech-tags { margin-top: 10px; }
        .tech-tag { background: #007acc; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>100-Day Python + AI Journey</h1>
        <p>A comprehensive portfolio of projects and learning milestones</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>${stats.totalDays}</h3>
            <p>Days of Learning</p>
        </div>
        <div class="stat-card">
            <h3>${stats.totalProjects}</h3>
            <p>Projects Built</p>
        </div>
        <div class="stat-card">
            <h3>${stats.totalCommits}</h3>
            <p>Total Commits</p>
        </div>
        <div class="stat-card">
            <h3>${stats.technologiesUsed.length}</h3>
            <p>Technologies</p>
        </div>
    </div>
    
    <h2>Project Timeline</h2>
    ${days
      .map(
        (day) => `
        <div class="project">
            <h3>Day ${day.day}: ${day.title}</h3>
            <p><strong>Category:</strong> ${day.category} | <strong>Complexity:</strong> ${day.complexity}</p>
            <p>${day.description}</p>
            <div class="tech-tags">
                ${day.technologies.map((tech) => `<span class="tech-tag">${tech}</span>`).join("")}
            </div>
        </div>
    `,
      )
      .join("")}
</body>
</html>
  `
}
