# --- IMPORTS ---
import pygame
import random

from settings import (
    WIDTH,
    HEIGHT,
    MIDDLE,
    STEP,
    LEFT_HALF_X,
    RIGHT_HALF_X,
    AI_SETTINGS,
    BLACK_COLOR,
    WHITE_COLOR,
    DASH_STEP,
    DASH_LENGTH,
    BUTTON_HEIGHT,
    STACK_SPACING,
    PADDLE_WIDTH
)
from display import screen, MESSAGE_Y, STACK_GAP,draw_text
from paddle import Paddle
from button import Button
from scoreboard import Scoreboard
from ball import Ball

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

        # Draws start and quit button
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
            # Draws the restart and main menu button
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