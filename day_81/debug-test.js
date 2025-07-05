#!/usr/bin/env node

/**
 * Debug Test Script
 * Tests all endpoints with detailed error reporting
 */

console.log('🔍 Debug Test - All Endpoints...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function testAllEndpoints() {
  const testUserId = 'test-user-' + Date.now();
  
  console.log('Test User ID:', testUserId);
  console.log('');
  
  // Test 1: User Stats (should work)
  console.log('🔄 Test 1: User Stats');
  console.log('─'.repeat(40));
  await testEndpoint('user-stats', testUserId);
  
  // Test 2: User Badges (should work)
  console.log('\n🔄 Test 2: User Badges');
  console.log('─'.repeat(40));
  await testEndpoint('user-badges', testUserId);
  
  // Test 3: Complete Ritual (problematic)
  console.log('\n🔄 Test 3: Complete Ritual');
  console.log('─'.repeat(40));
  await testCompleteRitual(testUserId);
  
  // Test 4: Check database tables
  console.log('\n🔄 Test 4: Database Tables');
  console.log('─'.repeat(40));
  await checkDatabaseTables();
}

async function testEndpoint(endpoint, userId) {
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/${endpoint}?user_id=${userId}`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`
      }
    });
    
    const data = await response.json();
    
    console.log('Status:', response.status);
    console.log('Headers:', Object.fromEntries(response.headers.entries()));
    
    if (response.ok) {
      console.log('✅ Success!');
      console.log('Data:', JSON.stringify(data, null, 2));
    } else {
      console.log('❌ Error:', data.error);
      console.log('Details:', data.details);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

async function testCompleteRitual(userId) {
  // Try with a UUID that might exist
  const testRitualId = '550e8400-e29b-41d4-a716-446655440000';
  
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/complete-ritual`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.anonKey}`
      },
      body: JSON.stringify({
        user_id: userId,
        ritual_id: testRitualId
      })
    });
    
    const data = await response.json();
    
    console.log('Status:', response.status);
    console.log('Headers:', Object.fromEntries(response.headers.entries()));
    
    if (response.ok) {
      console.log('✅ Success!');
      console.log('Data:', JSON.stringify(data, null, 2));
    } else {
      console.log('❌ Error:', data.error);
      console.log('Details:', data.details);
      console.log('Full Response:', JSON.stringify(data, null, 2));
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

async function checkDatabaseTables() {
  const tables = ['rituals', 'user_profiles', 'daily_completions', 'user_badges', 'user_streaks'];
  
  for (const table of tables) {
    try {
      const response = await fetch(`${config.supabaseUrl}/rest/v1/${table}?select=count`, {
        headers: {
          'Authorization': `Bearer ${config.anonKey}`,
          'apikey': config.anonKey
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log(`${table}: ${data.length} records`);
      } else {
        console.log(`${table}: Error ${response.status}`);
      }
    } catch (error) {
      console.log(`${table}: Network error`);
    }
  }
}

testAllEndpoints(); 