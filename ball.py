import pygame
import random
from settings import (
    BALL_SIZE,
    MIDDLE,
    HEIGHT,
    BALL_SPEED,
    PADDLE_HEIGHT,
    MAX_BALL_SPEED_Y,
    MAX_BALL_SPEED_X,
    SPEED_INCREASE,
    WHITE_COLOR
)

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