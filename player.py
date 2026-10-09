import pygame

class player:
    def __init__(self, x, y, surface):
        self.player_health = 100 
        self.invincible = False
        self.inv_timer = 0
        self.color = (255, 255, 255)
        self.state = "IDLE"

        self.player_base = pygame.Rect(x, y, 30, 90)
        self.dx = 0    
        self.acsel = 0.6
        self.fric = 0.8
        self.max = 6
        self.surface = surface
        self.facing_right = True
        self.dirp = pygame.Rect(0, 0, 10, 10) 

        self.dy = 0           
        self.gravity = 1.5
        self.jump_power = 28
        self.on_ground = False 
        self.jump_released = True
        self.jump_timer = 0
        self.is_hesitating = False

        self.is_att = False
        self.att_tim = 0
        self.attack_cooldown = 0
        self.hb = None
        self.attack_released = True

    def move(self, win_w, win_h, tile, platforms, enemy, offset_x, offset_y):
        keyboard = pygame.key.get_pressed()
        
        # 1. ATTACK LOGIC
        if not keyboard[pygame.K_x]:
            self.attack_released = True

        if keyboard[pygame.K_x] and self.attack_released and not self.is_att and self.attack_cooldown == 0:
            self.is_att = True
            self.att_tim = 10 
            self.attack_cooldown = 20 
            self.attack_released = False 
            
            if self.facing_right:
                self.hb = pygame.Rect(self.player_base.right, self.player_base.centery - 25, 50, 50)
            else:
                self.hb = pygame.Rect(self.player_base.x - 50, self.player_base.centery - 25, 50, 50)

        if self.is_att:
            self.att_tim -= 1
            if self.att_tim <= 0:
                self.is_att = False
                self.hb = None 

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # 2. HORIZONTAL INPUT
        if keyboard[pygame.K_RIGHT]:
            self.dx += self.acsel 
            self.facing_right = True 
        elif keyboard[pygame.K_LEFT]:
            self.dx -= self.acsel
            self.facing_right = False
        else:
            if self.dx > 0:
                self.dx = max(0, self.dx - self.fric)
            elif self.dx < 0:
                self.dx = min(0, self.dx + self.fric)

        if self.dx > self.max: self.dx = self.max
        if self.dx < -self.max: self.dx = -self.max

        # 3. JUMP LOGIC
        if not keyboard[pygame.K_z]:
            self.jump_released = True

        if keyboard[pygame.K_z] and self.on_ground and not self.is_hesitating and self.jump_released:
            self.is_hesitating = True
            self.jump_timer = 1
            self.jump_released = False

        if self.is_hesitating:
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.dy = -self.jump_power
                self.is_hesitating = False
                self.on_ground = False

        if not self.is_hesitating and not keyboard[pygame.K_z] and self.dy < 0:
            self.dy *= 0.5  

        if not self.is_hesitating:
            self.dy += self.gravity

        # 4. X-AXIS COLLISION
        self.player_base.x += int(self.dx)
        
        for b in tile.rects:
            if self.player_base.colliderect(b):
                if self.dx > 0: 
                    self.player_base.right = b.left 
                    self.dx = 0
                elif self.dx < 0: 
                    self.player_base.left = b.right 
                    self.dx = 0

        for p in platforms:
            if self.player_base.colliderect(p.plat):
                if self.dx > 0: 
                    self.player_base.right = p.plat.left 
                    self.dx = 0
                elif self.dx < 0: 
                    self.player_base.left = p.plat.right 
                    self.dx = 0

        # 5. Y-AXIS COLLISION
        self.player_base.y += int(self.dy)
        self.on_ground = False 
        
        for b in tile.rects:
            if self.player_base.colliderect(b):
                if self.dy > 0: 
                    self.player_base.bottom = b.top 
                    self.dy = 0
                    self.on_ground = True
                    self.is_hesitating = False 
                    self.jump_timer = 0
                elif self.dy < 0: 
                    self.player_base.top = b.bottom 
                    self.dy = 0

        for p in platforms:
            if self.player_base.colliderect(p.plat):
                if self.dy > 0: 
                    self.player_base.bottom = p.plat.top 
                    self.dy = 0
                    self.on_ground = True
                    self.is_hesitating = False
                    self.jump_timer = 0
                elif self.dy < 0: 
                    self.player_base.top = p.plat.bottom 
                    self.dy = 0

        # 6. ENEMY COLLISION & INVINCIBILITY
        if self.player_base.colliderect(enemy.eb) and not self.invincible:
            self.player_health -= 10
            self.inv_timer = 30
            self.invincible = True
            self.color = (0, 255, 0)

        if self.invincible:
            self.inv_timer -= 1
            if self.inv_timer <= 0:
                self.invincible = False
                self.color = (255, 255, 255)

        # 7. STATE MACHINE
        if self.is_att:
            self.state = "ATTACK"
        elif not self.on_ground:
            if self.dy < 0:
                self.state = "JUMP"
            else:
                self.state = "FALL"
        else:
            if self.dx > 0.5 or self.dx < -0.5:
                self.state = "RUN"
            else:
                self.state = "IDLE"

        if self.facing_right:
            self.dirp = pygame.Rect(self.player_base.right, self.player_base.centery, 10, 10)
        else:
            self.dirp = pygame.Rect(self.player_base.x - 10, self.player_base.centery, 10, 10)


    def draw(self, offset_x, offset_y):
        self.draw_rect = self.player_base.copy()
        self.draw_rect.x -= offset_x
        self.draw_rect.y -= offset_y
        pygame.draw.rect(self.surface, self.color, self.draw_rect)
        
        if self.is_att and self.hb: 
            draw_hb = self.hb.copy()
            draw_hb.x -= offset_x
            draw_hb.y -= offset_y
            pygame.draw.rect(self.surface, (0, 0, 255), draw_hb)

        draw_dirp = self.dirp.copy()
        draw_dirp.x -= offset_x
        draw_dirp.y -= offset_y
        pygame.draw.rect(self.surface, (0, 100, 100), draw_dirp)