# Enhanced Backend Deployment Setup Script
# This script helps set up the deployment environment

Write-Host "🚀 Enhanced Backend Deployment Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "supabase")) {
    Write-Host "❌ Error: Not in the correct directory. Please run this from the day_81 folder." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found Supabase directory" -ForegroundColor Green

# Check for required files
$requiredFiles = @(
    "supabase/migrations/20250706000000_enhanced_badges_system.sql",
    "supabase/functions/types.ts",
    "supabase/functions/utils/streak-utils.ts",
    "supabase/functions/utils/badge-utils.ts",
    "supabase/functions/complete-ritual/index.ts",
    "supabase/functions/user-stats/index.ts",
    "supabase/functions/user-badges/index.ts"
)

Write-Host "📁 Checking required files..." -ForegroundColor Yellow

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file - MISSING" -ForegroundColor Red
    }
}

Write-Host "`n🔧 Installation Options:" -ForegroundColor Cyan
Write-Host "1. Install Supabase CLI via Chocolatey (Recommended)" -ForegroundColor White
Write-Host "2. Manual installation from website" -ForegroundColor White
Write-Host "3. Skip CLI installation and deploy manually" -ForegroundColor White

$choice = Read-Host "`nChoose an option (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n📦 Installing Chocolatey..." -ForegroundColor Yellow
        try {
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            
            Write-Host "✅ Chocolatey installed successfully" -ForegroundColor Green
            
            Write-Host "📦 Installing Supabase CLI..." -ForegroundColor Yellow
            choco install supabase -y
            
            Write-Host "✅ Supabase CLI installed successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "❌ Failed to install via Chocolatey: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "Please try option 2 or 3" -ForegroundColor Yellow
        }
    }
    "2" {
        Write-Host "`n🌐 Manual Installation Instructions:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://supabase.com/docs/guides/cli" -ForegroundColor White
        Write-Host "2. Download the Windows executable" -ForegroundColor White
        Write-Host "3. Add to PATH or run from the directory" -ForegroundColor White
        Write-Host "4. Restart PowerShell after installation" -ForegroundColor White
    }
    "3" {
        Write-Host "`n📋 Manual Deployment Steps:" -ForegroundColor Yellow
        Write-Host "1. Create Supabase project at: https://supabase.com/dashboard" -ForegroundColor White
        Write-Host "2. Copy migration SQL to Supabase SQL Editor" -ForegroundColor White
        Write-Host "3. Create edge functions manually in dashboard" -ForegroundColor White
        Write-Host "4. Copy function code from the supabase/functions/ directory" -ForegroundColor White
    }
    default {
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n📚 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create a Supabase project at https://supabase.com/dashboard" -ForegroundColor White
Write-Host "2. Get your project reference ID" -ForegroundColor White
Write-Host "3. Run: supabase link --project-ref YOUR_PROJECT_REF" -ForegroundColor White
Write-Host "4. Run: supabase db push" -ForegroundColor White
Write-Host "5. Run: supabase functions deploy complete-ritual" -ForegroundColor White
Write-Host "6. Run: supabase functions deploy user-stats" -ForegroundColor White
Write-Host "7. Run: supabase functions deploy user-badges" -ForegroundColor White

Write-Host "`n📖 Documentation:" -ForegroundColor Cyan
Write-Host "• DEPLOYMENT_GUIDE.md - Complete deployment instructions" -ForegroundColor White
Write-Host "• TESTING_GUIDE.md - How to test your deployment" -ForegroundColor White
Write-Host "• README.md - Complete implementation guide" -ForegroundColor White

Write-Host "`n🎉 Your enhanced backend is ready for deployment!" -ForegroundColor Green 