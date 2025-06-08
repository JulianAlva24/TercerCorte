#!/usr/bin/env python3
import pygame
import sys
import random

# Inicialización
pygame.init()
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40  # Tamaño de cada casilla de la cuadrícula
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanques en Laberinto Simplificado")
clock = pygame.time.Clock()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

# Mapa: '1' muro, '0' espacio libre
MAP_LAYOUT = [
    "11111111111111111111",
    "10000000001000000001",
    "10111111101011111001",
    "10000000100000001001",
    "11101110101110101111",
    "10001000100010001001",
    "10111011101110111001",
    "10000000000000000001",
    "11101110111011101111",
    "10000000100000001001",
    "10111110101111111001",
    "10000000000000000001",
    "11111111111100111111"
]

class Wall:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)

class Tank:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.size = TILE_SIZE - 8
        self.angle = 0
        self.speed = 3
        self.health = 100
        self.controls = controls  # [left, right, up, down, shoot]
        self.bullets = []
        self.cooldown = 0

    def draw(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.size, self.size))
        pygame.draw.rect(surf, BLACK, (self.size//2 - 4, -8, 8, 12))  # Cañón
        rot = pygame.transform.rotate(surf, self.angle)
        rect = rot.get_rect(center=(self.x, self.y))
        screen.blit(rot, rect.topleft)
        pygame.draw.rect(screen, RED, (self.x - self.size//2, self.y - self.size, self.size, 5))
        pygame.draw.rect(screen, GREEN, (self.x - self.size//2, self.y - self.size, self.size * (self.health/100), 5))

    def move(self, walls):
        keys = pygame.key.get_pressed()
        if keys[self.controls[0]]: self.angle += 4
        if keys[self.controls[1]]: self.angle -= 4
        dx = dy = 0
        if keys[self.controls[2]]:
            vec = pygame.math.Vector2(1, 0).rotate(-self.angle) * self.speed
            dx, dy = vec.x, vec.y
        if keys[self.controls[3]]:
            vec = pygame.math.Vector2(1, 0).rotate(-self.angle) * -self.speed
            dx, dy = vec.x, vec.y
        new_x, new_y = self.x + dx, self.y + dy
        tank_rect = pygame.Rect(new_x - self.size/2, new_y - self.size/2, self.size, self.size)
        for wall in walls:
            if tank_rect.colliderect(wall.rect):
                return
        self.x, self.y = new_x, new_y

    def shoot(self):
        if self.cooldown <= 0:
            dir_vec = pygame.math.Vector2(1, 0).rotate(-self.angle)
            sx = self.x + dir_vec.x * (self.size//2 + 5)
            sy = self.y + dir_vec.y * (self.size//2 + 5)
            speed = 7
            self.bullets.append([sx, sy, dir_vec.x * speed, dir_vec.y * speed])
            self.cooldown = 20

    def update_bullets(self, walls, other):
        for b in self.bullets[:]:
            b[0] += b[2]; b[1] += b[3]
            pt = (int(b[0]), int(b[1]))
            for wall in walls:
                if wall.rect.collidepoint(pt):
                    self.bullets.remove(b)
                    break
            else:
                if pygame.Rect(other.x - self.size/2, other.y - self.size/2, self.size, self.size).collidepoint(pt):
                    other.health -= 20
                    self.bullets.remove(b)
                    continue
                pygame.draw.circle(screen, WHITE, pt, 4)
        if self.cooldown > 0:
            self.cooldown -= 1

# Crear muros a partir del mapa
walls = []
for row_idx, row in enumerate(MAP_LAYOUT):
    for col_idx, char in enumerate(row):
        if char == '1':
            walls.append(Wall(col_idx * TILE_SIZE, row_idx * TILE_SIZE))

# Posiciones iniciales de tanques
tank1 = Tank(TILE_SIZE + TILE_SIZE//2, TILE_SIZE + TILE_SIZE//2, BLUE,
             [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE])

tank2 = Tank(WIDTH - 2*TILE_SIZE + TILE_SIZE//2, HEIGHT - 2*TILE_SIZE + TILE_SIZE//2, RED,
             [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN])

# Bucle principal
game_over = False
winner = None
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN and game_over and e.key == pygame.K_r:
            tank1.health = 100; tank2.health = 100
            tank1.x, tank1.y = TILE_SIZE + TILE_SIZE//2, TILE_SIZE + TILE_SIZE//2
            tank2.x, tank2.y = WIDTH - 2*TILE_SIZE + TILE_SIZE//2, HEIGHT - 2*TILE_SIZE + TILE_SIZE//2
            tank1.bullets.clear(); tank2.bullets.clear()
            game_over = False

    screen.fill(BLACK)
    # Movimiento y disparo
    if not game_over:
        tank1.move(walls)
        tank2.move(walls)
        keys = pygame.key.get_pressed()
        if keys[tank1.controls[4]]: tank1.shoot()
        if keys[tank2.controls[4]]: tank2.shoot()

    # Actualizar balas
    tank1.update_bullets(walls, tank2)
    tank2.update_bullets(walls, tank1)

    # Comprobar fin del juego
    if not game_over:
        if tank1.health <= 0:
            game_over = True; winner = "Jugador 2"
        elif tank2.health <= 0:
            game_over = True; winner = "Jugador 1"

    # Dibujar muros y tanques
    for w in walls:
        w.draw(screen)
    tank1.draw()
    tank2.draw()

    # Mostrar fin
    if game_over:
        font = pygame.font.SysFont(None, 64)
        text = font.render(f"¡{winner} gana!", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 32))
        hint = pygame.font.SysFont(None, 24).render("Presiona R para reiniciar", True, WHITE)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 32))

    pygame.display.flip()
    clock.tick(60)


