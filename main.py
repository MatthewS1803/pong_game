# --- IMPORTS ---
import pygame
import random

# --- SETUP --- 
pygame.init()
clock = pygame.time.Clock()

HEIGHT = 600
WIDTH = 800

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
ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)

# Scores
left_score, right_score = 0, 0


def paddle_moves(paddle, keys, up, down):
    if keys[up]:
        paddle.y -= PADDLE_SPEED
    if keys[down]:
        paddle.y += PADDLE_SPEED

    if paddle.y < 0:
        paddle.y = 0

    if paddle.bottom > HEIGHT:
        paddle.bottom = HEIGHT

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.centerx = WIDTH // 2 + random.randint(-20, 20)
    ball.centery = HEIGHT // 2 + random.randint(-150, 150)
    ball_speed_x = BALL_SPEED * random.choice([-1, 1])
    ball_speed_y = BALL_SPEED * random.choice([-1, 1])
    
reset_ball()

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

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top < 0 or ball.bottom > HEIGHT:
        ball_speed_y *= -1
        
    if ball.colliderect(left_paddle) and ball_speed_x < 0:
        ball_speed_x *= -1
        ball.left = left_paddle.right

    if ball.colliderect(right_paddle) and ball_speed_x > 0:
        ball_speed_x *= -1
        ball.right = right_paddle.left

    if ball.left < 0:
        right_score += 1
        print(left_score, right_score)
        reset_ball()

    if ball.right > WIDTH:
        left_score += 1
        print(left_score, right_score)
        reset_ball()

    # --- DRAWING ---
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)
    pygame.draw.rect(screen, (255, 255, 255), ball)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()