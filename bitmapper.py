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
TOP_FPS = 12
TOP_FRAME_DELAY = 1 / TOP_FPS

# Display setup


def display_image(
    image: Image.Image,
    window: pygame.surface.Surface,
    position: tuple[int, int],
    render: bool = True,
):
    """
    Places image onto window at position.
    """
    # Convert the PIL image to a Pygame surface
    surface = pygame.image.frombytes(
        image.tobytes(), image.size, "RGB"  # type:ignore
    ).convert()
    # Overlays the surface onto window
    window.blit(surface, position)
    # Updates the window if rendering
    if render:
        pygame.display.flip()


def extract_gif_frames(gif_image: Image.Image) -> list[Image.Image]:
    """
    Collects images from gif into list of frames.
    """
    # Initializes list for frames
    frames: list[Image.Image] = []
    # For each frame:
    for frame_index in range(gif_image.n_frames):
        # Set the current frame
        gif_image.seek(frame_index)
        # Adds frame to list
        frames.append(gif_image.copy().convert("RGB"))
    # Returns list of frame  images
    return frames


def display_gif():
    # Sets up pygame
    pygame.init()
    # Creates window for frame and scaled frame
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Fills with background color
    window.fill(BG_COLOR)
    # Adds window caption
    pygame.display.set_caption("Mirror Animation Preview")

    # Creates path for image samples
    samples_path = Path("samples")
    image = Image.open(samples_path / "flag.png")
    motor_gif = Image.open(samples_path / "motor.gif")
    # Acquires image frames from gif
    motor_frames = extract_gif_frames(motor_gif)
    # For each frame
    for frame in motor_frames:
        # Creates larger scaled frame for display
        scaled_frame = frame.resize((SCALE_SIZE, SCALE_SIZE), Image.Resampling.NEAREST)
        # Draws the frame and scaled frame
        display_image(frame, window, (0, 0), False)
        display_image(scaled_frame, window, (MIRROR_WIDTH, 0), False)
        # Renders window surface
        pygame.display.flip()
        # Delays according to FPS
        time.sleep(TOP_FRAME_DELAY)


if __name__ == "__main__":
    try:
        display_gif()
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
