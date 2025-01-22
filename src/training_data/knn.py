import pandas as pd
import numpy as np
import math

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

from sklearn.metrics import confusion_matrix, f1_score, accuracy_score

# Load the dataset
dataset = pd.read_csv('dataset.csv')
print(len(dataset))
print(dataset.head())

# Encode categorical features (e.g., 'L', 'B') into numerical values
label_encoder = LabelEncoder()
for column in dataset.columns[:-1]:  # Apply encoding to all feature columns
    dataset[column] = label_encoder.fit_transform(dataset[column])

# Split dataset into features (X) and target (y)
x = dataset.iloc[:, 0:4]  # First 4 columns as features
y = dataset.iloc[:, 4]    # Fifth column as the target
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# Print the suggested value of K (based on the rule of thumb sqrt(n))
print("Suggested K value:", math.sqrt(len(y_train)))

# Define the KNN model
classifier = KNeighborsClassifier(n_neighbors=7, p=2, metric='euclidean')

# Train the model
classifier.fit(x_train, y_train)

# Predict the test set results
y_pred = classifier.predict(x_test)
# print(y_pred)

# Evaluate the model
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)

f1 = f1_score(y_test, y_pred, average='macro')
print("F1 Score:", f1)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
