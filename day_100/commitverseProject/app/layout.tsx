import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "CommitVerse - Uday Kumar's 100-Day Python + AI Journey",
  description:
    "An interactive portfolio showcasing Uday Kumar's transformation from Python beginner to AI developer over 100 days",
  keywords: ["portfolio", "python", "ai", "journey", "projects", "github", "uday kumar", "100 days of code"],
  authors: [{ name: "Uday Kumar" }],
  openGraph: {
    title: "CommitVerse - Uday Kumar's 100-Day Journey",
    description: "Explore Uday Kumar's incredible transformation from Python beginner to AI developer",
    type: "website",
  },
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
