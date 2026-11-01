# --- IMPORTS ---
import pygame
import random

# --- SETUP --- 
pygame.init()
clock = pygame.time.Clock()


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
WINNING_SCORE = 11

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

# Game States
game_state = 'start'

# Font
font = pygame.font.Font('retro-font.ttf', 40)
win_font = pygame.font.Font('retro-font.ttf', 30)

# Drawing Text function
def draw_text(text, centerx, top=TEXT_TOP, text_font=font):
    text_img = text_font.render(text, True, WHITE_COLOR)
    text_rect = text_img.get_rect()
    text_rect.centerx = centerx
    text_rect.top = top
    screen.blit(text_img, text_rect)

# Paddle Class
class Paddle:
    def __init__(self, x, up, down):
        self.rect = pygame.Rect(x, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.rect.centery = HEIGHT // 2
        self.up = up
        self.down = down

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
        draw_text(str(self.left_score), 0 + (WIDTH // 2 - 0) // 2)
        draw_text(str(self.right_score), WIDTH // 2 + (WIDTH - (WIDTH // 2)) // 2)
        side = self.winner()
        if side is not None:
            message = f"{side.capitalize()} player wins"
            draw_text(message, WIDTH // 2, top=HEIGHT // 2, text_font=win_font)

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

    
    # --- UPDATE ---
    keys = pygame.key.get_pressed()

    if not scoreboard.game_over:
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

    # --- DRAWING ---
    screen.fill(BLACK_COLOR)
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)

    # Scoreboard Text
    scoreboard.draw()
    
    # Pong Text
    draw_text('PONG', WIDTH // 2)

    # Dashed line in the center
    for y in range(0, HEIGHT, DASH_STEP):
        pygame.draw.line(screen, WHITE_COLOR, (WIDTH // 2, y), (WIDTH // 2, y + DASH_LENGTH), 2)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()