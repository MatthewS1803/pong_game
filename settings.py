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
PADDLE_SPEED = 7

# AI Constants
AI_SETTINGS = {
    'easy': {'speed': 3, 'error': 40},
    'medium': {'speed': 5, 'error': 25},
    'hard': {'speed': PADDLE_SPEED, 'error': 10}
}

# Button Constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_BORDER = 5

# Ball constants 
BALL_SIZE = 10 
BALL_SPEED = 4
MAX_BALL_SPEED_Y = 6
MAX_BALL_SPEED_X = 15 # Staying under the 25-pixel limit (paddle width + ball width)
SPEED_INCREASE = 1

# COLORS
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Winning Score 
WINNING_SCORE = 11

# Centering
MIDDLE = WIDTH // 2
LEFT_HALF_X = WIDTH // 4
RIGHT_HALF_X = MIDDLE + (WIDTH // 4)
MESSAGE_GAP = 10
STACK_SPACING = 20
STEP = BUTTON_HEIGHT + STACK_SPACING