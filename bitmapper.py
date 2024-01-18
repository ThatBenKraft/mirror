import os
from pathlib import Path

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import time

import pygame
from PIL import Image

# Display values
MIRROR_WIDTH = 24
MIRROR_HEIGHT = 24

SCALE_SIZE = 500

WINDOW_WIDTH = MIRROR_WIDTH + SCALE_SIZE
WINDOW_HEIGHT = SCALE_SIZE

BG_COLOR = (127, 127, 127)

# Animation values
TOP_FPS = 24
TOP_FRAME_DELAY = 1 / TOP_FPS

# Display setup
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(BG_COLOR)
pygame.display.set_caption("Mirror Animation Preview")


def display_image(
    image: Image.Image, window: pygame.surface.Surface, position: tuple[int, int]
):
    # Convert the PIL image to a Pygame surface
    surface = pygame.image.frombytes(
        image.tobytes(), image.size, "RGB"  # type:ignore
    ).convert()

    # Display the image
    window.blit(surface, position)
    pygame.display.flip()


samples_path = Path("samples/")

mirror_image = Image.open(samples_path / "flag.png")

motor_gif = Image.open(samples_path / "motor.gif")


def extract_gif_frames(gif_image: Image.Image):
    try:
        for frame_index in range(gif_image.n_frames):
            # Set the current frame
            gif_image.seek(frame_index)
            current_frame = gif_image.copy()

            # Process the current frame as needed
            # For example, you can display or save the frame
            width, height = current_frame.size
            print(f"Frame {frame_index} - Size: {width} x {height}")

    except EOFError:
        # Reached the end of the GIF
        pass


extract_gif_frames(motor_gif)

# Display the original image

# Resize the image to 200x200 pixels with nearest-neighbor interpolation
scaled_image = mirror_image.resize((SCALE_SIZE, SCALE_SIZE), Image.Resampling.NEAREST)

# Display the scaled-up image
display_image(mirror_image, window, (0, 0))
display_image(scaled_image, window, (MIRROR_WIDTH, 0))

# Wait for user input to close the window
continue_display = True
while continue_display:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continue_display = False
    time.sleep(TOP_FRAME_DELAY)


pygame.quit()
