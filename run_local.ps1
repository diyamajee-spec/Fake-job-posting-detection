Write-Host "🚀 Starting GuardJob: Fake Job Posting Detection System..." -ForegroundColor Cyan

# Check if requirements are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Generate data and train model if not present
if (-not (Test-Path "advanced_model_pipeline.pkl")) {
    Write-Host "🧠 Model not found. Initializing training..." -ForegroundColor Magenta
    python generate_data.py
    python analysis.py
}

# Start the Flask backend
Write-Host "🌐 Starting backend server at http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "🖥️ Please open index.html in your browser to use the application." -ForegroundColor Gray
python app.py
