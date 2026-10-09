import pygame

class platform:
    def __init__(self, posx, posy, sizex, sizey, surf):
        self.surface = surf
        self.plat = pygame.Rect(posx, posy, sizex, sizey)

    def draw(self, color, offset_x, offset_y):
        self.draw_rect = self.plat.copy()
        self.draw_rect.x -= offset_x
        self.draw_rect.y -= offset_y
        pygame.draw.rect(self.surface, color, self.draw_rect)