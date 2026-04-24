# Fake Job Posting Detection System

## Overview
This project develops a machine learning system to identify fraudulent job postings. By analyzing textual features such as job descriptions, company profiles, and requirements, the system learns to distinguish between legitimate opportunities and scams.

## Key Features
- **In-depth EDA**: Exploration of dataset distributions and patterns.
- **Advanced Text Preprocessing**: Cleaning, tokenization, and noise reduction.
- **Text Vectorization**: Transforming unstructured text into numerical data using TF-IDF.
- **Multiple Classifiers**: Comparison between Logistic Regression and Naive Bayes models.
- **Functional Prediction System**: A command-line tool for classifying new job postings.

## Project Structure
- `generate_data.py`: Script to generate synthetic data for demonstration.
- `analysis.py`: Main script for EDA, preprocessing, training, and evaluation.
- `predict.py`: Interactive script for real-time job posting classification.
- `fake_job_postings.csv`: The dataset (generated).
- `*.pkl`: Saved models and vectorizer for deployment.

## Technical Implementation

### 1. Data Exploration & Preprocessing
- **Handling Missing Values**: Empty fields in textual columns are filled with empty strings.
- **Text Cleaning**: Removal of special characters, numbers, URLs, and stop words to focus on meaningful keywords.
- **Feature Engineering**: Concatenation of multiple text fields (`title`, `description`, `requirements`, etc.) to provide a holistic view of the posting.

### 2. Transformation
We utilized **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert text into a matrix of TF-IDF features. This method highlights words that are unique and descriptive for specific documents while downplaying common words across all documents.

### 3. Model Performance
Two models were evaluated:
- **Logistic Regression**: Effective for high-dimensional text data and provides probability scores.
- **Naive Bayes (Multinomial)**: Computationally efficient and robust for text classification.

*Note: In the synthetic dataset provided, both models achieved high accuracy due to clear patterns in fraudulent postings (e.g., use of urgent keywords and unrealistic promises).*

## Interpretation & Decision Making
The model primarily makes decisions based on:
1. **Keyword Analysis**: Words like "urgent", "no experience", "high pay", and "work from home" often correlate with fraudulent postings in the training data.
2. **Company Profile**: Legitimate postings typically have more structured and specific company information.
3. **Tone and Language**: Scam postings often use sensationalist language to attract victims.

## Real-World Limitations
While effective, the system has limitations:
- **Adversarial Evolution**: Scammers constantly change their tactics to mimic legitimate postings.
- **Cold Start Problem**: New types of scams may not be recognized if they differ significantly from historical data.
- **Contextual Nuance**: Some legitimate jobs (e.g., genuine remote entry-level roles) might be misclassified as scams if they share common keywords.

## Web Application
The project includes a premium web interface with a "reddish-blue" (Indigo/Pink) aesthetic. It uses a Flask backend to serve predictions in real-time.

### Backend (`app.py`)
- Built with Flask and Flask-CORS.
- Exposes a `/predict` JSON endpoint.
- Integrates the trained Logistic Regression model.

### Frontend (`index.html`, `style.css`, `script.js`)
- Modern glassmorphism UI.
- Responsive design for mobile and desktop.
- Dynamic result gauges and animations.

## How to Use

### ⚡ Quick Start
You can now start the entire application (including dependency checks and training) with a single command:

**On Windows (PowerShell):**
```powershell
./run_local.ps1
```

**On Linux/Mac/Git Bash:**
```bash
bash run_local.sh
```

### Manual Setup
1. **Prepare Data & Model**:
   ```bash
   python generate_data.py
   python analysis.py
   ```
2. **Start the Backend**:
   ```bash
   python app.py
   ```
3. **Open the Frontend**:
   Open `index.html` in your web browser.
