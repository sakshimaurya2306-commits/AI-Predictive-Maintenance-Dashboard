import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from preprocess import load_data, preprocess

# Load & preprocess data
data = load_data()
X, y = preprocess(data)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/model.pkl")

print("✅ Model Trained Successfully!")