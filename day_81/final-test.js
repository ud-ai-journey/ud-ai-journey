#!/usr/bin/env node

/**
 * Final Test Script
 * Gets actual ritual ID and tests complete-ritual function
 */

console.log('🎯 Final Test - Complete Ritual with Real Data...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function getRealRitualAndTest() {
  console.log('🔍 Step 1: Getting real ritual from database...');
  console.log('─'.repeat(50));
  
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=*`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const rituals = await response.json();
      console.log('Found rituals:', rituals.length);
      
      if (rituals.length > 0) {
        const ritual = rituals[0];
        console.log('✅ Using ritual:');
        console.log('   Title:', ritual.title);
        console.log('   Type:', ritual.type);
        console.log('   ID:', ritual.id);
        console.log('');
        
        // Test with this real ritual ID
        await testCompleteRitual(ritual.id);
      } else {
        console.log('❌ No rituals found');
      }
    } else {
      console.log('❌ Error fetching rituals:', response.statusText);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

async function testCompleteRitual(ritualId) {
  console.log('🔄 Step 2: Testing complete-ritual function...');
  console.log('─'.repeat(50));
  
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
      console.log('🎉 SUCCESS! Complete Ritual function is working!');
      console.log('Response:', JSON.stringify(data, null, 2));
      
      // Test the other endpoints to see updated stats
      console.log('\n🔄 Step 3: Testing updated stats...');
      console.log('─'.repeat(50));
      await testUpdatedStats(testUserId);
      
    } else {
      console.log('❌ Error:', data.error);
      console.log('Details:', data.details);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

async function testUpdatedStats(userId) {
  // Test user stats
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/user-stats?user_id=${userId}`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`
      }
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('✅ Updated User Stats:');
      console.log(JSON.stringify(data.stats, null, 2));
    }
  } catch (error) {
    console.log('❌ Error getting updated stats:', error.message);
  }
  
  // Test user badges
  try {
    const response = await fetch(`${config.supabaseUrl}/functions/v1/user-badges?user_id=${userId}`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`
      }
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('\n✅ Updated User Badges:');
      console.log('Earned badges:', data.badges.earned.length);
      if (data.badges.earned.length > 0) {
        console.log('First earned badge:', data.badges.earned[0]);
      }
    }
  } catch (error) {
    console.log('❌ Error getting updated badges:', error.message);
  }
}

getRealRitualAndTest(); 