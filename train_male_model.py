import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load data
data = pd.read_csv("D:/DPS/DPS updated/MaleData.csv")

# Define features (X) and target (Y)
X = data.drop("DiagnosisInFuture", axis=1)  # Independent variables
Y = data['DiagnosisInFuture']  # Dependent variable

# Define preprocessing steps
numeric_cols = ['Age', 'BMI', 'HbA1c']
categorical_cols = ['FamilyHistory', 'Exercise', 'Smoking', 'HealthyDiet']

numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)])

# Define the model
model = LogisticRegression(max_iter=1000, solver='lbfgs')

# Create a pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

# Fit the pipeline on the training data
pipeline.fit(X, Y)

# Save the model
joblib.dump(pipeline, 'ModelMaleData.pkl')

scaler = pipeline.named_steps['preprocessor'].named_transformers_['num']
joblib.dump(scaler, 'ScalerMaleData.pkl')

