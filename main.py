# --- IMPORTS ---
import pygame
import random

from settings import *
from display import (
    screen,
    font,
    win_font,
    state_font,
    MESSAGE_Y,
    STACK_GAP,
    draw_text
)

# --- SETUP --- 
clock = pygame.time.Clock()
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(150)
overlay.fill(BLACK_COLOR)

# Game States
game_state = 'menu'
running = True
game_mode = 'two_player'
difficulty = 'medium'


def reset_game():
    scoreboard.reset()
    left_paddle.reset()
    right_paddle.reset()
    ball.reset()

# Paddle Class
class Paddle:
    def __init__(self, x, up, down):
        self.rect = pygame.Rect(x, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.up = up
        self.down = down
        self.aim_offset = 0
        self.reset()

    def reset(self):
        self.rect.centery = HEIGHT // 2

    def move(self, keys):
        if keys[self.up]:
            self.rect.y -= PADDLE_SPEED

        if keys[self.down]:
            self.rect.y += PADDLE_SPEED

        self.clamp()

    def follow(self, ball_rect, speed):
        target = ball_rect.centery + self.aim_offset
        gap = target - self.rect.centery
        step = min(gap, speed)
        step = max(step, -speed)

        self.rect.y += step
        self.clamp()

    def clamp(self):
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
        self.rect.centerx = MIDDLE + random.randint(-20, 20)
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
            return True
        return False

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

class Button:
    def __init__(self, text, centerx, centery):
        self.rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.text = text
    
    def draw(self, screen):
        hovered = pygame.mouse.get_pos()
        if self.rect.collidepoint(hovered):
            border_color = (110, 110, 110)
            text_color = (20, 20, 20)
            fill_color = (200, 200, 200)
        else:
            text_color = WHITE_COLOR
            fill_color = BLACK_COLOR
            border_color = WHITE_COLOR

        pygame.draw.rect(screen, fill_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, BUTTON_BORDER)
        draw_text(self.text, self.rect.centerx, centery=self.rect.centery, text_font=state_font, color=text_color)


    def clicked(self, pos):
        return self.rect.collidepoint(pos)

left_paddle = Paddle(20, pygame.K_w, pygame.K_s)
right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, pygame.K_UP, pygame.K_DOWN)
ball = Ball()
scoreboard = Scoreboard()

# Buttons
start_button = Button('START', MIDDLE, HEIGHT // 2)
restart_button = Button('RESTART', MIDDLE, MESSAGE_Y + STACK_GAP)
menu_button = Button('MAIN MENU', MIDDLE, restart_button.rect.centery + BUTTON_HEIGHT + STACK_SPACING)
quit_button = Button('QUIT', MIDDLE, start_button.rect.centery + BUTTON_HEIGHT + STACK_SPACING)

# Pause Buttons
pause_menu_button = Button('MAIN MENU', MIDDLE, HEIGHT // 2)
resume_button = Button('RESUME', MIDDLE, pause_menu_button.rect.centery - STEP)
pause_quit_button = Button('QUIT', MIDDLE, pause_menu_button.rect.centery + STEP)

# Settings Button
# settings_button will do later

# Game mode buttons
one_player_button = Button('ONE PLAYER', MIDDLE, HEIGHT // 2)
two_player_button = Button('TWO PLAYER', MIDDLE, one_player_button.rect.centery + STEP)

# Difficulty buttons
medium_button = Button('MEDIUM', MIDDLE, HEIGHT // 2)
easy_button = Button('EASY', MIDDLE, medium_button.rect.centery - STEP)
hard_button = Button('HARD', MIDDLE, medium_button.rect.centery + STEP)

# --- GAME LOOP ---
while running:
    clock.tick(60)
    # --- Event Handling ---
    for event in pygame.event.get():
        # Checks if the user clicked the window's close (X) button
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state == 'playing':
                    game_state = 'paused'
                elif game_state == 'paused':
                    game_state = 'playing'

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'menu':
                if start_button.clicked(event.pos):
                    game_state = 'mode_select'
                elif quit_button.clicked(event.pos):
                    running = False
            elif game_state == 'game_over':
                if restart_button.clicked(event.pos):
                    reset_game()
                    game_state = 'playing'
                elif menu_button.clicked(event.pos):
                    reset_game()
                    game_state = 'menu'
            elif game_state == 'paused':
                if resume_button.clicked(event.pos):
                    game_state = 'playing'
                elif pause_quit_button.clicked(event.pos):
                    running = False
                elif pause_menu_button.clicked(event.pos):
                    reset_game()
                    game_state = 'menu'
            elif game_state == 'mode_select':
                if one_player_button.clicked(event.pos):
                    game_mode = 'one_player'
                    game_state = 'difficulty'
                elif two_player_button.clicked(event.pos):
                    game_mode = 'two_player'
                    game_state = 'playing'
            elif game_state == 'difficulty':
                if easy_button.clicked(event.pos):
                    difficulty = 'easy'
                    game_state = 'playing'
                elif medium_button.clicked(event.pos):
                    difficulty = 'medium'
                    game_state = 'playing'
                elif hard_button.clicked(event.pos):
                    difficulty = 'hard'
                    game_state = 'playing'
                
            
    
    # --- UPDATE ---
    keys = pygame.key.get_pressed()

    if game_state == 'playing':
        left_paddle.move(keys)

        if game_mode == 'two_player':
            right_paddle.move(keys)
        else:
            right_paddle.follow(ball.rect, AI_SETTINGS[difficulty]['speed'])

        ball.move()
        hit = ball.bounce_off_paddle(left_paddle.rect)
        ball.bounce_off_paddle(right_paddle.rect)

        if hit and game_mode == 'one_player':
            error = AI_SETTINGS[difficulty]['error']
            right_paddle.aim_offset = random.randint(-error, error)

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
                restart_button.rect.centerx = LEFT_HALF_X
                menu_button.rect.centerx = LEFT_HALF_X
            else:
                restart_button.rect.centerx = RIGHT_HALF_X
                menu_button.rect.centerx = RIGHT_HALF_X

    # --- DRAWING ---
    screen.fill(BLACK_COLOR)
    
    if game_state == 'menu':
        # Draws the game title
        draw_text('PONG', MIDDLE)

        # Creates the start button 
        start_button.draw(screen)
        quit_button.draw(screen)
    elif game_state == 'mode_select':
        draw_text('PONG', MIDDLE)
        draw_text('SELECT MODE', MIDDLE, centery=MESSAGE_Y)

        one_player_button.draw(screen)
        two_player_button.draw(screen)
    elif game_state == 'difficulty':
        draw_text('SELECT DIFFICULTY', MIDDLE, centery=MESSAGE_Y)
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
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
            pygame.draw.line(screen, WHITE_COLOR, (MIDDLE, y), (MIDDLE, y + DASH_LENGTH), 2)

        if game_state == 'game_over':
            # Creates restart and main menu button
            restart_button.draw(screen)
            menu_button.draw(screen)
        elif game_state == 'paused':
            screen.blit(overlay, (0, 0))
            pause_menu_button.draw(screen)
            resume_button.draw(screen)
            pause_quit_button.draw(screen)

    pygame.display.flip()
# --- CLEANUP ---
pygame.quit()