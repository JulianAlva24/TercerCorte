import pygame
import random
import math
import sys
import os

# Inicializar pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Rutas de recursos
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
IMG_DIR = os.path.join(ASSETS_DIR, "images")
SND_DIR = os.path.join(ASSETS_DIR, "sounds")

# Cargar imágenes
PLAYER_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "player.png")), (40, 40)
)

ENEMY_IMGS = [
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "enemy1.png")), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "enemy2.png")), (50, 50)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "enemy3.png")), (60, 60)),
]
BULLET_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "bullet.png")), (8, 20)
)

BACKGROUND_IMG = pygame.image.load(os.path.join(IMG_DIR, "background.jpg"))

# Cargar sonidos
LASER_SOUND = pygame.mixer.Sound(os.path.join(SND_DIR, "laser.wav"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(SND_DIR, "explosion.wav"))

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Bullet:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Player:
    def __init__(self, x, y):
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullets = []
        self.last_shot = 0
        self.shoot_delay = 250

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot > self.shoot_delay:
                bullet = Bullet(self.rect.centerx, self.rect.top, -8, WHITE)
                self.bullets.append(bullet)
                LASER_SOUND.play()
                self.last_shot = current_time

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)
        # Barra de vida
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 60, 8))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, 60 * (self.health / self.max_health), 8))


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.image = ENEMY_IMGS[enemy_type - 1]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = enemy_type
        self.speed = 2 - (enemy_type * 0.3)
        self.health = 20 * enemy_type
        self.max_health = self.health

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # Barra de vida
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 5, self.rect.width, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 5, self.rect.width * (self.health / self.max_health), 5))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🚀 Space Shooter con Recursos")
        self.clock = pygame.time.Clock()
        self.player = Player(WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT - 60)
        self.enemies = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.background = BACKGROUND_IMG
        self.spawn_timer = 0

    def spawn_enemy(self):
        if len(self.enemies) < 5:
            enemy_type = random.randint(1, 3)
            x = random.randint(0, WINDOW_WIDTH - 50)
            y = random.randint(-60, -40)
            self.enemies.append(Enemy(x, y, enemy_type))

    def check_collisions(self):
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.health -= 10
                    self.player.bullets.remove(bullet)
                    if enemy.health <= 0:
                        EXPLOSION_SOUND.play()
                        self.enemies.remove(enemy)
                        self.score += 10
                    break
    # Colisión directa: enemigo toca al jugador
        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.player.rect):
                self.player.health -= 10
                self.enemies.remove(enemy)
                if self.player.health <= 0:
                    print("¡GAME OVER!")
                    pygame.quit()
                    sys.exit()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.spawn_timer += 1
            if self.spawn_timer >= 60:
                self.spawn_enemy()
                self.spawn_timer = 0

            for enemy in self.enemies[:]:
                enemy.update()
                if enemy.rect.top > WINDOW_HEIGHT:
                    self.enemies.remove(enemy)

            self.check_collisions()

            # Dibujar fondo
            self.screen.blit(self.background, (0, 0))
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Dibujar puntuación
            score_text = self.font.render(f"Puntaje: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()

