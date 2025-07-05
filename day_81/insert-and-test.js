#!/usr/bin/env node

/**
 * Insert Ritual and Test
 */

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function insertRitualAndTest() {
  console.log('🔧 Inserting test ritual...\n');
  
  try {
    // Insert a test ritual
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey,
        'Prefer': 'return=representation'
      },
      body: JSON.stringify({
        type: 'reflection',
        title: 'Test Gratitude Ritual',
        description: 'A simple test ritual for debugging',
        content: {
          prompts: ['What are you grateful for today?']
        }
      })
    });
    
    console.log('Insert Response Status:', response.status);
    
    if (response.ok) {
      const ritual = await response.json();
      console.log('✅ Ritual inserted successfully!');
      console.log('Ritual ID:', ritual[0].id);
      console.log('Ritual Title:', ritual[0].title);
      console.log('');
      
      // Now test with this ritual
      await testWithRitual(ritual[0].id);
    } else {
      const errorText = await response.text();
      console.log('❌ Error inserting ritual:', errorText);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

async function testWithRitual(ritualId) {
  console.log('🔄 Testing complete-ritual function...');
  console.log('─'.repeat(40));
  
  const testUserId = 'test-user-' + Date.now();
  
  console.log('Test User ID:', testUserId);
  console.log('Ritual ID:', ritualId);
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

insertRitualAndTest(); 