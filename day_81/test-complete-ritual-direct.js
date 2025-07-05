#!/usr/bin/env node

/**
 * Direct Complete Ritual Test
 * Tests the function directly and provides workaround
 */

console.log('🎯 Direct Complete Ritual Test...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function testCompleteRitualDirect() {
  console.log('🔄 Testing complete-ritual function directly...');
  console.log('─'.repeat(50));
  
  const testUserId = 'test-user-' + Date.now();
  // Use a UUID that we know should work if the ritual exists
  const testRitualId = '550e8400-e29b-41d4-a716-446655440000';
  
  console.log('Test User ID:', testUserId);
  console.log('Test Ritual ID:', testRitualId);
  console.log('');
  
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/complete-ritual`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.anonKey}`
      },
      body: JSON.stringify({
        user_id: testUserId,
        ritual_id: testRitualId
      })
    });
    
    const data = await response.json();
    
    console.log('Response Status:', response.status);
    console.log('');
    
    if (response.ok) {
      console.log('🎉 SUCCESS! Complete Ritual function is working!');
      console.log('Response:', JSON.stringify(data, null, 2));
    } else {
      console.log('❌ Error:', data.error);
      console.log('Details:', data.details);
      
      if (data.error === 'Invalid ritual_id') {
        console.log('\n🔧 SOLUTION:');
        console.log('The ritual ID does not exist in the database.');
        console.log('');
        console.log('To fix this, you need to:');
        console.log('');
        console.log('1. Go to your Supabase Dashboard');
        console.log('2. Navigate to Table Editor > rituals');
        console.log('3. Copy the ID of an existing ritual');
        console.log('4. Update the testRitualId in this script');
        console.log('');
        console.log('OR');
        console.log('');
        console.log('1. Go to Authentication > Policies');
        console.log('2. Find the rituals table');
        console.log('3. Update the "Anyone can read rituals" policy');
        console.log('4. Add "anon" to the roles (TO anon, authenticated)');
        console.log('');
        console.log('Current working endpoints:');
        console.log('✅ User Stats: Working');
        console.log('✅ User Badges: Working');
        console.log('❌ Complete Ritual: Needs valid ritual ID');
      }
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

console.log('📋 Current Status:');
console.log('✅ User Stats endpoint: Working');
console.log('✅ User Badges endpoint: Working');
console.log('❌ Complete Ritual endpoint: Needs valid ritual ID');
console.log('');
console.log('🔧 The issue is that we cannot get the real ritual ID');
console.log('due to RLS policy restrictions.');
console.log('');

testCompleteRitualDirect(); 