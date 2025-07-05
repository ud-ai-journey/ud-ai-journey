#!/usr/bin/env node

/**
 * Simple Deployment Test Script
 * Tests the deployed API endpoints
 */

console.log('🧪 Testing Deployed API Endpoints...\n');

// Configuration - Replace with your actual values
const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co', // e.g., https://abcdefghijklmnop.supabase.co
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY',
  testUserId: 'test-user-' + Date.now(),
  testRitualId: '550e8400-e29b-41d4-a716-446655440000' // Valid UUID format
};

console.log('📋 Configuration:');
console.log('Supabase URL:', config.supabaseUrl);
console.log('Test User ID:', config.testUserId);
console.log('Test Ritual ID:', config.testRitualId);
console.log('');

// Test 1: Complete Ritual
async function testCompleteRitual() {
  console.log('🔄 Test 1: Complete Ritual');
  console.log('─'.repeat(40));
  
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/complete-ritual`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.anonKey}`
      },
      body: JSON.stringify({
        user_id: config.testUserId,
        ritual_id: config.testRitualId
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('✅ Success!');
      console.log('Response:', JSON.stringify(data, null, 2));
    } else {
      console.log('❌ Error:', data.error);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

// Test 2: Get User Stats
async function testUserStats() {
  console.log('\n🔄 Test 2: User Stats');
  console.log('─'.repeat(40));
  
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/user-stats?user_id=${config.testUserId}`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`
      }
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('✅ Success!');
      console.log('Stats:', JSON.stringify(data.stats, null, 2));
    } else {
      console.log('❌ Error:', data.error);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

// Test 3: Get User Badges
async function testUserBadges() {
  console.log('\n🔄 Test 3: User Badges');
  console.log('─'.repeat(40));
  
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/user-badges?user_id=${config.testUserId}`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`
      }
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('✅ Success!');
      console.log('Badges:', JSON.stringify(data.badges, null, 2));
    } else {
      console.log('❌ Error:', data.error);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

// Run tests
async function runTests() {
  console.log('🚀 Starting API Tests...\n');
  
  await testCompleteRitual();
  await testUserStats();
  await testUserBadges();
  
  console.log('\n📊 Test Summary:');
  console.log('─'.repeat(40));
  console.log('✅ All tests completed');
  console.log('📖 Check the responses above for any errors');
  console.log('');
  console.log('🎯 Next Steps:');
  console.log('1. Update the config values with your actual Supabase details');
  console.log('2. Run this script again to test your deployment');
  console.log('3. Check the Supabase dashboard for function logs');
}

// Check if config is set up
if (config.supabaseUrl === 'YOUR_SUPABASE_URL' || config.anonKey === 'YOUR_ANON_KEY') {
  console.log('⚠️  Please update the configuration first:');
  console.log('1. Replace YOUR_SUPABASE_URL with your actual Supabase URL');
  console.log('2. Replace YOUR_ANON_KEY with your actual anon key');
  console.log('3. Run this script again');
} else {
  runTests();
} 