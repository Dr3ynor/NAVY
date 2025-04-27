import numpy as np
import plotly.graph_objects as go
import random

def apply_transform(point, transform):
    x, y, z = point
    a, b, c, d, e, f, g, h, i, j, k, l = transform
    
    new_x = a * x + b * y + c * z + j
    new_y = d * x + e * y + f * z + k
    new_z = g * x + h * y + i * z + l
    
    return (new_x, new_y, new_z)

def generate_fractal(transforms, probabilities, iterations=50000, start_point=(0, 0, 0)):
    points = [start_point]
    current_point = start_point
    
    for _ in range(iterations):
        transform_idx = random.choices(range(len(transforms)), weights=probabilities, k=1)[0]
        transform = transforms[transform_idx]
        
        current_point = apply_transform(current_point, transform)
        points.append(current_point)
    
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    z_coords = [p[2] for p in points]
    
    return x_coords, y_coords, z_coords

first_model_transforms = [
    [0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00],
    [-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00],
    [0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00]
]

second_model_transforms = [
    [0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45, 0.00, 1.00, 0.00],
    [-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45, 0.00, 1.25, 0.00],
    [0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00]
]

probabilities = [0.25, 0.25, 0.25, 0.25]



x1, y1, z1 = generate_fractal(first_model_transforms, probabilities)
x2, y2, z2 = generate_fractal(second_model_transforms, probabilities)

fig1 = go.Figure(data=[
    go.Scatter3d(
        x=x1, y=y1, z=z1,
        mode='markers',
        marker=dict(
            size=1,
            color=z1,
            colorscale='Viridis',
            opacity=0.8
        ),
        name="Model 1"
    )
])

fig1.update_layout(
    title_text="3D Fern-like Fractal - First Model",
    width=1920,
    height=1080,
    scene=dict(
        aspectmode='data',
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

fig2 = go.Figure(data=[
    go.Scatter3d(
        x=x2, y=y2, z=z2,
        mode='markers',
        marker=dict(
            size=1,
            color=z2,
            colorscale='Plasma',
            opacity=0.8
        ),
        name="Model 2"
    )
])

fig2.update_layout(
    title_text="3D Fern-like Fractal - Second Model",
    width=1920,
    height=1080,
    scene=dict(
        aspectmode='data',
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

fig1.show()
fig2.show()
