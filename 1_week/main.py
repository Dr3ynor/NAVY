
from matplotlib import pyplot as plt
import random

def generate_random_points(num_points=100):
    points = []
    for _ in range(num_points):
        x = random.randint(0, 200)
        y = random.randint(0, 600)
        points.append((x, y))
    return points

def plot_points(points):
    x, y = zip(*points)
    plt.plot(x, y, marker='o', linestyle='None')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of points')

def function(x):
    return 3*x+2

def calculate_plot_function():
    function_x = [i for i in range(200)]
    function_y = [function(i) for i in function_x]
    plt.plot(function_x, function_y)


def main():
    points = generate_random_points()
    plot_points(points)
    calculate_plot_function()
    plt.show()
if __name__ == "__main__":
    main()