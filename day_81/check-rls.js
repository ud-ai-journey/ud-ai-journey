#!/usr/bin/env node

/**
 * Check RLS Policies
 */

console.log('🔍 Checking RLS Policies and Ritual Access...\n');

const config = {
  supabaseUrl: 'https://vijwcbryeklsvcgyjqoa.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpandjYnJ5ZWtsc3ZjZ3lqcW9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MDgxNDEsImV4cCI6MjA2NzI4NDE0MX0.9zcYPJQmgeWUDJhkOkaHzCu2owjO0llrhhW7ULdsMMY'
};

async function checkRitualAccess() {
  console.log('🔄 Testing different ritual queries...\n');
  
  // Test 1: Count query (worked before)
  console.log('1. Testing count query...');
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=count`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   ✅ Count query successful:', data.length, 'records');
    } else {
      console.log('   ❌ Count query failed:', response.statusText);
    }
  } catch (error) {
    console.log('   ❌ Count query error:', error.message);
  }
  
  // Test 2: Select all query (failed before)
  console.log('\n2. Testing select all query...');
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=*`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   ✅ Select all query successful:', data.length, 'records');
      if (data.length > 0) {
        console.log('   First ritual:', data[0].title, '(ID:', data[0].id + ')');
      }
    } else {
      const errorText = await response.text();
      console.log('   ❌ Select all query failed:', errorText);
    }
  } catch (error) {
    console.log('   ❌ Select all query error:', error.message);
  }
  
  // Test 3: Select specific fields
  console.log('\n3. Testing select specific fields...');
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=id,title,type`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   ✅ Select specific fields successful:', data.length, 'records');
      if (data.length > 0) {
        console.log('   First ritual:', data[0].title, '(ID:', data[0].id + ')');
      }
    } else {
      const errorText = await response.text();
      console.log('   ❌ Select specific fields failed:', errorText);
    }
  } catch (error) {
    console.log('   ❌ Select specific fields error:', error.message);
  }
  
  // Test 4: Try with different headers
  console.log('\n4. Testing with different headers...');
  try {
    const response = await fetch(`${config.supabaseUrl}/rest/v1/rituals?select=*`, {
      headers: {
        'Authorization': `Bearer ${config.anonKey}`,
        'apikey': config.anonKey,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('   ✅ Different headers successful:', data.length, 'records');
    } else {
      const errorText = await response.text();
      console.log('   ❌ Different headers failed:', errorText);
    }
  } catch (error) {
    console.log('   ❌ Different headers error:', error.message);
  }
}

checkRitualAccess(); 