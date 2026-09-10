import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

# Player Car Class
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Enemy Car Class
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(3, 8)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Game variables
player = PlayerCar()
enemies = [EnemyCar() for _ in range(3)]
score = 0
font = pygame.font.Font(None, 36)
game_over = False

# Main Game Loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                # Reset game
                game_over = False
                score = 0
                player = PlayerCar()
                enemies = [EnemyCar() for _ in range(3)]

    if not game_over:
        # Update player
        player.update()

        # Update enemies
        for enemy in enemies:
            enemy.update()

        # Collision detection
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                game_over = True

        # Increase score
        score += 1

        # Draw everything
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score // 10}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Game Over screen
        game_over_text = font.render("GAME OVER!", True, RED)
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        final_score_text = font.render(f"Final Score: {score // 10}", True, YELLOW)
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 20))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80))

    pygame.display.flip()

pygame.quit()
sys.exit()
