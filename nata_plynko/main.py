from ball import Ball
from board import *
from multis import *
from settings import *
import ctypes, pygame, pymunk, random, sys, time

# Mantener la resolución independientemente de la configuración de escalado de Windows
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Configuración general de pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Configuración de pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 1800)

        # Configuración de Plinko
        self.ball_group = pygame.sprite.Group()
        self.board = Board(self.space)
        self.board.game = self  # Pasar la referencia del juego al tablero

        # Depuración y dinero
        self.balls_played = 0
        self.total_money = 0.0  # Total de dinero acumulado
        self.money = 0  # Dinero ingresado en una transacción

        # Cargar la imagen/logo
        self.image = pygame.image.load("graphics/logo.png")
        self.image_rect = self.image.get_rect(center=(WIDTH // 2, 300))

    def show_menu(self):
        running = True
        font = pygame.font.Font(None, 36)

        # Dimensiones del botón
        button_width = 100
        button_height = 50
        button_spacing = 20
        button_radius = 15

        # Botones de monedas
        coin_values = ['1 peso', '2 pesos', '5 pesos', '10 pesos']
        total_buttons_width = (button_width * len(coin_values)) + (button_spacing * (len(coin_values) - 1))
        button_x_start = (WIDTH - total_buttons_width) // 2 - button_width - button_spacing

        # Crear un diccionario de botones para las monedas
        coin_buttons = {index: pygame.Rect(button_x_start + (button_width + button_spacing) * index,
                                          (HEIGHT - button_height) // 2,
                                          button_width,
                                          button_height) for index, value in enumerate(coin_values)}

        # Agregar botón de START
        start_button = pygame.Rect(button_x_start + total_buttons_width + button_spacing * 2,
                                   (HEIGHT - button_height) // 2,
                                   button_width,
                                   button_height)
        selected_index = 0
        max_index = len(coin_values)
        error_message = ""  # Mensaje para indicar error si el total es 0
        error_start_time = 0  # Tiempo de inicio para el mensaje de error

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % (max_index + 1)
                    elif event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % (max_index + 1)
                    elif event.key == pygame.K_SPACE:
                        if selected_index == max_index:
                            if self.total_money == 0:
                                error_message = "Debes ingresar dinero para jugar."
                                error_start_time = time.time()  # Establecer tiempo de inicio
                            else:
                                running = False
                                error_message = ""
                        else:
                            self.total_money += int(coin_values[selected_index].split()[0])

            self.screen.fill(BG_COLOR)
            self.screen.blit(self.image, self.image_rect)

            # Dibujar botones de monedas y START
            for index, button_rect in coin_buttons.items():
                button_color = self.GREEN if index == selected_index else self.WHITE
                pygame.draw.rect(self.screen, button_color, button_rect, border_radius=button_radius)
                label = font.render(coin_values[index], True, self.BLACK)
                label_rect = label.get_rect(center=button_rect.center)
                self.screen.blit(label, label_rect)

            start_button_color = self.GREEN if selected_index == max_index else self.WHITE
            pygame.draw.rect(self.screen, start_button_color, start_button, border_radius=button_radius)
            start_label = font.render("START", True, self.BLACK)
            start_label_rect = start_label.get_rect(center=start_button.center)
            self.screen.blit(start_label, start_label_rect)

              # Mostrar total de dinero
            total_money_label = font.render(f"Total: ${int(self.total_money)}", True, self.WHITE)
            self.screen.blit(total_money_label, ((WIDTH - total_buttons_width) // 2, (HEIGHT + button_height) // 2 + 10))

            money_label = font.render(f"Dinero ingresado: ${self.money}", True, self.WHITE)
            self.screen.blit(money_label, ((WIDTH - total_buttons_width) // 2, (HEIGHT + button_height) // 2 + 40))

            # Mostrar mensaje de error si es necesario
            if error_message and (time.time() - error_start_time < 3):
                error_surf = font.render(error_message, True, self.RED)
                error_rect = error_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
                self.screen.blit(error_surf, error_rect)

            pygame.display.flip()

        # Pasar el total de dinero al tablero
        self.board.update_money(self.total_money)

    def drop_ball(self):
        coin_value = self.board.get_selected_coin_value()
        if self.total_money >= coin_value:
            self.total_money -= coin_value
            self.board.current_bet = coin_value  # Guardar la jugada actual en el tablero
            self.board.update_money(self.total_money)  # Actualizar el tablero con el nuevo saldo
            random_x = WIDTH // 2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
            self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
            self.ball_group.add(self.ball)
        else:
            # Establecer el mensaje de error en el tablero
            self.board.set_error_message("Saldo insuficiente para jugar.")

    def handle_ball_landed(self, multiplier_value):
        bet_amount = self.board.current_bet  # Usar la jugada actual almacenada en el tablero
        winnings = bet_amount * multiplier_value
        winnings = round(winnings, 1)  # Asegurarse de que las ganancias se manejen con un decimal internamente
        self.board.update_withdrawable_money(winnings)

    def run(self):
        self.show_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                        self.board.handle_numeric_keys(event.key)

            self.screen.fill(BG_COLOR)

            self.delta_time = self.clock.tick(FPS) / 1000.0

            self.space.step(self.delta_time)
            self.board.update()
            self.ball_group.update()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
