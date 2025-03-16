import numpy as np
import matplotlib.pyplot as plt

def heaviside_function(x):
    return 1 if x >= 0 else 0

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1, epochs=10):
        self.weights = np.random.randn(input_size + 1)  # Včetně biasu (+1)
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.bias = 1

    def predict(self, x):
        x = np.insert(x, 0, self.bias)  # Přidání biasu
        return heaviside_function(np.dot(self.weights, x)) # Aktivace (Rozhodnutí)

    def train(self, X, y):
        for _ in range(self.epochs):
            for i in range(len(X)):
                x_i = np.insert(X[i], 0, self.bias)  # Přidání biasu k aktuálnímu vstupu
                prediction = self.predict(X[i])  # Předpověď perceptronu
                error = y[i] - prediction  # Výpočet chyby (rozdíl mezi skutečnou a predikovanou hodnotou)
                self.weights += self.learning_rate * error * x_i  # Aktualizace vah podle chyby a rychlosti učení

# Generování dat podle rozhodovací hranice y = 3x + 2
np.random.seed(13)
X = np.random.randn(100, 2)
y = (X[:, 1] > 3 * X[:, 0] + 2).astype(int)  # Rozdělení podle přímky

# Trénování perceptronu
perceptron = Perceptron(input_size=2)
perceptron.train(X, y)

# Vizualizace rozhodovací hranice
xx = np.linspace(-2, 2, 10)
yy = 3 * xx + 2 

plt.scatter(X[:, 0], X[:, 1], c=y, cmap="bwr")
plt.plot(xx, yy, "k--", label="y=3x+2")
plt.xlabel("X1")
plt.ylabel("X2")
plt.title("Perceptron - Lineární klasifikace")
plt.show()
