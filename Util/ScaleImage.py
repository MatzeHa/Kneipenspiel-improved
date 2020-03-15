
def scale_image(img, _new_width):
    import pygame
    img_width = img.get_width()
    img_height = img.get_height()
    new_width = _new_width
    new_heigth = int(img_height * (new_width / img_width))
    img_scaled = pygame.transform.scale(img, (new_width, new_heigth))
    return img_scaled, new_heigth