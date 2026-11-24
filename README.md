# Python Pong
 
A classic Pong game built in Python with **pygame**. Play against a friend in 2-player mode, or take on an AI opponent in 1-player mode with three difficulty levels. The game includes a full menu system, pause screen, and win/restart flow.
 
## Gameplay Preview
 
![Gameplay screenshot](screenshots/gameplay.png)
 
<!-- Add a screenshot or GIF at screenshots/gameplay.png (a GIF of a rally works best). -->
 
## Features
 
- **1-player and 2-player modes** with a mode-select screen
- **Three AI difficulty levels** (Easy, Medium, Hard). Each level has its own paddle speed and aiming error, so the AI plays differently instead of just moving faster
- **Angled returns:** where the ball hits the paddle controls its bounce angle, so players can aim
- **Rally speed-up:** the ball gets faster with each paddle hit (up to a cap), then resets to its base speed after each point
- **Random serves** with varied starting positions and angles
- **First to 11 wins**, with a winner message shown on the winning side and RESTART / MAIN MENU buttons
- **Pause menu** (Resume, Main Menu, Quit) over a dimmed copy of the frozen court
- **Mouse-driven menus** with hover effects on buttons
- **Retro pixel font** and a dashed center line
- **Modular code:** split into separate modules for settings, display, and each game object
## Prerequisites & Installation
 
**Requirements**
 
- Python 3.10 or newer
- pygame
**Setup**
 
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt
```
 
`requirements.txt` contains:
 
```
pygame
```
 
## How to Run
 
From the project folder (the font file must be in the same folder):
 
```bash
python main.py
```
 
## Controls
 
| Action        | Player 1 (Left) | Player 2 (Right) |
|---------------|-----------------|------------------|
| Move Up       | W               | Up Arrow         |
| Move Down     | S               | Down Arrow       |
| Pause / Resume| Esc             | Esc              |
 
In 1-player mode, the right paddle is controlled by the AI. All menus are navigated with the mouse.
 
## Game Rules
 
- The ball bounces off the top and bottom walls and off each paddle.
- A point is scored when the ball passes the opponent's paddle and leaves the screen.
- The first player to reach **11 points** wins.
- After each point, the ball resets near the center with a random direction and returns to its starting speed.
## Project Structure
 
```
main.py         # Game loop, game states, and screen flow
settings.py     # Constants (sizes, speeds, colors, AI settings)
display.py      # Window, fonts, and text drawing
paddle.py       # Paddle class (keyboard movement and AI following)
ball.py         # Ball class (movement, bounces, angles, speed-up)
scoreboard.py   # Scoreboard class (scores, winner, drawing)
button.py       # Button class (drawing, hover effect, click detection)
retro-font.ttf  # Pixel font
```
 
## What I Learned
 
- Building a game loop with pygame: events, update, and drawing each frame
- Using `Rect` objects for positioning, collision detection, and clamping
- Organizing a project with classes and separate modules
- Modeling screens (menu, playing, paused, game over) with a state variable
- Designing a simple AI whose difficulty comes from speed and aim error
## Credits
 
Font: "Super Legend Boy" by GameDevDan (Chequered Ink Ltd., 2019), via FontStruct (https://fontstruct.com). Used under the Chequered Ink Font License.
