# --- IMPORTS ---
import pygame

# --- SETUP --- 
pygame.init()

HEIGHT = 600
WIDTH = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 15
 
left_paddle = pygame.Rect(20, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
left_paddle.centery =  HEIGHT // 2

PADDLE_SPEED = 5

# --- GAME LOOP ---
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        # Checks if the user clicked the window's close (X) button
        if event.type == pygame.QUIT:
            running = False

    
    # --- UPDATE ---
    # TODO: get the current key state with pygame.key.get_pressed()
    # TODO: if W is held, move left_paddle up
    # TODO: if S is held, move left_paddle down


    # --- DRAWING ---
    # Fill the screen with the color black
    screen.fill((0, 0, 0))
    # TODO: draw the paddle on the screen 
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    # TODO: push the drawn frame onto the display
    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()