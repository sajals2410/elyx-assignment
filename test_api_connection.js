// Quick test script to verify API connection
const fetch = require('node-fetch');

async function testConnection() {
  try {
    console.log('Testing API connection...');
    const response = await fetch('http://localhost:5001/api/health');
    console.log('Status:', response.status);
    console.log('Headers:', Object.fromEntries(response.headers));
    const data = await response.json();
    console.log('Response:', data);
    console.log('✅ API connection successful!');
  } catch (error) {
    console.error('❌ API connection failed:', error.message);
  }
}

testConnection();
