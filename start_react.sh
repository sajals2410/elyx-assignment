#!/bin/bash
# Start both Flask API and React frontend

echo "🚀 Starting Resource Allocator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Start Flask API in background
echo "📡 Starting Flask API on port 5000..."
python api.py &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Start React frontend
echo "⚛️  Starting React frontend on port 3000..."
cd frontend
npm start &
REACT_PID=$!

echo ""
echo "✅ Both servers are starting!"
echo "   - API: http://localhost:5000"
echo "   - React: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $API_PID $REACT_PID 2>/dev/null; exit" INT TERM
wait
