from settings import *
import pygame

# Sprite para los multiplicadores debajo de los obstáculos:
multi_group = pygame.sprite.Group()
clock = pygame.time.Clock()
delta_time = clock.tick(FPS) / 1000.0

class Multi(pygame.sprite.Sprite):
    def __init__(self, position, color, multi_amt):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 26)
        self.color = color
        self.border_radius = 10
        self.position = position
        self.rect_width, self.rect_height = OBSTACLE_PAD - (OBSTACLE_PAD / 14), MULTI_HEIGHT
        self.image = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, self.image.get_rect(), border_radius=self.border_radius)
        self.rect = self.image.get_rect(center=position)
        self.multi_amt = multi_amt
        self.prev_multi = int(WIDTH / 21.3)

        # Cosas de animación
        self.animated_frames = 0
        self.animation_frames = int(0.25 / delta_time)
        self.is_animating = False

        # Dibujar la cantidad del multiplicador en el rectángulo
        self.render_multi()

    def animate(self, color, amount):
        if self.animated_frames < self.animation_frames // 2:
            self.rect.bottom += 2
        else:
            self.rect.bottom -= 2
        self.animated_frames += 1
        if self.animated_frames == (self.animation_frames // 2) * 2:
            self.is_animating = False
            self.animated_frames = 0

    def render_multi(self):
        text_surface = self.font.render(f"{self.multi_amt}x", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

    def hit_sound(self):
        if str(self.multi_amt) == "0.0":
            sound01.play()
        elif str(self.multi_amt) == "0.4":
            sound02.play()
        elif str(self.multi_amt) == "0.5":
            sound03.play()
        elif str(self.multi_amt) == "1":
            sound04.play()
        elif str(self.multi_amt) == "2":
            sound05.play()
        elif str(self.multi_amt) == "5":
            sound06.play()
        elif str(self.multi_amt) == "10":
            sound07.play()

    def update(self):
        if self.is_animating:
            self.animate(self.color, self.multi_amt)

# Clase para la visualización del multiplicador anterior en el lado derecho de la pantalla
class PrevMulti(pygame.sprite.Sprite):
    def __init__(self, multi_amt, rgb_tuple):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Cosas del rectángulo
        self.multi_amt = multi_amt
        self.font = pygame.font.SysFont(None, 36)
        self.rect_width = SCORE_RECT
        self.rect_height = SCORE_RECT
        self.prev_surf = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.rgb = rgb_tuple
        pygame.draw.rect(self.prev_surf, self.rgb, (0, 0, self.rect_width, self.rect_height))
        self.prev_rect = self.prev_surf.get_rect(midbottom=(int(WIDTH * .85), (HEIGHT / 2) - (SCORE_RECT * 2)))

        # Animación
        self.y_traverse = 0
        self.traveled = 0

        self.render_multi()

    def render_multi(self):
        text_surface = self.font.render(f"{self.multi_amt}x", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.prev_surf.get_rect().center)
        self.prev_surf.blit(text_surface, text_rect)

    def update(self):
        if self.prev_rect.bottom > (HEIGHT - (SCORE_RECT * 2)): 
            self.kill()

        else:
            if self.traveled < self.y_traverse:
                total_distance = SCORE_RECT
                distance_per_second = 1800
                distance_per_frame = distance_per_second * delta_time 
                divisor = int(SCORE_RECT / distance_per_frame)
                distance_per_frame = SCORE_RECT / divisor
                self.prev_rect.bottom += int(distance_per_frame)
                self.traveled += int(distance_per_frame)
            self.display_surface.blit(self.prev_surf, self.prev_rect)

class PrevMultiGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        pass

    def update(self):
        super().update()

        # Mantener un máximo de cuatro multiplicadores anteriores; animar
        if len(self) > 5:
            self.remove(self.sprites().pop(0))        
        if len(self) == 1:
            self.sprites()[0].y_traverse = SCORE_RECT
        elif len(self) == 2:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse = SCORE_RECT * 2, SCORE_RECT
        elif len(self) == 3:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse, self.sprites()[2].y_traverse = SCORE_RECT * 3, SCORE_RECT * 2, SCORE_RECT
        elif len(self) == 4:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse, self.sprites()[2].y_traverse, self.sprites()[3].y_traverse = SCORE_RECT * 4, SCORE_RECT * 3, SCORE_RECT * 2, SCORE_RECT
        elif len(self) == 5:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse, self.sprites()[2].y_traverse, self.sprites()[3].y_traverse, self.sprites()[4].y_traverse = SCORE_RECT * 5, SCORE_RECT * 4, SCORE_RECT * 3, SCORE_RECT * 2, SCORE_RECT

prev_multi_group = PrevMultiGroup()