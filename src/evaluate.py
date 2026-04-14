import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
from preprocess import load_data, preprocess
from sklearn.model_selection import train_test_split

# Load data
data = load_data()
X, y = preprocess(data)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Load model
model = joblib.load("models/model.pkl")

# Predict
y_pred = model.predict(X_test)

# Accuracy
acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {acc*100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig("outputs/confusion_matrix.png")
plt.show()