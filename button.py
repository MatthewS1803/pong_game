import pygame

from settings import (
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    WHITE_COLOR,
    BLACK_COLOR,
    BUTTON_BORDER
)

from display import state_font, draw_text

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