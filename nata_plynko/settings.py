import ctypes, pygame, pymunk

TITLE_STRING = 'Nata Plinko'
FPS = 60

ctypes.windll.user32.SetProcessDPIAware()

WIDTH = 1600
HEIGHT = 900

# Plinko configuracion
BG_COLOR = (16, 32, 45)
MULTI_HEIGHT = int(HEIGHT / 19) # 56 en 1920x1080
MULTI_COLLISION = HEIGHT - (MULTI_HEIGHT * 2) # 968 en 1920x1080

SCORE_RECT = int(WIDTH / 16) # 120 en 1920x1080

OBSTACLE_COLOR = "White"
OBSTACLE_RAD = int(WIDTH / 240) # 8 en 1920x1080
OBSTACLE_PAD = int(HEIGHT / 19) # 56 en 1920x1080
OBSTACLE_START = (int((WIDTH / 2) - OBSTACLE_PAD), int((HEIGHT - (HEIGHT * .9)))) # (904, 108) en 1920x1080
segmentA_2 = OBSTACLE_START

BALL_RAD = 14


# Diccionario para llevar un registro de las puntuaciones
multipliers = {
    "10": 0,
    "5": 0,
    "2": 0,
    "1": 0,
    "0.5": 0,
    "0.4": 0,
    "0.0": 0
}

# Valores rgb para los multiplicadores
multi_rgb = {
    (0, 10): (255, 0, 0),
    (1, 5): (255, 30, 0),# a partir de este se desbloquea
    (2, 2): (255, 60, 0),
    (3, 1): (255, 90, 0),
    (4, 0.5): (255, 120, 0),
    (5, 0.5): (255, 150, 0),
    (6, 0.4): (255, 180, 0),
    (7, 0.0): (255, 210, 0), 
    (8, 0.0): (255, 240, 0),
    (9, 0.4): (255, 210, 0),
    (10, 0.5): (255, 180, 0),
    (11, 0.5): (255, 150, 0),
    (12, 0.5): (255, 120, 0),
    (13, 1): (255, 90, 0),
    (14, 2): (255, 60, 0),
    (15, 5): (255, 30, 0),# a partir de este se desbloquea
    (16, 10): (255, 0, 0),
}

# numero de multiplicadores
NUM_MULTIS = 17

# configuracioon Pymunk
BALL_CATEGORY = 1
OBSTACLE_CATEGORY = 2
BALL_MASK = pymunk.ShapeFilter.ALL_MASKS() ^ BALL_CATEGORY
OBSTACLE_MASK = pymunk.ShapeFilter.ALL_MASKS()

# Sonidos al chocar con multis
pygame.mixer.init()
click = pygame.mixer.Sound("audio/click.mp3")
sound01 = pygame.mixer.Sound("audio/001.mp3")
sound01.set_volume(0.2)
sound02 = pygame.mixer.Sound("audio/002.mp3")
sound02.set_volume(0.3)
sound03 = pygame.mixer.Sound("audio/003.mp3")
sound03.set_volume(0.4)
sound04 = pygame.mixer.Sound("audio/004.mp3")
sound04.set_volume(0.5)
sound05 = pygame.mixer.Sound("audio/005.mp3")
sound05.set_volume(0.6)
sound06 = pygame.mixer.Sound("audio/006.mp3")
sound06.set_volume(0.7)
sound07 = pygame.mixer.Sound("audio/007.mp3")
sound07.set_volume(0.8)