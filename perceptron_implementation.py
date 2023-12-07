# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OMubtRgVOKE1lJM67LA1SntIJxk6Kbdq
"""

!pip install numpy

pip install scikit-learn

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, num_features, learning_rate=0.1, max_epochs=100):
        self.weights = np.zeros(num_features)
        self.bias = 0
        self.learning_rate = learning_rate
        self.max_epochs = max_epochs

    def predict(self, x):
        weighted_sum = np.dot(self.weights, x) + self.bias
        return 1 if weighted_sum > 0 else 0

    def train(self, X, y):
        for epoch in range(self.max_epochs):
            errors = 0
            for i in range(len(X)):
                prediction = self.predict(X[i])
                error = y[i] - prediction
                self.weights += self.learning_rate * error * X[i]
                self.bias += self.learning_rate * error
                errors += int(error != 0)
            if errors == 0:
                print(f"Converged after {epoch+1} epochs")
                return
        print("Did not converge within the maximum number of epochs.")

# Cargar el conjunto de datos Iris
iris = datasets.load_iris()
X = iris.data[:100, :2]  # Usar solo las dos primeras características (longitud del sépalo y longitud del pétalo)
y = iris.target[:100]  # Clases: 0 para Setosa y 1 para No-Setosa

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Estandarizar características (escalar)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Crear una instancia del Perceptrón
num_features = X_train.shape[1]
perceptron = Perceptron(num_features, learning_rate=0.1, max_epochs=100)

# Entrenar el Perceptrón
perceptron.train(X_train, y_train)

# Evaluar el modelo en el conjunto de prueba
correct = 0
total = len(X_test)
for i in range(total):
    prediction = perceptron.predict(X_test[i])
    if prediction == y_test[i]:
        correct += 1

accuracy = correct / total
print(f"Accuracy on test data: {accuracy * 100:.2f}%")

# Visualización de la decisión
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='viridis', marker='o')
x_min, x_max = X_test[:, 0].min() - 1, X_test[:, 0].max() + 1
y_min, y_max = X_test[:, 1].min() - 1, X_test[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))
Z = np.array([perceptron.predict(x) for x in np.c_[xx.ravel(), yy.ravel()]])
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Petal Length (cm)')
plt.title('Perceptron Decision Boundary')
plt.show()