import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("3D Shapes")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Define cube vertices (scaled up)
cube_vertices = [
    [-100, -100, -100],
    [100, -100, -100],
    [100, 100, -100],
    [-100, 100, -100],
    [-100, -100, 100],
    [100, -100, 100],
    [100, 100, 100],
    [-100, 100, 100]
]

# Define pyramid vertices (scaled up)
pyramid_vertices = [
    [0, -100, 0],
    [100, 100, -100],
    [100, 100, 100],
    [-100, 100, 100],
    [-100, 100, -100]
]

# Define cube edges
cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Define pyramid edges
pyramid_edges = [
    (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 2), (2, 3), (3, 4), (4, 1)
]

# Define camera parameters
fov = 720
distance = 1000  # Increased distance between shapes

# Define initial rotation angles
angle_x = 0
angle_y = 0

# Flag for mouse click
mouse_clicked = False

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = False

    # Clear the screen
    screen.fill(BLACK)

    # Get mouse position to control rotation angles only when clicked
    if mouse_clicked:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle_x = (mouse_y - SCREEN_HEIGHT / 2) * 0.01
        angle_y = (mouse_x - SCREEN_WIDTH / 2) * 0.01

    # Calculate rotation matrices
    rot_x = [
        [1, 0, 0],
        [0, math.cos(angle_x), -math.sin(angle_x)],
        [0, math.sin(angle_x), math.cos(angle_x)]
    ]

    rot_y = [
        [math.cos(angle_y), 0, math.sin(angle_y)],
        [0, 1, 0],
        [-math.sin(angle_y), 0, math.cos(angle_y)]
    ]

    # Apply rotation to cube vertices
    rotated_cube_vertices = []
    for vertex in cube_vertices:
        # Apply rotation around x-axis
        x_rotated = [sum([rot_x[i][j] * vertex[i] for i in range(3)]) for j in range(3)]
        # Apply rotation around y-axis
        rotated = [sum([rot_y[i][j] * x_rotated[i] for i in range(3)]) for j in range(3)]
        rotated_cube_vertices.append(rotated)

    # Apply rotation to pyramid vertices
    rotated_pyramid_vertices = []
    for vertex in pyramid_vertices:
        # Apply rotation around x-axis
        x_rotated = [sum([rot_x[i][j] * vertex[i] for i in range(3)]) for j in range(3)]
        # Apply rotation around y-axis
        rotated = [sum([rot_y[i][j] * x_rotated[i] for i in range(3)]) for j in range(3)]
        rotated_pyramid_vertices.append(rotated)

    # Project vertices onto 2D screen for cube
    projected_cube_points = []
    for vertex in rotated_cube_vertices:
        # Perspective projection
        z = vertex[2] + distance
        if z != 0:
            scale = fov / z
            x_proj = int(vertex[0] * scale + SCREEN_WIDTH / 2)
            y_proj = int(vertex[1] * scale + SCREEN_HEIGHT / 2)
            projected_cube_points.append((x_proj, y_proj))
        else:
            # If vertex is behind the camera, skip projection
            projected_cube_points.append(None)

    # Project vertices onto 2D screen for pyramid
    projected_pyramid_points = []
    for vertex in rotated_pyramid_vertices:
        # Perspective projection
        z = vertex[2] + distance
        if z != 0:
            scale = fov / z
            x_proj = int(vertex[0] * scale + SCREEN_WIDTH / 2)
            y_proj = int(vertex[1] * scale + SCREEN_HEIGHT / 2)
            projected_pyramid_points.append((x_proj, y_proj))
        else:
            # If vertex is behind the camera, skip projection
            projected_pyramid_points.append(None)

    # Draw edges of the cube
    for edge in cube_edges:
        start = projected_cube_points[edge[0]]
        end = projected_cube_points[edge[1]]
        if start and end:
            pygame.draw.line(screen, RED, start, end, 2)

    # Draw edges of the pyramid
    for edge in pyramid_edges:
        start = projected_pyramid_points[edge[0]]
        end = projected_pyramid_points[edge[1]]
        if start and end:
            pygame.draw.line(screen, ORANGE, start, end, 2)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
