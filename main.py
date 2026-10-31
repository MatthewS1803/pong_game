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

# Left Paddle 
left_paddle = pygame.Rect(20, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
left_paddle.centery =  HEIGHT // 2

# Right Paddle
right_paddle = pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle.right = WIDTH - 20
right_paddle.centery = HEIGHT // 2

# Ball 
BALL_SIZE = 10 
BALL_SPEED = 4
MAX_BALL_SPEED_Y = 6

# Scores
left_score, right_score = 0, 0

# Font
TEXT_COLOR = (255, 255, 255)
font = pygame.font.Font('retro-font.ttf', 40)

def paddle_moves(paddle, keys, up, down):
    if keys[up]:
        paddle.y -= PADDLE_SPEED
    if keys[down]:
        paddle.y += PADDLE_SPEED

    if paddle.y < 0:
        paddle.y = 0

    if paddle.bottom > HEIGHT:
        paddle.bottom = HEIGHT

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.reset()

    def reset(self):
        self.rect.centerx = WIDTH // 2 + random.randint(-20, 20)
        self.rect.centery = HEIGHT // 2 + random.randint(-150, 150)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = random.randint(0, BALL_SPEED) * random.choice([-1, 1])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

    def bounce_off_paddle(self, paddle):
        if self.rect.colliderect(paddle) and self.speed_x < 0:
            self.speed_x *= -1
            self.rect.left = paddle.right
            offset = self.rect.centery - paddle.centery
            normalized = offset / (PADDLE_HEIGHT // 2)
            final_speed = normalized * MAX_BALL_SPEED_Y
            self.speed_y = round(final_speed)

        if self.rect.colliderect(paddle) and self.speed_x > 0:
            self.speed_x *= -1
            self.rect.right = paddle.left
            offset = self.rect.centery - paddle.centery
            normalized = offset / (PADDLE_HEIGHT // 2)
            final_speed = normalized * MAX_BALL_SPEED_Y
            self.speed_y = round(final_speed)


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

    paddle_moves(left_paddle, keys, pygame.K_w, pygame.K_s)
    paddle_moves(right_paddle, keys, pygame.K_UP, pygame.K_DOWN)

    ball.move()
    ball.bounce_off_paddle(left_paddle)
    ball.bounce_off_paddle(right_paddle)
          

    if ball.rect.left < 0:
        right_score += 1
        ball.reset()

    if ball.rect.right > WIDTH:
        left_score += 1
        ball.reset()

    # --- DRAWING ---
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, TEXT_COLOR, left_paddle)
    pygame.draw.rect(screen, TEXT_COLOR, right_paddle)
    pygame.draw.rect(screen, TEXT_COLOR, ball)

    left_score_img = font.render(str(left_score), True, TEXT_COLOR)
    left_rect = left_score_img.get_rect()
    left_rect.centerx = 0 + (WIDTH // 2 - 0) // 2
    left_rect.top = 20
    screen.blit(left_score_img, left_rect)

    right_score_img = font.render(str(right_score), True, TEXT_COLOR)
    right_rect = right_score_img.get_rect()
    right_rect.centerx = WIDTH // 2 + (WIDTH - (WIDTH // 2)) // 2
    right_rect.top = 20
    screen.blit(right_score_img, right_rect)

    pong_img = font.render('PONG', True, TEXT_COLOR)
    pong_rect = pong_img.get_rect()
    pong_rect.top = 20
    pong_rect.centerx = WIDTH // 2
    screen.blit(pong_img, pong_rect)

    for y in range(0, HEIGHT, 30):
        pygame.draw.line(screen, TEXT_COLOR, (WIDTH // 2, y), (WIDTH // 2, y + DASH_LENGTH), 2)

    # pygame.draw.line(screen, TEXT_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()