import pygame


def resize_image(screen, image):
    size = (int(75 * screen.engine.settings.graphic['screen']['resolution_scale'][0]), int(75 * screen.engine.settings.graphic['screen']['resolution_scale'][1]))
    if image.get_size() != size:
        return pygame.transform.scale(image, size)
    return image
