import os
from pathlib import Path
from typing import Tuple

import numpy as np

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import time

import pygame
from PIL import Image, ImageChops

# Display values
MIRROR_WIDTH = 24
MIRROR_HEIGHT = 24

DISPLAY_SCALE = 20

WINDOW_WIDTH = MIRROR_WIDTH * (1 + DISPLAY_SCALE)
WINDOW_HEIGHT = MIRROR_HEIGHT * DISPLAY_SCALE

BG_COLOR = (127, 127, 127)

# Animation values
RUNNING_FPS = 4
RUNNING_FRAME_DELAY = 1 / RUNNING_FPS

PIXEL_FPS = 2
PIXEL_FRAME_DELAY = 1 / PIXEL_FPS


def draw_image(
    pil_image: Image.Image,
    window: pygame.surface.Surface,
    position: tuple[int, int],
    render: bool = True,
    scale: float = 1,
) -> None:
    """
    Places image onto window at position. Optional parameter to render window.
    """
    # Converts the image back to RGB
    rgb_image = pil_image.convert("RGB")
    # Convert the PIL image to a Pygame surface
    surface = pygame.image.frombytes(
        rgb_image.tobytes(), rgb_image.size, "RGB"  # type:ignore
    ).convert()

    if scale != 1:
        surface = pygame.transform.scale(
            surface, (surface.get_width() * scale, surface.get_height() * scale)
        )
    # Overlays the surface onto window
    window.blit(surface, position)
    # Updates the window if rendering
    if render:
        pygame.display.flip()


def draw_array(
    array: np.ndarray,
    window: pygame.surface.Surface,
    position: tuple[int, int],
    render: bool = True,
    scale: float = 1,
) -> None:
    """
    Places image onto window at position. Optional parameter to render window.
    """
    # Creates pygame surface from numpy array
    surface = pygame.surfarray.make_surface(array)
    # Scales if specified
    if scale != 1:
        surface = pygame.transform.scale(
            surface, (surface.get_width() * scale, surface.get_height() * scale)
        )
    # Overlays the surface onto window
    window.blit(surface, position)
    # Updates the window if rendering
    if render:
        pygame.display.flip()


# pygame_surface = pygame.surfarray.make_surface(numpy_array)


def extract_gif_frames(gif_image: Image.Image) -> list[np.ndarray]:
    """
    Collects images from gif into list of frames. Optional parameter for image
    format.
    """
    # Initializes list for frames
    frames: list[np.ndarray] = []
    # For each frame:
    for frame_index in range(gif_image.n_frames):
        # Set the current frame
        gif_image.seek(frame_index)
        # Turns image to boolean array
        array = np.array(
            # Copies, resizes, and converts to bitmap
            gif_image.copy()
            .resize((MIRROR_WIDTH, MIRROR_HEIGHT), Image.Resampling.NEAREST)
            .convert("1")
        )
        # Casts contents to integers and transposes axes
        oriented_array = np.transpose(array.astype(int), (1, 0))
        # Adds frame to list
        frames.append(oriented_array)
    # Returns list of frame  images
    return frames


def display_gif(filename: str) -> None:
    """
    Plays gif on screen.
    """
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
    # image = Image.open(samples_path / "spiral.png")

    # binary_array = np.all(spiral_array >= 200, axis=1).astype(int)
    # for col in average_values:
    #     for item in col:
    #         print(item, end=" - ")
    #     print("\n")
    # print(spiral_array)
    # scaled_image = image.resize((SCALE_SIZE, SCALE_SIZE), Image.Resampling.NEAREST)
    # time.sleep(2)
    gif_image = Image.open(samples_path / filename)
    # Acquires image frames from gif
    frames = extract_gif_frames(gif_image)
    # Initializes frame storage and pizel timings arrays
    previous_frame = np.zeros((MIRROR_WIDTH, MIRROR_HEIGHT))
    pixel_timings = previous_frame
    # Converts image to numpy array
    # For each frame
    for frame in frames:
        start_time = time.time()
        difference_mask = np.abs(previous_frame - frame)
        # Draws the frame and scaled frame
        draw_array(frame, window, (0, 0), False)
        draw_array(frame, window, (MIRROR_WIDTH, 0), False, DISPLAY_SCALE)
        # draw_image(gif_image, window, (MIRROR_WIDTH, 0), False, DISPLAY_SCALE)
        # Renders window surface
        pygame.display.flip()
        # Delays according to FPS
        time.sleep(RUNNING_FRAME_DELAY)


# def find_difference(image_a: Image.Image, image_b: Image.Image) -> Image.Image:


if __name__ == "__main__":
    try:
        display_gif("worm.gif")
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
