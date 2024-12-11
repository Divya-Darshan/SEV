import pygame
import sys
import os
import math

pygame.init()

# Get display info for full screen resolution
info = pygame.display.Info()
initial_width, initial_height = info.current_w, info.current_h

# Initialize window in fullscreen mode
screen = pygame.display.set_mode((initial_width, initial_height)) #pygame.RESIZABLE | #pygame.FULLSCREEN
pygame.display.set_caption('SEV')
clock = pygame.time.Clock()

# File paths
current_dir = os.path.dirname(__file__)
background_path = os.path.join(current_dir, 'img', 'back.jpg')
character_path = os.path.join(current_dir, 'img', 'Start.png')

# Load assets
background = pygame.image.load(background_path).convert()
character = pygame.image.load(character_path).convert_alpha()

# Joystick properties
joystick_center = (200, initial_height - 200)  # Position of joystick base
joystick_radius = 50  # Radius of the joystick base
joystick_knob_radius = 20  # Radius of the knob
joystick_knob_pos = list(joystick_center)  # Position of the knob
joystick_active = False  # Tracks if joystick is being used

# Character properties
char_x = 650
char_y = 530
speed = 3

# Variables to track window size
window_width, window_height = initial_width, initial_height

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Quit Pygame
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            # Update the window size dynamically
            window_width, window_height = event.w, event.h
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE | pygame.FULLSCREEN)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Activate joystick if mouse is within knob area
            mouse_pos = pygame.mouse.get_pos()
            if distance(mouse_pos, joystick_knob_pos) <= joystick_knob_radius:
                joystick_active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Reset joystick when mouse is released
            joystick_active = False
            joystick_knob_pos = list(joystick_center)
        elif event.type == pygame.MOUSEMOTION:
            # Move the knob if joystick is active
            if joystick_active:
                mouse_pos = pygame.mouse.get_pos()
                dx = mouse_pos[0] - joystick_center[0]
                dy = mouse_pos[1] - joystick_center[1]
                dist = distance(mouse_pos, joystick_center)
                if dist > joystick_radius:
                    # Constrain knob to joystick radius
                    dx = (dx / dist) * joystick_radius
                    dy = (dy / dist) * joystick_radius
                joystick_knob_pos = [joystick_center[0] + dx, joystick_center[1] + dy]

    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and char_x > 0:
        char_x -= speed
    if keys[pygame.K_RIGHT] and char_x < window_width - character.get_width():
        char_x += speed
    if keys[pygame.K_UP] and char_y > 0:
        char_y -= speed
    if keys[pygame.K_DOWN] and char_y < window_height - character.get_height():
        char_y += speed
    if keys[pygame.K_ESCAPE]:
            pygame.display.iconify()

    # Calculate movement based on joystick knob position
    dx = joystick_knob_pos[0] - joystick_center[0]
    dy = joystick_knob_pos[1] - joystick_center[1]
    char_x += dx / joystick_radius * speed
    char_y += dy / joystick_radius * speed

    # Constrain character to screen boundaries
    char_x = max(0, min(window_width - character.get_width(), char_x))
    char_y = max(0, min(window_height - character.get_height(), char_y))

    # Draw assets
   # scaled_background = pygame.transform.scale(background, (window_width, window_height))
    screen.blit(background, (0, 0))
    screen.blit(character, (char_x, char_y))

    # Draw joystick
    pygame.draw.circle(screen, (150, 150, 150), joystick_center, joystick_radius)  # Joystick base
    pygame.draw.circle(screen, (255, 0, 0), (int(joystick_knob_pos[0]), int(joystick_knob_pos[1])), joystick_knob_radius)

    # Update display
    pygame.display.update()
    clock.tick(60)
