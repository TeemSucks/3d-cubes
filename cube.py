import pygame
import math

pygame.init()

screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("THE CUBE")

cube_size = 50
cube_points = [(-cube_size, -cube_size, -cube_size),
               (cube_size, -cube_size, -cube_size),
               (cube_size, cube_size, -cube_size),
               (-cube_size, cube_size, -cube_size),
               (-cube_size, -cube_size, cube_size),
               (cube_size, -cube_size, cube_size),
               (cube_size, cube_size, cube_size),
               (-cube_size, cube_size, cube_size)]

cube_faces = [(0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2),
              (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5)]

face_colors = {
    (0, 1, 2, 3): (100, 100, 100),
    (0, 4, 5, 1): (120, 120, 120),
    (1, 5, 6, 2): (140, 140, 140),
    (2, 6, 7, 3): (160, 160, 160),
    (3, 7, 4, 0): (180, 180, 180),
    (4, 7, 6, 5): (200, 200, 200)
}

angle_x = 0
angle_y = 0
angle_z = 0
rotation_increment = 0.01

camera_distance = 300
camera_speed = 10.0
min_camera_distance = 50
max_camera_distance = 500

zoom = 1.0
zoom_speed = 0.1

mouse_dragging = False
prev_mouse_pos = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_dragging = True
            prev_mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_dragging = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            zoom += zoom_speed
            if zoom > 2.0:
                zoom = 2.0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            zoom -= zoom_speed
            if zoom < 0.5:
                zoom = 0.5

    if mouse_dragging:
        current_mouse_pos = pygame.mouse.get_pos()
        delta_x = current_mouse_pos[0] - prev_mouse_pos[0]
        delta_y = current_mouse_pos[1] - prev_mouse_pos[1]

        angle_x -= delta_y * rotation_increment
        angle_y += delta_x * rotation_increment

        prev_mouse_pos = current_mouse_pos

    screen.fill((0, 0, 0))

    rotation_x = [[1, 0, 0],
                  [0, math.cos(angle_x), -math.sin(angle_x)],
                  [0, math.sin(angle_x), math.cos(angle_x)]]

    rotation_y = [[math.cos(angle_y), 0, math.sin(angle_y)],
                  [0, 1, 0],
                  [-math.sin(angle_y), 0, math.cos(angle_y)]]

    rotation_z = [[math.cos(angle_z), -math.sin(angle_z), 0],
                  [math.sin(angle_z), math.cos(angle_z), 0],
                  [0, 0, 1]]

    camera_matrix = [[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, -camera_distance],
                     [0, 0, 0, 1]]

    cube_points_rotated = []

    for point in cube_points:
        point_rotated = point
        point_rotated = [sum([rotation_x[i][j] * point_rotated[j] for j in range(3)]) for i in range(3)]
        point_rotated = [sum([rotation_y[i][j] * point_rotated[j] for j in range(3)]) for i in range(3)]
        point_rotated = [sum([rotation_z[i][j] * point_rotated[j] for j in range(3)]) for i in range(3)]

        point_rotated.append(1)
        point_rotated = [sum([camera_matrix[i][j] * point_rotated[j] for j in range(4)]) for i in range(3)]

        cube_points_rotated.append(point_rotated)

    sorted_faces = sorted(cube_faces, key=lambda face: sum([cube_points_rotated[i][2] for i in face]))

    for face in sorted_faces:
        points = [cube_points_rotated[i] for i in face]
        color = face_colors[face]

        normal = [0, 0, 0]
        for i in range(3):
            normal[0] += (points[i][1] - points[i - 1][1]) * (points[i][2] + points[i - 1][2])
            normal[1] += (points[i][2] - points[i - 1][2]) * (points[i][0] + points[i - 1][0])
            normal[2] += (points[i][0] - points[i - 1][0]) * (points[i][1] + points[i - 1][1])
        length = math.sqrt(sum([n ** 2 for n in normal]))
        if length != 0:
            normal = [n / length for n in normal]
        shading = sum([normal[i] * rotation_z[i][2] for i in range(3)])

        color = tuple(int(max(0, min(255, c * shading))) for c in color)

        points = [(p[0] * zoom, p[1] * zoom, p[2] * zoom) for p in points]

        pygame.draw.polygon(screen, color, [(p[0] + screen_width / 2, p[1] + screen_height / 2) for p in points])

    pygame.display.update()
