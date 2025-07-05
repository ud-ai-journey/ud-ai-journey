#!/usr/bin/env node

/**
 * Get Real Ritual ID and Test
 */

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function getRealRitualAndTest() {
  console.log('🔍 Getting real ritual ID...\n');
  
  try {
    // First, let's try to get all rituals
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=*`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    console.log('Response Status:', response.status);
    console.log('Response Headers:', Object.fromEntries(response.headers.entries()));
    console.log('');
    
    if (response.ok) {
      const rituals = await response.json();
      console.log('Found rituals:', rituals.length);
      
      if (rituals.length > 0) {
        const ritual = rituals[0];
        console.log('Using ritual:', ritual.title);
        console.log('Ritual ID:', ritual.id);
        console.log('Ritual Type:', ritual.type);
        console.log('');
        
        // Now test with this real ritual ID
        await testWithRealRitual(ritual.id);
      } else {
        console.log('❌ No rituals found');
      }
    } else {
      const errorText = await response.text();
      console.log('❌ Error fetching rituals:', errorText);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

async function testWithRealRitual(ritualId) {
  console.log('🔄 Testing with real ritual ID...');
  console.log('─'.repeat(40));
  
  const testUserId = 'test-user-' + Date.now();
  
  console.log('Test User ID:', testUserId);
  console.log('Real Ritual ID:', ritualId);
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
        ritual_id: ritualId
      })
    });
    
    const data = await response.json();
    
    console.log('Response Status:', response.status);
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

getRealRitualAndTest(); 