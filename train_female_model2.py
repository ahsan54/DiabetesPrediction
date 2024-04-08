# train_model.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv("D:/DPS/DPS updated/data/FemalData.csv")

# Data Preprocessing
X = data.drop("DiagnosisInFuture", axis=1)  # Independent variables
Y = data['DiagnosisInFuture']  # Dependent variable

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model Training
model = LogisticRegression(max_iter=1000, solver='lbfgs')
model.fit(X_scaled, Y)

# Save the model and scaler to files with custom names
joblib.dump(model, 'ModelFemalData.pkl')
joblib.dump(scaler, 'ScalerFemalData.pkl')
