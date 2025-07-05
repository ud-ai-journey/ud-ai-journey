#!/bin/bash

# One-Minute Wins - Enhanced Backend Deployment Script
# This script helps deploy the enhanced backend with all improvements

set -e

echo "🚀 Deploying One-Minute Wins Enhanced Backend..."

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI not found. Please install it first:"
    echo "   npm install -g supabase"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "supabase/config.toml" ]; then
    echo "❌ Not in a Supabase project directory. Please run this from the project root."
    exit 1
fi

echo "📦 Applying database migrations..."
supabase db push

echo "🔧 Deploying Edge Functions..."
supabase functions deploy complete-ritual
supabase functions deploy user-stats
supabase functions deploy user-badges

echo "✅ Deployment complete!"
echo ""
echo "🔍 To verify deployment:"
echo "   1. Check your Supabase dashboard"
echo "   2. Verify the badges table was created"
echo "   3. Test the API endpoints"
echo ""
echo "📚 For more information, see README.md" 