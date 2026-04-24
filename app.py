from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import re
import string

app = Flask(__name__)
CORS(app)

# Load dataset for random samples
try:
    df_data = pd.read_csv('fake_job_postings.csv')
    df_data.fillna('', inplace=True)
except Exception as e:
    print(f"Error loading CSV: {e}")

# Load advanced model pipeline
try:
    model_pipeline = joblib.load('advanced_model_pipeline.pkl')
except Exception as e:
    print(f"Error loading model pipeline: {e}")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Text features
    title = data.get('title', '')
    company_profile = data.get('company_profile', '')
    description = data.get('description', '')
    requirements = data.get('requirements', '')
    benefits = data.get('benefits', '')
    
    combined_text = clean_text(f"{title} {company_profile} {description} {requirements} {benefits}")
    
    # Metadata features
    input_df = pd.DataFrame([{
        'combined_text': combined_text,
        'employment_type': data.get('employment_type', 'Full-time'),
        'required_experience': data.get('required_experience', 'Entry level'),
        'required_education': data.get('required_education', 'Unspecified'),
        'industry': data.get('industry', 'Other'),
        'telecommuting': int(data.get('telecommuting', 0)),
        'has_company_logo': int(data.get('has_company_logo', 0)),
        'has_questions': int(data.get('has_questions', 0))
    }])
    
    # Predict
    prediction = model_pipeline.predict(input_df)[0]
    probability = model_pipeline.predict_proba(input_df)[0]
    
    result = "Fraudulent" if prediction == 1 else "Legitimate"
    confidence = float(probability[1] if prediction == 1 else probability[0])
    
    return jsonify({
        "result": result,
        "confidence": confidence,
        "is_fraudulent": bool(prediction)
    })

@app.route('/random_sample', methods=['GET'])
def get_random_sample():
    if df_data is not None:
        sample = df_data.sample(1).iloc[0].to_dict()
        # Convert any NaN to empty string for JSON
        sample = {k: ("" if pd.isna(v) else v) for k, v in sample.items()}
        return jsonify(sample)
    return jsonify({"error": "Dataset not loaded"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
