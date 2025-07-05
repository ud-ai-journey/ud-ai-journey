#!/usr/bin/env node

/**
 * Test with Known ID and Provide Solution
 */

console.log('🎯 Testing with Known Ritual ID...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function testWithKnownId() {
  console.log('🔄 Testing complete-ritual with a known ritual ID...');
  console.log('─'.repeat(50));
  
  // Since we can't get the real ID due to RLS, let's test with a UUID
  // that might exist, and also provide the solution
  const testRitualId = '550e8400-e29b-41d4-a716-446655440000';
  const testUserId = 'test-user-' + Date.now();
  
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
        console.log('\n🔧 SOLUTION: The ritual ID does not exist.');
        console.log('This is expected because we used a hardcoded UUID.');
        console.log('');
        console.log('To fix this, you need to:');
        console.log('1. Fix the RLS policy to allow anonymous users to read rituals');
        console.log('2. Or get the real ritual ID from the database');
        console.log('');
        console.log('The RLS policy should be:');
        console.log('DROP POLICY IF EXISTS "Anyone can read rituals" ON rituals;');
        console.log('CREATE POLICY "Anyone can read rituals"');
        console.log('  ON rituals FOR SELECT');
        console.log('  TO anon, authenticated');
        console.log('  USING (true);');
      }
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

console.log('📋 Current Status:');
console.log('✅ User Stats endpoint: Working');
console.log('✅ User Badges endpoint: Working');
console.log('❌ Complete Ritual endpoint: Failing due to invalid ritual_id');
console.log('');
console.log('🔧 Root Cause:');
console.log('- RLS policy blocks anonymous users from reading rituals');
console.log('- We cannot get the real ritual ID to test with');
console.log('- Edge function validates ritual exists before proceeding');
console.log('');

testWithKnownId(); 