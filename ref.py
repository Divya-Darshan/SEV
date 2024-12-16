import pygame
import sys
import os
import math

pygame.init()

# Get display info for full screen resolution
info = pygame.display.Info()
initial_width, initial_height = info.current_w, info.current_h

# Initialize window
screen = pygame.display.set_mode((initial_width, initial_height))  # Can switch to RESIZABLE | FULLSCREEN if needed
pygame.display.set_caption('SEV')
clock = pygame.time.Clock()

# File paths
current_dir = os.path.dirname(__file__)
background_path = os.path.join(current_dir, 'img', 'back.jpg')
character_path = os.path.join(current_dir, 'img', 'Start.png')
joystick_base_path = os.path.join(current_dir, 'img', 'base.png')
joystick_knob_path = os.path.join(current_dir, 'img', 'joy.png')

# Load assets
background = pygame.image.load(background_path).convert()
character = pygame.image.load(character_path).convert_alpha()
joystick_base_img = pygame.image.load(joystick_base_path).convert_alpha()
joystick_knob_img = pygame.image.load(joystick_knob_path).convert_alpha()

# Scale joystick images
print(initial_height,initial_width)
joystick_radius = int(min(initial_width, initial_height) * 0.1)  # Radius of the joystick base
joystick_knob_radius = int(joystick_radius * 0.6)   # Radius of the knob
joystick_base_img = pygame.transform.scale(joystick_base_img, (joystick_radius * 2, joystick_radius * 2))
joystick_knob_img = pygame.transform.scale(joystick_knob_img, (joystick_knob_radius * 2, joystick_knob_radius * 2))

# Joystick properties
joystick_center = None  # No initial center; dynamically set on click
joystick_knob_pos = None  # Position of the knob
joystick_active = False  # Tracks if joystick is being used

# Character properties
char_x = initial_width // 4
char_y = initial_height // 4
speed = 8

# Variables to track window size
window_width, window_height = initial_width, initial_height

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            # Update the window size dynamically
            window_width, window_height = event.w, event.h
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Activate joystick at mouse position
            mouse_pos = pygame.mouse.get_pos()
            joystick_center = mouse_pos
            joystick_knob_pos = list(joystick_center)
            joystick_active = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # Deactivate joystick
            joystick_active = False
            joystick_center = None
            joystick_knob_pos = None

        elif event.type == pygame.MOUSEMOTION:
            # Move the knob if joystick is active
            if joystick_active and joystick_center:
                mouse_pos = pygame.mouse.get_pos()
                dx = mouse_pos[0] - joystick_center[0]
                dy = mouse_pos[1] - joystick_center[1]
                dist = distance(mouse_pos, joystick_center)
                if dist > joystick_radius:
                    # Constrain knob to joystick radius
                    dx = (dx / dist) * joystick_radius
                    dy = (dy / dist) * joystick_radius
                joystick_knob_pos = [joystick_center[0] + dx, joystick_center[1] + dy]

    keys = pygame.key.get_pressed()    
    # if keys[pygame.K_LEFT] and char_x > 0:
    #     char_x -= speed
    # if keys[pygame.K_RIGHT] and char_x < window_width - character.get_width():
    #     char_x += speed
    # if keys[pygame.K_UP] and char_y > 0:
    #     char_y -= speed
    # if keys[pygame.K_DOWN] and char_y < window_height - character.get_height():
    #     char_y += speed


    if keys[pygame.K_ESCAPE]:
        pygame.display.iconify()

    # Calculate movement based on joystick knob position
    if joystick_knob_pos and joystick_center:
        dx = joystick_knob_pos[0] - joystick_center[0]
        dy = joystick_knob_pos[1] - joystick_center[1]
        char_x += dx / joystick_radius * speed
        char_y += dy / joystick_radius * speed

    # Constrain character to screen boundaries
    char_x = max(0, min(window_width - character.get_width(), char_x))
    char_y = max(0, min(window_height - character.get_height(), char_y))

    # Draw assets
    scaled_background = pygame.transform.scale(background, (window_width, window_height))
    screen.blit(scaled_background, (0, 0))
    screen.blit(character, (char_x, char_y))

    # Draw joystick if active
    if joystick_center:
        # Calculate positions for blitting
        base_position = (joystick_center[0] - joystick_radius, joystick_center[1] - joystick_radius)
        knob_position = (joystick_knob_pos[0] - joystick_knob_radius, joystick_knob_pos[1] - joystick_knob_radius)

        screen.blit(joystick_base_img, base_position)  # Blit the base image
        screen.blit(joystick_knob_img, knob_position)  # Blit the knob image

    # Update display
    pygame.display.update()
    clock.tick(60)
