#!/usr/bin/env node

/**
 * Simple Test Script
 * Tests the complete-ritual function directly
 */

console.log('🧪 Simple API Test...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

// Test with a simple UUID format
async function testCompleteRitual() {
  console.log('🔄 Testing Complete Ritual...');
  console.log('─'.repeat(40));
  
  const testUserId = 'test-user-' + Date.now();
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
    console.log('Response Headers:', Object.fromEntries(response.headers.entries()));
    console.log('');
    
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

testCompleteRitual(); 