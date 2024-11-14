# model_predictions.py
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

def create_target(data):
    # Create a binary target variable where 1 = next price is higher, 0 = lower
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    data.dropna(inplace=True)  # Drop rows with NaN values from shifting
    return data

def train_model(data):
    # Generate the target variable
    data = create_target(data)

    # Define features and target
    features = ['SMA_20', 'RSI', 'MACD']
    X = data[features]
    y = data['Target']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions and calculate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Random Forest Model Accuracy: {accuracy:.2f}")

    # Add predictions to the data for backtesting
    data['Prediction'] = model.predict(X)

    return data, model
