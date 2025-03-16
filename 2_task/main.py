import numpy as np
import matplotlib.pyplot as plt

# Sigmoid aktivace a její derivace
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Funkce pro výpočet SSE (suma čtvercových chyb)
def sse(y_true, y_pred):
    return np.sum((y_true - y_pred) ** 2) / 2

# Trénovací data pro XOR problém
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Inicializace vah a biasů náhodně
np.random.seed(42)
input_size = 2
hidden_size = 2
output_size = 1
errors = []
losses = []

W1 = np.random.randn(input_size, hidden_size)
b1 = np.random.randn(hidden_size)
W2 = np.random.randn(hidden_size, output_size)
b2 = np.random.randn(output_size)

learning_rate = 0.5
epochs = 10_000

# Trénování sítě
for epoch in range(epochs):
    # Forward pass
    hidden_input = np.dot(X, W1) + b1
    hidden_output = sigmoid(hidden_input)
    
    final_input = np.dot(hidden_output, W2) + b2
    final_output = sigmoid(final_input)
    
    # Výpočet chyby
    error = y - final_output
    errors.append(np.mean(np.abs(error)))
    loss = sse(y, final_output)
    losses.append(loss)
    
    # Backpropagation
    d_output = error * sigmoid_derivative(final_output)
    d_hidden = np.dot(d_output, W2.T) * sigmoid_derivative(hidden_output)
    
    # Aktualizace vah a biasů
    W2 += learning_rate * np.dot(hidden_output.T, d_output)
    b2 += learning_rate * np.sum(d_output, axis=0)
    W1 += learning_rate * np.dot(X.T, d_hidden)
    b1 += learning_rate * np.sum(d_hidden, axis=0)
    
    # Výpis chyby každých 1000 epoch
    if epoch % 1000 == 0:
        print(f'Epoch {epoch}, Loss: {loss:.5f}')

# Výstup po trénování
print("Final Output:")
print(final_output)

# Vizualizace chyby a lossu
plt.plot(errors, label="Error")
plt.plot(losses, label="Loss")
plt.xlabel("Epoch")
plt.ylabel("Error/Loss")
plt.legend()
plt.title("Chyba a loss během trénování")
plt.show()