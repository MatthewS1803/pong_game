# --- IMPORTS ---
import pygame
import random

# --- SETUP --- 
pygame.init()
clock = pygame.time.Clock()

HEIGHT = 600
WIDTH = 800
DASH_LENGTH = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 15
PADDLE_SPEED = 5

# Ball 
BALL_SIZE = 10 
BALL_SPEED = 4
MAX_BALL_SPEED_Y = 6
MAX_BALL_SPEED_X = 15 # Staying under the 25-pixel limit (paddle width + ball width)
SPEED_INCREASE = 1

# Scores
left_score, right_score = 0, 0

# Font
TEXT_COLOR = (255, 255, 255)
font = pygame.font.Font('retro-font.ttf', 40)

# Paddle Class
class Paddle:
    def __init__(self, x, up, down):
        self.rect = pygame.Rect(x, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.rect.centery = HEIGHT // 2
        self.up = up
        self.down = down

    def moves(self, keys):
        if keys[self.up]:
            self.rect.y -= PADDLE_SPEED

        if keys[self.down]:
            self.rect.y += PADDLE_SPEED

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

left_paddle = Paddle(20, pygame.K_w, pygame.K_s)
right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, pygame.K_UP, pygame.K_DOWN)

# The movements of the ball
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.reset()

    def reset(self):
        self.rect.centerx = WIDTH // 2 + random.randint(-20, 20)
        self.rect.centery = HEIGHT // 2 + random.randint(-150, 150)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = random.randint(0, BALL_SPEED) * random.choice([-1, 1])

    def moves(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

    def hit_angle(self, paddle):
        offset = self.rect.centery - paddle.centery
        normalized = offset / (PADDLE_HEIGHT // 2)
        final_speed = normalized * MAX_BALL_SPEED_Y
        return round(final_speed)

    def bounce_off_paddle(self, paddle):
        if self.rect.colliderect(paddle):
            if self.speed_x < 0:
                self.speed_x *= -1
                self.speed_x += SPEED_INCREASE
                self.speed_x = min(self.speed_x, MAX_BALL_SPEED_X)
                self.rect.left = paddle.right
            elif self.speed_x > 0:
                self.speed_x *= -1
                self.speed_x -= SPEED_INCREASE
                self.speed_x = max(self.speed_x, -MAX_BALL_SPEED_X)
                self.rect.right = paddle.left
            self.speed_y = self.hit_angle(paddle)

ball = Ball()

# --- GAME LOOP ---
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        # Checks if the user clicked the window's close (X) button
        if event.type == pygame.QUIT:
            running = False

    
    # --- UPDATE ---
    keys = pygame.key.get_pressed()

    left_paddle.moves(keys)
    right_paddle.moves(keys)

    ball.moves()
    ball.bounce_off_paddle(left_paddle.rect)
    ball.bounce_off_paddle(right_paddle.rect)
          

    if ball.rect.left < 0:
        right_score += 1
        ball.reset()

    if ball.rect.right > WIDTH:
        left_score += 1
        ball.reset()

    # --- DRAWING ---
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, TEXT_COLOR, left_paddle.rect)
    pygame.draw.rect(screen, TEXT_COLOR, right_paddle.rect)
    pygame.draw.rect(screen, TEXT_COLOR, ball.rect)

    # Left Score Text
    left_score_img = font.render(str(left_score), True, TEXT_COLOR)
    left_rect = left_score_img.get_rect()
    left_rect.centerx = 0 + (WIDTH // 2 - 0) // 2
    left_rect.top = 20
    screen.blit(left_score_img, left_rect)

    # Right Score Text
    right_score_img = font.render(str(right_score), True, TEXT_COLOR)
    right_rect = right_score_img.get_rect()
    right_rect.centerx = WIDTH // 2 + (WIDTH - (WIDTH // 2)) // 2
    right_rect.top = 20
    screen.blit(right_score_img, right_rect)

    # 'Pong' Text
    pong_img = font.render('PONG', True, TEXT_COLOR)
    pong_rect = pong_img.get_rect()
    pong_rect.top = 20
    pong_rect.centerx = WIDTH // 2
    screen.blit(pong_img, pong_rect)

    # Dashed line in the center
    for y in range(0, HEIGHT, 30):
        pygame.draw.line(screen, TEXT_COLOR, (WIDTH // 2, y), (WIDTH // 2, y + DASH_LENGTH), 2)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()