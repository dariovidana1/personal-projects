from multis import *
from obstacles import *
from settings import *
import pygame, pymunk

games_played = 0

class Board:
    def __init__(self, space, initial_money=0):
        self.space = space
        self.display_surface = pygame.display.get_surface()

        # Obstáculos
        self.curr_row_count = 3
        self.final_row_count = 18
        self.obstacles_list = []
        self.obstacle_sprites = pygame.sprite.Group()
        self.updated_coords = OBSTACLE_START

        # Manejo de dinero
        self.total_money = initial_money
        self.withdrawable_money = 0.0  # Dinero que puede ser retirado
        self.current_bet = 0  # Jugada actual

        # Mensaje de error
        self.error_message = ""
        self.error_start_time = 0

        # Botones de monedas
        self.coin_values = [1, 2, 4, 6, 8, 10]
        self.selected_button = 0

        # Obtener el segundo punto para el segmento A
        self.segmentA_2 = OBSTACLE_START
        while self.curr_row_count <= self.final_row_count:
            for i in range(self.curr_row_count):
                if self.curr_row_count == 3 and self.updated_coords[0] > OBSTACLE_START[0] + OBSTACLE_PAD:
                    self.segmentB_1 = self.updated_coords
                elif self.curr_row_count == self.final_row_count and i == 0:
                    self.segmentA_1 = self.updated_coords
                elif self.curr_row_count == self.final_row_count and i == self.curr_row_count - 1:
                    self.segmentB_2 = self.updated_coords
                self.obstacles_list.append(self.spawn_obstacle(self.updated_coords, self.space))
                self.updated_coords = (int(self.updated_coords[0] + OBSTACLE_PAD), self.updated_coords[1])
            self.updated_coords = (int(WIDTH - self.updated_coords[0] + (.5 * OBSTACLE_PAD)), int(self.updated_coords[1] + OBSTACLE_PAD))
            self.curr_row_count += 1
        self.multi_x, self.multi_y = self.updated_coords[0] + OBSTACLE_PAD, self.updated_coords[1]

        # Segmentos alrededor de los obstáculos
        self.spawn_segments(self.segmentA_1, self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, self.segmentB_2, self.space)
        self.spawn_segments((self.segmentA_2[0], 0), self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, (self.segmentB_1[0], 0), self.space)

        # Generar multiplicadores
        self.blockers = []
        self.blocker_visuals = []  # Asegurarse de inicializar aquí
        self.spawn_multis()

        # Barreras para bloquear multiplicadores
        self.create_blockers()

        # Bandera para evitar múltiples actualizaciones de multiplicadores
        self.multipliers_updated = False

    def get_selected_coin_value(self):
        """Devuelve el valor del botón seleccionado actualmente."""
        return self.coin_values[self.selected_button]

    def update_money(self, money):
        self.total_money = money

    def update_withdrawable_money(self, amount):
        self.withdrawable_money += amount

    def draw_money(self):
        font = pygame.font.Font(None, 36) 
        money_surf = font.render(f"Total: ${int(self.total_money)}", True, (255, 255, 255))
        money_rect = money_surf.get_rect(midleft=(200, HEIGHT // 8))
        self.display_surface.blit(money_surf, money_rect)

        withdrawable_surf = font.render(f"Dinero retirable: ${int(self.withdrawable_money)}", True, (255, 255, 255))
        withdrawable_rect = withdrawable_surf.get_rect(midleft=(200, HEIGHT // 8 + 40))
        self.display_surface.blit(withdrawable_surf, withdrawable_rect)

    def draw_buttons(self):
        font = pygame.font.Font(None, 36)
        button_width, button_height = 100, 50
        button_spacing = 10
        button_x = 250
        button_y_start = (HEIGHT // 7) + 50

        for index, value in enumerate(self.coin_values):
            button_y = button_y_start + (button_height + button_spacing) * index
            color = (0, 255, 0) if index == self.selected_button else (255, 255, 255)
            pygame.draw.rect(self.display_surface, color, (button_x, button_y, button_width, button_height), border_radius=10)
            value_surf = font.render(f"{value} pesos", True, (0, 0, 0))
            value_rect = value_surf.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.display_surface.blit(value_surf, value_rect)

    def draw_error_message(self):
        """Dibuja el mensaje de error si está configurado y no ha expirado."""
        if self.error_message and (pygame.time.get_ticks() - self.error_start_time < 2000):
            font = pygame.font.Font(None, 36)
            error_surf = font.render(self.error_message, True, (255, 0, 0))
            error_rect = error_surf.get_rect(midtop=(350, (HEIGHT // 7) + 500))
            self.display_surface.blit(error_surf, error_rect)
        else:
            self.error_message = ""  # Limpiar mensaje si ha expirado

    def handle_button_navigation(self, key):
        if key == pygame.K_DOWN:
            self.selected_button = (self.selected_button + 1) % len(self.coin_values)
        elif key == pygame.K_UP:
            self.selected_button = (self.selected_button - 1) % len(self.coin_values)

    def handle_numeric_keys(self, key):
        """Maneja la selección de botones basada en las teclas numéricas presionadas."""
        key_to_index = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
            pygame.K_6: 5
        }
        if key in key_to_index:
            self.selected_button = key_to_index[key]
            self.drop_ball()  # Llama a la función para soltar la pelota

    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            pos_x, pos_y = int(obstacle.body.position.x), int(obstacle.body.position.y)
            pygame.draw.circle(self.display_surface, (255, 255, 255), (pos_x, pos_y), OBSTACLE_RAD)

    def draw_prev_multi_mask(self):
        multi_mask_surface = pygame.Surface((WIDTH / 4, HEIGHT), pygame.SRCALPHA)
        multi_mask_surface.fill(BG_COLOR)
        right_side_of_board = (WIDTH / 16) * 13
        right_side_pad = right_side_of_board / 130
        mask_y = (HEIGHT / 4) + ((HEIGHT / 4) / 9)
        pygame.draw.rect(multi_mask_surface, (0, 0, 0, 0), (right_side_pad, mask_y, SCORE_RECT, SCORE_RECT * 4), border_radius=30)
        self.display_surface.blit(multi_mask_surface, (right_side_of_board, 0))

    def spawn_multis(self):
        print(f"Spawning multipliers, games played: {games_played}")

        # Limpiar el grupo de multiplicadores antes de regenerarlos
        multi_group.empty()

        # Incluir todos los multiplicadores desde el principio
        allowed_multipliers = {val[1] for val in multi_rgb.keys()}

        # Filtrar las cantidades y colores basados en los multiplicadores permitidos
        filtered_multi_amounts = [val[1] for val in multi_rgb.keys() if val[1] in allowed_multipliers]
        filtered_rgb_vals = [multi_rgb[key] for key in multi_rgb.keys() if key[1] in allowed_multipliers]

        # ambas listas tengan la misma longitud
        assert len(filtered_multi_amounts) == len(filtered_rgb_vals), "Las listas de multiplicadores y colores no coinciden"

        # Generar los multiplicadores
        for i in range(len(filtered_multi_amounts)):
            print(f"Adding multiplier: {filtered_multi_amounts[i]}")
            multi = Multi((self.multi_x, self.multi_y), filtered_rgb_vals[i], filtered_multi_amounts[i])
            multi_group.add(multi)
            self.multi_x += OBSTACLE_PAD

        # Redibujar todos los elementos para actualizar la vista
        self.update_view()

    def create_blockers(self):
        """Crea barreras que impiden que las pelotas caigan en los multiplicadores x5 y x10."""
        if games_played < 30:
            #Coordenadas de las barreras
            left_blocker_start = (WIDTH * 0.27, HEIGHT * 0.75)
            left_blocker_end = (WIDTH * 0.33, HEIGHT * 0.96)

            right_blocker_start = (WIDTH * 0.73, HEIGHT * 0.75)
            right_blocker_end = (WIDTH * 0.67, HEIGHT * 0.96)

            up_blocker_left_start = (WIDTH * 0.39, HEIGHT * 0.35)
            up_blocker_left_end = (WIDTH * 0.407, HEIGHT * 0.40)

            up_blocker_right_start = (WIDTH * 0.61, HEIGHT * 0.35)
            up_blocker_right_end = (WIDTH * 0.593, HEIGHT * 0.40)

            #Crear barreras invisibles
            left_blocker = self.spawn_segments(left_blocker_start, left_blocker_end, self.space)
            right_blocker = self.spawn_segments(right_blocker_start, right_blocker_end, self.space)
            up_blocker_right = self.spawn_segments(up_blocker_right_start, up_blocker_right_end, self.space)
            up_blocker_left = self.spawn_segments(up_blocker_left_start, up_blocker_left_end, self.space)

            self.blockers.extend([left_blocker, right_blocker])
            self.blockers.extend([up_blocker_left, up_blocker_right])

            #Añadir visualización de las barreras
            self.blocker_visuals.append((left_blocker_start, left_blocker_end))
            self.blocker_visuals.append((right_blocker_start, right_blocker_end))
            self.blocker_visuals.append((up_blocker_right_start, up_blocker_right_end))
            self.blocker_visuals.append((up_blocker_left_start, up_blocker_left_end))

    def remove_blockers(self):
        """Elimina las barreras que bloquean los multiplicadores x5 y x10."""
        for blocker in self.blockers:
            self.space.remove(blocker)
        self.blockers.clear()
        self.blocker_visuals.clear()

    def draw_blockers(self):
        """Dibuja las barreras en la pantalla."""
        for start, end in self.blocker_visuals:
            pygame.draw.line(self.display_surface, (255, 0, 0), start, end, 0)   #rgba(16,32,45,255)

    def spawn_obstacle(self, pos, space):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        body.friction = 0.6
        shape = pymunk.Circle(body, OBSTACLE_RAD)
        shape.elasticity = 0.4
        shape.filter = pymunk.ShapeFilter(categories=OBSTACLE_CATEGORY, mask=OBSTACLE_MASK)
        self.space.add(body, shape)
        obstacle = Obstacle(body.position.x, body.position.y)
        self.obstacle_sprites.add(obstacle)
        return shape

    def spawn_segments(self, pointA, pointB, space):
        segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, pointA, pointB, 5)
        self.space.add(segment_body, segment_shape)
        return segment_shape

    def set_error_message(self, message):
        """Configura el mensaje de error y reinicia el temporizador."""
        self.error_message = message
        self.error_start_time = pygame.time.get_ticks()

    def update_view(self):
        """Actualiza y redibuja todos los elementos visibles en la pantalla."""
        self.display_surface.fill(BG_COLOR)
        self.draw_obstacles(self.obstacles_list)
        multi_group.draw(self.display_surface)
        multi_group.update()
        if len(list(prev_multi_group)) > 0:
            prev_multi_group.update()
        if len(list(animation_group)) > 0:
            animation_group.update()
        self.draw_prev_multi_mask()
        self.draw_money()
        self.draw_buttons()
        self.draw_error_message()
        self.draw_blockers()  # Dibujar las barreras
        pygame.display.flip()

    def update(self):
        """Actualiza los elementos del juego sin forzar una nueva renderización completa."""
        self.draw_obstacles(self.obstacles_list)
        multi_group.draw(self.display_surface)
        multi_group.update()
        if len(list(prev_multi_group)) > 0:
            prev_multi_group.update()
        if len(list(animation_group)) > 0:
            animation_group.update()
        self.draw_prev_multi_mask()
        self.draw_money()
        self.draw_buttons()
        self.draw_error_message()
        self.draw_blockers()  # Dibujar las barreras

        # Si el número de juegos es mayor o igual que 20 y aún no se han actualizado los multiplicadores
        if games_played >= 30 and not self.multipliers_updated:
            self.multi_x, self.multi_y = self.updated_coords[0] + OBSTACLE_PAD, self.updated_coords[1]  # Resetea multi positions
            self.spawn_multis()
            self.multipliers_updated = True
            self.remove_blockers()  # Eliminar las barreras
            self.update_view()  # Actualizar la vista para reflejar los cambios

    def drop_ball(self):
        """Lógica para soltar la pelota y manejar el contador de juegos."""
        coin_value = self.get_selected_coin_value()
        if self.total_money >= coin_value:
            global games_played
            games_played += 1
            print(f"Games played: {games_played}")
            self.update()
            self.game.drop_ball()  # Llama al método drop_ball de la instancia de Game
        else:
            self.set_error_message("Saldo insuficiente para jugar.")
