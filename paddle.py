import pygame
from settings import (
    PADDLE_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_SPEED,
    HEIGHT,
    WHITE_COLOR
)

class Paddle:
    def __init__(self, x, up, down):
        self.rect = pygame.Rect(x, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.up = up
        self.down = down
        self.reset()

    def reset(self):
        self.aim_offset = 0
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