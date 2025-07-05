#!/usr/bin/env node

/**
 * Script to fetch available rituals from Supabase
 */

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function getRituals() {
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=id,title,type`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const rituals = await response.json();
      console.log('Available Rituals:');
      console.log('─'.repeat(50));
      rituals.forEach((ritual, index) => {
        console.log(`${index + 1}. ${ritual.title} (${ritual.type})`);
        console.log(`   ID: ${ritual.id}`);
        console.log('');
      });
      
      if (rituals.length > 0) {
        console.log('✅ Use the first ritual ID for testing:');
        console.log(`   ${rituals[0].id}`);
      }
    } else {
      console.log('❌ Error fetching rituals:', response.statusText);
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
  }
}

getRituals(); 