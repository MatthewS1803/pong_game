import pygame
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

# Font
font = pygame.font.Font('retro-font.ttf', 40)
win_font = pygame.font.Font('retro-font.ttf', 25)
state_font = pygame.font.Font('retro-font.ttf', 20)

MESSAGE_Y = TEXT_TOP + font.get_height() + MESSAGE_GAP + win_font.get_height() // 2
STACK_GAP = (win_font.get_height() // 2) + STACK_SPACING + (BUTTON_HEIGHT // 2)

# Drawing Text function
def draw_text(text, centerx, centery=None, top=TEXT_TOP, text_font=font, color=WHITE_COLOR):
    text_img = text_font.render(text, True, color)
    text_rect = text_img.get_rect()
    text_rect.centerx = centerx
    if centery is not None:
        text_rect.centery = centery
    else:
        text_rect.top = top
    screen.blit(text_img, text_rect)