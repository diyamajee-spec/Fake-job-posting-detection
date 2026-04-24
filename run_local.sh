#!/bin/bash

echo "🚀 Starting GuardJob: Fake Job Posting Detection System..."

# Check if requirements are installed
echo "📦 Checking dependencies..."
pip install -r requirements.txt --quiet

# Generate data and train model if not present
if [ ! -f "advanced_model_pipeline.pkl" ]; then
    echo "🧠 Model not found. Initializing training..."
    python generate_data.py
    python analysis.py
fi

# Start the Flask backend
echo "🌐 Starting backend server at http://127.0.0.1:5000"
echo "🖥️ Please open index.html in your browser to use the application."
python app.py
