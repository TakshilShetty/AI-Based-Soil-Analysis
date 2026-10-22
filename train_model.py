import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib
import os

def train_and_save_model():
    # 1. Update this to the exact name of your CSV file
    file_name = "data.csv" 
    
    # 2. Check if the file exists
    if not os.path.exists(file_name):
        print(f"Error: Could not find '{file_name}' in the current folder.")
        print("Please ensure your CSV is in the same folder as this script.")
        return 

    # 3. Load the data
    try:
        df = pd.read_csv(file_name)
        print(f"Successfully loaded '{file_name}'.")
    except Exception as e:
        print(f"Error reading the CSV: {e}")
        return

    # 4. Isolate features
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph']]
    y = df['label']
    
    # 5. Fit the k-NN Model
    print("Fitting Scaled k-NN Pipeline Model (k=8)...")
    model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=8)
    )
    model.fit(X, y)
    
    # 6. Save the model
    joblib.dump(model, 'model.pkl')
    print("Success! Trained model file created as 'model.pkl'.")

if __name__ == "__main__":
    train_and_save_model()