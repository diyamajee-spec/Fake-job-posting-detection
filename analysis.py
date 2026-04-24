import pandas as pd
import numpy as np
import re
import string
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

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

def run_advanced_analysis():
    print("Loading dataset...")
    df = pd.read_csv("fake_job_postings.csv")
    
    # Preprocessing
    df.fillna('', inplace=True)
    
    # Feature Engineering: Combine all text fields
    df['combined_text'] = (df['title'] + ' ' + df['company_profile'] + ' ' + 
                          df['description'] + ' ' + df['requirements'] + ' ' + 
                          df['benefits']).apply(clean_text)
    
    # Define features
    text_features = 'combined_text'
    categorical_features = ['employment_type', 'required_experience', 'required_education', 'industry']
    binary_features = ['telecommuting', 'has_company_logo', 'has_questions']
    
    X = df[['combined_text', 'employment_type', 'required_experience', 'required_education', 'industry', 'telecommuting', 'has_company_logo', 'has_questions']]
    y = df['fraudulent']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Text Transformer (TF-IDF with n-grams)
    text_transformer = TfidfVectorizer(max_features=10000, stop_words='english', ngram_range=(1, 2))
    
    # Categorical Transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Binary/Numeric Transformer
    binary_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent'))
    ])
    
    # Combine into a ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', text_transformer, 'combined_text'),
            ('cat', categorical_transformer, categorical_features),
            ('bin', binary_transformer, binary_features)
        ]
    )
    
    # Ensemble Model (Voting Classifier)
    clf1 = LogisticRegression(max_iter=1000)
    clf2 = RandomForestClassifier(n_estimators=200, random_state=42)
    clf3 = MultinomialNB()
    
    ensemble = VotingClassifier(
        estimators=[('lr', clf1), ('rf', clf2), ('nb', clf3)],
        voting='soft'
    )
    
    # Create Full Pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', ensemble)
    ])
    
    print("Training Super-Sufficient Ensemble Model...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model_pipeline.predict(X_test)
    print("\n--- Advanced Ensemble Model Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save Pipeline
    joblib.dump(model_pipeline, 'advanced_model_pipeline.pkl')
    print("\nAdvanced model pipeline saved.")

if __name__ == "__main__":
    run_advanced_analysis()
