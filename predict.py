import joblib
import re
import string

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

def predict_job_posting(title, company_profile, description, requirements, benefits):
    # Load model and vectorizer
    model = joblib.load('logistic_regression_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
    
    # Combine and clean text
    combined_text = f"{title} {company_profile} {description} {requirements} {benefits}"
    cleaned_text = clean_text(combined_text)
    
    # Vectorize
    vectorized_text = tfidf.transform([cleaned_text])
    
    # Predict
    prediction = model.predict(vectorized_text)[0]
    probability = model.predict_proba(vectorized_text)[0]
    
    result = "Fraudulent" if prediction == 1 else "Legitimate"
    confidence = probability[1] if prediction == 1 else probability[0]
    
    return result, confidence

if __name__ == "__main__":
    print("--- Fake Job Posting Detector ---")
    title = input("Enter Job Title: ")
    company_profile = input("Enter Company Profile: ")
    description = input("Enter Job Description: ")
    requirements = input("Enter Requirements: ")
    benefits = input("Enter Benefits: ")
    
    result, confidence = predict_job_posting(title, company_profile, description, requirements, benefits)
    
    print(f"\nResult: {result}")
    print(f"Confidence: {confidence:.2%}")
