import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your dataset
data = pd.read_csv('data/Casualties.csv')  # Adjust path if needed

# Define your features and target
features = ['Sex_of_Casualty', 'Age_of_Casualty', 'Casualty_Severity']
target = 'Casualty_Severity'

# Prepare the features and target
X = data[features]
y = data[target]

# Encode categorical features
label_encoders = {}
for column in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    label_encoders[column] = le

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'trained_model.pkl')
