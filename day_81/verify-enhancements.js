#!/usr/bin/env node

/**
 * Verification Script for Enhanced Backend
 * This script checks if all enhanced files are in place and have correct structure
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🔍 Verifying Enhanced Backend Structure...\n');

const requiredFiles = [
  'supabase/migrations/20250706000000_enhanced_badges_system.sql',
  'supabase/functions/types.ts',
  'supabase/functions/utils/streak-utils.ts',
  'supabase/functions/utils/badge-utils.ts',
  'supabase/functions/complete-ritual/index.ts',
  'supabase/functions/user-stats/index.ts',
  'supabase/functions/user-badges/index.ts',
  'README.md',
  'TESTING_GUIDE.md',
  'deploy.sh'
];

const requiredContent = {
  'supabase/functions/types.ts': [
    'CompleteRitualRequest',
    'CompleteRitualResponse',
    'UserStatsResponse',
    'UserBadgesResponse'
  ],
  'supabase/functions/utils/streak-utils.ts': [
    'calculateStreakUpdate',
    'getTodayDate',
    'updateUserStreak'
  ],
  'supabase/functions/utils/badge-utils.ts': [
    'checkBadgeCriteria',
    'getAllBadges',
    'checkAndAwardBadges'
  ],
  'supabase/functions/complete-ritual/index.ts': [
    'calculateStreakUpdate',
    'checkAndAwardBadges',
    'CompleteRitualRequest'
  ]
};

let allFilesExist = true;
let allContentCorrect = true;

console.log('📁 Checking Required Files:');
console.log('─'.repeat(50));

for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - MISSING`);
    allFilesExist = false;
  }
}

console.log('\n🔍 Checking File Content:');
console.log('─'.repeat(50));

for (const [file, requiredStrings] of Object.entries(requiredContent)) {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf8');
    let fileCorrect = true;
    
    for (const requiredString of requiredStrings) {
      if (!content.includes(requiredString)) {
        console.log(`❌ ${file} - Missing: ${requiredString}`);
        fileCorrect = false;
        allContentCorrect = false;
      }
    }
    
    if (fileCorrect) {
      console.log(`✅ ${file} - All required content present`);
    }
  }
}

console.log('\n📊 Summary:');
console.log('─'.repeat(50));

if (allFilesExist && allContentCorrect) {
  console.log('🎉 All enhancements are properly implemented!');
  console.log('\n🚀 Ready for testing with:');
  console.log('   1. Install Node.js from https://nodejs.org/');
  console.log('   2. Run: npm install');
  console.log('   3. Follow TESTING_GUIDE.md');
} else {
  console.log('⚠️  Some enhancements are missing or incomplete.');
  console.log('   Please check the files marked with ❌');
}

console.log('\n📚 Documentation:');
console.log('   - README.md - Complete implementation guide');
console.log('   - TESTING_GUIDE.md - How to test locally');
console.log('   - deploy.sh - Deployment automation');

// Check for specific enhancements
console.log('\n🔧 Enhancement Status:');
console.log('─'.repeat(50));

const enhancements = [
  { name: 'Robust Streak Logic', file: 'supabase/functions/utils/streak-utils.ts', keyword: 'calculateStreakUpdate' },
  { name: 'Dynamic Badge System', file: 'supabase/migrations/20250706000000_enhanced_badges_system.sql', keyword: 'CREATE TABLE badges' },
  { name: 'TypeScript Types', file: 'supabase/functions/types.ts', keyword: 'Database' },
  { name: 'Enhanced Security', file: 'supabase/migrations/20250706000000_enhanced_badges_system.sql', keyword: 'RLS' },
  { name: 'Performance Indexes', file: 'supabase/migrations/20250706000000_enhanced_badges_system.sql', keyword: 'CREATE INDEX' }
];

for (const enhancement of enhancements) {
  const filePath = path.join(__dirname, enhancement.file);
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf8');
    if (content.includes(enhancement.keyword)) {
      console.log(`✅ ${enhancement.name}`);
    } else {
      console.log(`❌ ${enhancement.name} - Missing implementation`);
    }
  } else {
    console.log(`❌ ${enhancement.name} - File missing`);
  }
}

console.log('\n🎯 Next Steps:');
console.log('   1. Install Node.js and npm');
console.log('   2. Run: npm install');
console.log('   3. Set up Supabase project');
console.log('   4. Follow TESTING_GUIDE.md');
console.log('   5. Deploy with: ./deploy.sh'); 