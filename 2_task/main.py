import numpy as np
import matplotlib.pyplot as plt

# Sigmoid funkce a její derivace
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Funkce pro výpočet SSE
def sse(y_true, y_pred):
    return np.sum((y_true - y_pred) ** 2) / 2

# Trénovací data pro XOR problém
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # vstup
y = np.array([[0], [1], [1], [0]]) # výstup

# Náhodná inicializace vah a biasů
np.random.seed(42)
input_size = 2
hidden_size = 2
output_size = 1

# Tracking
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
    
    # Backpropagation (Zpětná úprava vah na základě erroru)
    d_output = error * sigmoid_derivative(final_output)
    d_hidden = np.dot(d_output, W2.T) * sigmoid_derivative(hidden_output)
    
    # Aktualizace vah a biasů
    W1 += learning_rate * np.dot(X.T, d_hidden) # váhy - vstupní -> skrytá vrstva
    W2 += learning_rate * np.dot(hidden_output.T, d_output) # váhy - skrytá -> výstupní vrstva

    b1 += learning_rate * np.sum(d_hidden, axis=0) # bias - skrytá vrstva
    b2 += learning_rate * np.sum(d_output, axis=0) # bias - výstupní vrstva
    
    if epoch % 1000 == 0:
        print(f'Epoch {epoch}, Loss: {loss:.5f}')

print("Final Output:")
print(final_output)



# Vizualizace chyby a lossu
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(errors, label="Error")
plt.plot(losses, label="Loss")
plt.xlabel("Epoch")
plt.ylabel("Error/Loss")
plt.legend()
plt.title("Chyba a loss během trénování")

# Subplot
plt.subplot(1, 2, 2)
xx, yy = np.meshgrid(np.linspace(-0.1, 1.1, 100), np.linspace(-0.1, 1.1, 100))
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Forward pass pro mřížku bodů
hidden_input = np.dot(grid_points, W1) + b1
hidden_output = sigmoid(hidden_input)
final_input = np.dot(hidden_output, W2) + b2
grid_predictions = sigmoid(final_input).reshape(xx.shape)

# Vykreslení rozhodovací hranice
plt.contourf(xx, yy, grid_predictions, levels=[0, 0.5, 1], alpha=0.6, cmap="coolwarm")
plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), edgecolors='k', cmap="coolwarm")
plt.xlabel("X1")
plt.ylabel("X2")
plt.title("Rozhodovací hranice")

plt.show()

