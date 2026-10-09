import pygame

class enemy:
    def __init__(self, win, level_w, win_h):
        self.health = 200
        self.dy = 0
        self.gravity = 1.5
        self.dx = 0    
        self.acsel = 0.5
        self.fric = 0.8
        self.max = 5
        self.surf = win
        self.eb = pygame.Rect (level_w//2,win_h-175,100,100)
        self.level_w = level_w
        self.win_h = win_h
        self.on_ground = False
        self.is_hit = False
        self.tim = 0

        
        self.color = (100,0,0)
    def move(self, tile, player):
        self.eb.x +=self.dx
        if self.eb.left <=0:
            self.eb.left = 0
            self.dx *= -1

        if self.eb.right >=self.level_w:
            self.eb.right = self.level_w
            self.dx *= -1


        if self.eb.x > player.player_base.centerx:
            self.dx -= self.acsel 
        elif self.eb.x < player.player_base.centerx:
            self.dx += self.acsel
        else:
            if self.dx > 0:
                self.dx = max(0, self.dx - self.fric)
            elif self.dx < 0:
                self.dx = min(0, self.dx + self.fric)

        if self.dx > self.max: self.dx = self.max
        if self.dx < -self.max: self.dx = -self.max




        # Apply Gravity
        self.dy += self.gravity
        self.eb.y += int(self.dy)

        self.on_ground = False

        for b in tile.rects:
            if self.eb.colliderect(b):
                if self.dy > 0: # Falling
                    self.eb.bottom = b.top
                    self.dy = 0
                    self.on_ground = True
                elif self.dy < 0: # Jumping
                    self.eb.top = b.bottom
                    self.dy = 0
        if player.is_att:
            if self.eb.colliderect(player.hb) and not self.is_hit:
                self.health -= 10
                self.is_hit = True
                self.tim = 4

                if self.eb.x > player.player_base.centerx:
                    self.eb.x+=50
                if self.eb.x < player.player_base.centerx:
                    self.eb.x-=50
                self.eb.y-=10
            if self.is_hit and self.tim >0:
                self.color = (0,100,0)
                self.tim-=1
            if self.tim <= 0:
                self.is_hit = False
                self.color = (100,0,0)

    def draw(self, offset_x, offset_y):
        self.draw_rect = self.eb.copy()
        self.draw_rect.x -= offset_x
        self.draw_rect.y -= offset_y
        pygame.draw.rect(self.surf, self.color, self.draw_rect)
