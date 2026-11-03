# --- IMPORTS ---
import pygame
import random

# --- SETUP --- 
pygame.init()
clock = pygame.time.Clock()

# Font
font = pygame.font.Font('retro-font.ttf', 40)
win_font = pygame.font.Font('retro-font.ttf', 25)
state_font = pygame.font.Font('retro-font.ttf', 20)

# CONSTANTS 
HEIGHT = 600
WIDTH = 800
TEXT_TOP = HEIGHT // 30

# Center-line constants
DASH_LENGTH = 15
DASH_STEP = 30

# Paddle Constants
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 15
PADDLE_SPEED = 5

# Button Constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_BORDER = 3

# Ball constants 
BALL_SIZE = 10 
BALL_SPEED = 4
MAX_BALL_SPEED_Y = 6
MAX_BALL_SPEED_X = 15 # Staying under the 25-pixel limit (paddle width + ball width)
SPEED_INCREASE = 1

# Color constant
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Winning Score 
WINNING_SCORE = 2

# Centers for both side
LEFT_HALF_X = WIDTH // 4
RIGHT_HALF_X = WIDTH // 2 + (WIDTH // 4)
MESSAGE_GAP = 10
STACK_SPACING = 20
MESSAGE_Y = TEXT_TOP + font.get_height() + MESSAGE_GAP + win_font.get_height() // 2
STACK_GAP = (win_font.get_height() // 2) + STACK_SPACING + (BUTTON_HEIGHT // 2)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

# Game States
start_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
start_button.centerx = WIDTH // 2
start_button.centery = HEIGHT // 2
game_state = 'menu'

restart_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
restart_button.centerx = WIDTH // 2
restart_button.centery = MESSAGE_Y + STACK_GAP

menu_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
menu_button.centerx = WIDTH // 2
menu_button.centery = restart_button.centery + BUTTON_HEIGHT + STACK_SPACING

def reset_game():
    scoreboard.reset()
    left_paddle.reset()
    right_paddle.reset()
    ball.reset()

# Drawing Text function
def draw_text(text, centerx, centery=None, top=TEXT_TOP, text_font=font):
    text_img = text_font.render(text, True, WHITE_COLOR)
    text_rect = text_img.get_rect()
    text_rect.centerx = centerx
    if centery is not None:
        text_rect.centery = centery
    else:
        text_rect.top = top
    screen.blit(text_img, text_rect)

# Paddle Class
class Paddle:
    def __init__(self, x, up, down):
        self.rect = pygame.Rect(x, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.up = up
        self.down = down
        self.reset()

    def reset(self):
        self.rect.centery = HEIGHT // 2

    def move(self, keys):
        if keys[self.up]:
            self.rect.y -= PADDLE_SPEED

        if keys[self.down]:
            self.rect.y += PADDLE_SPEED

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE_COLOR, self.rect)

# Ball: position, speed, and bounces
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

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE_COLOR, self.rect)

class Scoreboard:
    def __init__(self):
        self.reset()

    def reset(self):
        self.left_score = 0
        self.right_score = 0
        self.game_over = False

    def point_for(self, side):
        if side == 'left':
            self.left_score += 1
        elif side == 'right':
            self.right_score += 1

        if self.left_score >= WINNING_SCORE or self.right_score >= WINNING_SCORE:
            self.game_over = True

    def winner(self):
        if not self.game_over:
            return None
        else:
            if self.left_score > self.right_score:
                return 'left'
            else:
                return 'right'

    def draw(self):
        draw_text(str(self.left_score), LEFT_HALF_X)
        draw_text(str(self.right_score), RIGHT_HALF_X)
        side = self.winner()
        if side is not None:
            message = f"{side.capitalize()} player wins"
            message_x = LEFT_HALF_X if side == 'left' else RIGHT_HALF_X
            draw_text(message, message_x, centery=MESSAGE_Y, text_font=win_font)
    
left_paddle = Paddle(20, pygame.K_w, pygame.K_s)
right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, pygame.K_UP, pygame.K_DOWN)
ball = Ball()
scoreboard = Scoreboard()

# --- GAME LOOP ---
running = True
while running:
    clock.tick(60)
    # --- Event Handling ---
    for event in pygame.event.get():
        # Checks if the user clicked the window's close (X) button
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'menu' and start_button.collidepoint(event.pos):
                game_state = 'playing'
            elif game_state == 'game_over':
                if restart_button.collidepoint(event.pos):
                    reset_game()
                    game_state = 'playing'
                elif menu_button.collidepoint(event.pos):
                    reset_game()
                    game_state = 'menu'
        
    
    # --- UPDATE ---
    keys = pygame.key.get_pressed()

    if game_state == 'playing':
        left_paddle.move(keys)
        right_paddle.move(keys)

        ball.move()
        ball.bounce_off_paddle(left_paddle.rect)
        ball.bounce_off_paddle(right_paddle.rect)

        if ball.rect.left < 0:
            scoreboard.point_for('right')
            ball.reset()

        if ball.rect.right > WIDTH:
            scoreboard.point_for('left')
            ball.reset()

        if scoreboard.game_over:
            game_state = 'game_over'
            winner_side = scoreboard.winner()
            if winner_side == 'left':
                restart_button.centerx = LEFT_HALF_X
                menu_button.centerx = LEFT_HALF_X
            else:
                restart_button.centerx = RIGHT_HALF_X
                menu_button.centerx = RIGHT_HALF_X

    # --- DRAWING ---
    screen.fill(BLACK_COLOR)
    
    if game_state == 'menu':
        # Draws the game title
        draw_text('PONG', WIDTH // 2)

        # Creates the start button 
        pygame.draw.rect(screen, BLACK_COLOR, start_button)
        pygame.draw.rect(screen, WHITE_COLOR, start_button, BUTTON_BORDER)
        
        # Draws the start button
        draw_text('START', start_button.centerx, centery=start_button.centery, text_font=state_font)
    else:
        # Draws the paddles 
        left_paddle.draw(screen)
        right_paddle.draw(screen)

        # Draws the ball
        ball.draw(screen)

        # Draws the scoreboard
        scoreboard.draw()

        # Dashed line in the center
        for y in range(0, HEIGHT, DASH_STEP):
            pygame.draw.line(screen, WHITE_COLOR, (WIDTH // 2, y), (WIDTH // 2, y + DASH_LENGTH), 2)

        if game_state == 'game_over':
            # Creates restart and main menu button
            pygame.draw.rect(screen, BLACK_COLOR, restart_button)
            pygame.draw.rect(screen, WHITE_COLOR, restart_button, BUTTON_BORDER)
            pygame.draw.rect(screen, BLACK_COLOR, menu_button)
            pygame.draw.rect(screen, WHITE_COLOR, menu_button, BUTTON_BORDER)

            # Draws the restart and main menu button
            draw_text('RESTART', restart_button.centerx, centery=restart_button.centery, text_font=state_font)
            draw_text('MAIN MENU', menu_button.centerx, centery=menu_button.centery, text_font=state_font)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()