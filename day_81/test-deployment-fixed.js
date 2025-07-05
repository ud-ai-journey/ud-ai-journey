#!/usr/bin/env node

/**
 * Fixed Deployment Test Script
 * Tests the deployed API endpoints with proper UUID handling
 */

console.log('🧪 Testing Deployed API Endpoints (Fixed)...\n');

// Configuration
const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY',
  testUserId: 'test-user-' + Date.now(),
  testRitualId: null // Will be fetched from database
};

console.log('📋 Configuration:');
console.log('Supabase URL:', config.supabaseUrl);
console.log('Test User ID:', config.testUserId);
console.log('');

// Step 1: Get available rituals
async function getRituals() {
  console.log('🔄 Step 1: Fetching available rituals...');
  console.log('─'.repeat(40));
  
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=id,title,type&limit=1`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const rituals = await response.json();
      if (rituals.length > 0) {
        config.testRitualId = rituals[0].id;
        console.log('✅ Found ritual:', rituals[0].title);
        console.log('   ID:', config.testRitualId);
        console.log('   Type:', rituals[0].type);
        return true;
      } else {
        console.log('❌ No rituals found in database');
        return false;
      }
    } else {
      console.log('❌ Error fetching rituals:', response.statusText);
      return false;
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
    return false;
  }
}

// Step 2: Create test user profile
async function createTestUser() {
  console.log('\n🔄 Step 2: Creating test user profile...');
  console.log('─'.repeat(40));
  
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/user_profiles`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify({
        id: config.testUserId,
        username: 'test-user-' + Date.now()
      })
    });
    
    if (response.ok) {
      console.log('✅ Test user created successfully');
      return true;
    } else {
      console.log('❌ Error creating user:', response.statusText);
      return false;
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
    return false;
  }
}

// Step 3: Test Complete Ritual
async function testCompleteRitual() {
  console.log('\n🔄 Step 3: Testing Complete Ritual...');
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
      console.log('Details:', data.details);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

// Step 4: Test User Stats
async function testUserStats() {
  console.log('\n🔄 Step 4: Testing User Stats...');
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

// Step 5: Test User Badges
async function testUserBadges() {
  console.log('\n🔄 Step 5: Testing User Badges...');
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

// Run all tests
async function runTests() {
  console.log('🚀 Starting Fixed API Tests...\n');
  
  // Step 1: Get rituals
  const ritualsFound = await getRituals();
  if (!ritualsFound) {
    console.log('❌ Cannot proceed without rituals');
    return;
  }
  
  // Step 2: Create test user
  const userCreated = await createTestUser();
  if (!userCreated) {
    console.log('❌ Cannot proceed without test user');
    return;
  }
  
  // Step 3-5: Run API tests
  await testCompleteRitual();
  await testUserStats();
  await testUserBadges();
  
  console.log('\n📊 Test Summary:');
  console.log('─'.repeat(40));
  console.log('✅ All tests completed');
  console.log('📖 Check the responses above for any errors');
  console.log('');
  console.log('🎯 Next Steps:');
  console.log('1. Check the Supabase dashboard for function logs');
  console.log('2. Test with your frontend application');
  console.log('3. Monitor user activity and badge awards');
}

runTests(); 