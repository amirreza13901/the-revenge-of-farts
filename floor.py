import pygame

class floor:
    def __init__(self, level_w, win_h, surf):
        self.surf = surf
        self.tile_size = 100
        self.tile_num = level_w // self.tile_size
        self.rects = []
        for n in range(self.tile_num):
            x_pos = n * self.tile_size
            self.rects.append(pygame.Rect(x_pos, win_h - 80, self.tile_size, 100))

    def draw(self, offset_x, offset_y):
        for j in self.rects:
            draw_rect = j.copy()
            draw_rect.x -= offset_x
            draw_rect.y -= offset_y
            pygame.draw.rect(self.surf, (255, 255, 255), draw_rect)