import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Youtube, Upload } from "lucide-react"

export function Navigation() {
  return (
    <nav className="border-b bg-white/80 backdrop-blur sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <Youtube className="h-6 w-6 text-red-600" />
            Title Optimizer
          </Link>

          <div className="flex gap-2">
            <Button variant="ghost" asChild>
              <Link href="/">Single Title</Link>
            </Button>
            <Button variant="ghost" asChild>
              <Link href="/batch">
                <Upload className="mr-2 h-4 w-4" />
                Batch Process
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
