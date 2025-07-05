#!/usr/bin/env node

/**
 * Final Working Test Script
 * Uses a real UUID for user_id and inserts the user profile before testing
 */

const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

console.log('🎉 Final Working Test Script (UUID fix)...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

const supabase = createClient(config.supabaseUrl, config.anonKey);

async function run() {
  // 1. Sign up a new user
  const email = `testuser+${Date.now()}@example.com`;
  const password = 'TestPassword123!';
  console.log('🔑 Signing up new user:', email);

  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) {
    console.error('❌ Error signing up user:', error.message);
    return;
  }
  const userId = data.user.id;
  console.log('✅ User created with UUID:', userId);

  // 2. Insert user profile
  console.log('📝 Inserting user profile...');
  const profileRes = await fetch(`${config.supabaseUrl}/rest/v1/user_profiles`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.anonKey}`,
      'apikey': config.anonKey,
      'Prefer': 'return=minimal'
    },
    body: JSON.stringify({
      id: userId,
      username: email
    })
  });
  if (!profileRes.ok) {
    const err = await profileRes.text();
    console.error('❌ Error inserting user profile:', err);
    return;
  }
  console.log('✅ User profile inserted.');

  // 3. Get a real ritual ID
  console.log('🔍 Fetching a ritual...');
  const ritualRes = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=id,title&limit=1`, {
    headers: {
      'Authorization': `Bearer ${config.anonKey}`,
      'apikey': config.anonKey
    }
  });
  const rituals = await ritualRes.json();
  if (!rituals.length) {
    console.error('❌ No rituals found.');
    return;
  }
  const ritualId = rituals[0].id;
  console.log('✅ Using ritual:', rituals[0].title, ritualId);

  // 4. Complete the ritual
  console.log('🏁 Completing ritual...');
  const completeRes = await fetch(`${config.supabaseUrl}/functions/v1/complete-ritual`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.anonKey}`
    },
    body: JSON.stringify({
      user_id: userId,
      ritual_id: ritualId
    })
  });
  const completeData = await completeRes.json();
  if (completeRes.ok) {
    console.log('🎉 Ritual completed:', JSON.stringify(completeData, null, 2));
  } else {
    console.error('❌ Error completing ritual:', completeData);
    return;
  }

  // 5. Fetch updated stats
  const statsRes = await fetch(`${config.supabaseUrl}/functions/v1/user-stats?user_id=${userId}`, {
    headers: { 'Authorization': `Bearer ${config.anonKey}` }
  });
  const stats = await statsRes.json();
  console.log('📊 Updated stats:', JSON.stringify(stats, null, 2));

  // 6. Fetch updated badges
  const badgesRes = await fetch(`${config.supabaseUrl}/functions/v1/user-badges?user_id=${userId}`, {
    headers: { 'Authorization': `Bearer ${config.anonKey}` }
  });
  const badges = await badgesRes.json();
  console.log('🏅 Updated badges:', JSON.stringify(badges, null, 2));
}

console.log('📋 Instructions:');
console.log('1. Make sure you have run: npm install uuid');
console.log('2. Run this script to test all endpoints');
console.log('3. Your backend will be fully functional!');
console.log('');

run(); 