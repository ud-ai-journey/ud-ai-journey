#!/usr/bin/env node

/**
 * Database State Checker
 */

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function checkDatabase() {
  console.log('🔍 Checking Database State...\n');
  
  // Check rituals table
  console.log('1. Checking rituals table...');
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=count`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   Rituals count:', data.length);
      
      if (data.length === 0) {
        console.log('   ❌ No rituals found. Inserting sample ritual...');
        await insertSampleRitual();
      } else {
        console.log('   ✅ Rituals found');
      }
    } else {
      console.log('   ❌ Error:', response.statusText);
    }
  } catch (error) {
    console.log('   ❌ Network Error:', error.message);
  }
  
  // Check user_profiles table
  console.log('\n2. Checking user_profiles table...');
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/user_profiles?select=count`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   User profiles count:', data.length);
    } else {
      console.log('   ❌ Error:', response.statusText);
    }
  } catch (error) {
    console.log('   ❌ Network Error:', error.message);
  }
}

async function insertSampleRitual() {
  try {
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
    
    if (response.ok) {
      const ritual = await response.json();
      console.log('   ✅ Sample ritual inserted:', ritual[0].id);
      return ritual[0].id;
    } else {
      console.log('   ❌ Error inserting ritual:', response.statusText);
      return null;
    }
  } catch (error) {
    console.log('   ❌ Network Error:', error.message);
    return null;
  }
}

checkDatabase(); 