#!/bin/bash

# Ensure virtual environment is activated if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Virtual environment (.venv) not found. Please create it first."
    exit 1
fi

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check if GOOGLE_API_KEY is set or still placeholder
if [ -z "$GOOGLE_API_KEY" ] || [ "$GOOGLE_API_KEY" = "your-google-api-key-here" ]; then
    echo "⚠️  WARNING: GOOGLE_API_KEY environment variable is not set correctly."
    echo "Please update the .env file with your actual API key for the AI features to work properly."
    echo ""
fi

# Start FastAPI backend server in the background
echo "🚀 Starting FastAPI backend server on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start Streamlit UI in the background
echo "🎨 Starting Streamlit UI on port 8501..."
export STREAMLIT_GATHER_USAGE_STATS=false
streamlit run ui.py --server.port 8501 --server.headless true &
UI_PID=$!

# Define a cleanup function to kill background processes on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $UI_PID 2>/dev/null
    echo "Done."
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM signals to safely shut down the servers
trap cleanup SIGINT SIGTERM

echo "========================================================"
echo "✅ Both servers are running!"
echo "   - FastAPI Backend API:  http://localhost:8000"
echo "   - Streamlit UI:         http://localhost:8501"
echo "========================================================"
echo "Press Ctrl+C to stop both servers."

# Keep the script running and wait for the user to press Ctrl+C
wait
