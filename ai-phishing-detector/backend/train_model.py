import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

def load_and_prepare_data():
    """Load data from data folder and prepare training dataset"""
    
    # Load legitimate emails
    legit_df = pd.read_csv('../data/legitimate_emails.csv')
    legit_df['label'] = 0  # 0 for legitimate
    
    # Load phishing emails
    phishing_df = pd.read_csv('../data/phishing_emails.csv')
    phishing_df['label'] = 1  # 1 for phishing
    
    # Combine datasets
    df = pd.concat([legit_df, phishing_df], ignore_index=True)
    
    # Drop any rows with missing data
    df = df.dropna(subset=['subject', 'body'])
    
    # Combine subject and body for feature extraction
    df['email_text'] = df['subject'].astype(str) + ' ' + df['body'].astype(str)
    
    return df

def train_model():
    """Train the phishing detection model"""
    
    try:
        # Load and prepare data
        print("Loading and preparing training data...")
        df = load_and_prepare_data()
        print(f"Loaded {len(df)} emails ({df['label'].sum()} phishing, {len(df) - df['label'].sum()} legitimate)")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            df['email_text'], 
            df['label'], 
            test_size=0.2, 
            random_state=42,
            stratify=df['label']  # Ensure balanced split
        )
        
        # Vectorize text
        print("Vectorizing text...")
        vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)
        
        # Train model
        print("Training model...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_vec, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test_vec)
        
        print("\n=== Model Performance ===")
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"Recall: {recall_score(y_test, y_pred, zero_division=0):.4f}")
        print(f"F1-Score: {f1_score(y_test, y_pred, zero_division=0):.4f}")
        
        # Save model and vectorizer
        print("\nSaving model...")
        joblib.dump(model, 'phishing_model.pkl')
        joblib.dump(vectorizer, 'vectorizer.pkl')
        print("Model and vectorizer saved successfully")
        
        # Also save the prepared dataset for reference
        df.to_csv('emails.csv', index=False)
        print("Training data saved as emails.csv")
        
    except FileNotFoundError as e:
        print(f"Error: Data files not found: {e}")
        print("Make sure legitimate_emails.csv and phishing_emails.csv exist in the data folder")
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == '__main__':
    train_model()
