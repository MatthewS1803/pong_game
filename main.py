# --- IMPORTS ---
import pygame

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
 
left_paddle = pygame.Rect(20, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
left_paddle.centery =  HEIGHT // 2


right_paddle = pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle.right = WIDTH - 20
right_paddle.centery = HEIGHT // 2

def paddle_moves(paddle, keys, up, down):
    if keys[up]:
        paddle.y -= PADDLE_SPEED
    if keys[down]:
        paddle.y += PADDLE_SPEED

    if paddle.y < 0:
        paddle.y = 0

    if paddle.bottom > HEIGHT:
        paddle.bottom = HEIGHT



# --- GAME LOOP ---
running = True

# Main game loop
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

    if keys[pygame.K_w]:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s]:
        left_paddle.y += PADDLE_SPEED

    if left_paddle.y < 0:
        left_paddle.y = 0

    if left_paddle.bottom > HEIGHT:
        left_paddle.bottom = HEIGHT

    if keys[pygame.K_UP]:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        right_paddle.y += PADDLE_SPEED

    if right_paddle.y < 0:
        right_paddle.y = 0

    if right_paddle.bottom > HEIGHT:
        right_paddle.bottom = HEIGHT

    

    # --- DRAWING ---
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()