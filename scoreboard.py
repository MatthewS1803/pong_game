from settings import WINNING_SCORE, LEFT_HALF_X, RIGHT_HALF_X
from display import draw_text, MESSAGE_Y, win_font

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
