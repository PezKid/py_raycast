import pygame
import math

# Initialize pygame
pygame.init()
pygame.display.set_caption("Raycast")
SCREEN_DIM = SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
screen = pygame.display.set_mode(SCREEN_DIM)
clock = pygame.time.Clock()

# Set colors
PLAYER_COLOR = (255, 0, 0) # red
MAP_COLOR = (255, 255, 255) # white
BG_COLOR = (0, 0, 0) # black

# Set up map
map = [
    ['1','1','1','1','1','1','1','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','1','1','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','1','0','1'],
    ['1','0','0','0','0','1','0','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','1','1','1','1','1','1','1'],
]
map_width, map_height = len(map[0]), len(map)
mso = 1 # map square offset, adds negative space background outline around blocks

# Set up player class
class Player:
    def __init__(self, x, y, radius, move_speed, rotation, rotation_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.move_speed = move_speed
        self.rotation = rotation # rotation in radians [0,2pi)
        self.rotation_speed = rotation_speed

    def move_forward(self):
        dx = self.move_speed * math.cos(self.rotation)
        dy = self.move_speed * math.sin(self.rotation)
        self.x += dx
        self.y += dy

    def move_backward(self):
        dx = self.move_speed * math.cos(self.rotation)
        dy = self.move_speed * math.sin(self.rotation)
        self.x -= dx
        self.y -= dy

    def turn_left(self):
        self.rotation -= self.rotation_speed
        if self.rotation < 0:
            self.rotation = 2 * math.pi
        if self.rotation > 2 * math.pi:
            self.rotation = 0

    def turn_right(self):
        self.rotation += self.rotation_speed
        if self.rotation < 0:
            self.rotation = 2 * math.pi
        if self.rotation > 2 * math.pi:
            self.rotation = 0

    def draw(self, canvas, color):
        pygame.draw.circle(canvas, PLAYER_COLOR, (self.x, self.y), self.radius, self.radius)  # body
        dx = self.radius * 1.5 * math.cos(self.rotation)
        dy = self.radius * 1.5 * math.sin(self.rotation)
        pygame.draw.line(canvas, PLAYER_COLOR, (self.x, self.y), (self.x + dx, self.y + dy), 3)

# Draws map on screen from variable map where value == 1
def draw_map():
    # Calculate square positions to perfectly fit screen dims
    square_width = SCREEN_WIDTH // map_width
    square_height = SCREEN_HEIGHT // map_height

    # Loop through each value in map
    for h in range(map_height):
        for w in range(map_width):

            # If map position == 1, draw rect
            if map[h][w] == '1':
                start_x = w * square_height
                start_y = h * square_width

                pygame.draw.rect(screen, MAP_COLOR, (start_x+mso, start_y+mso, square_width-mso, square_height-mso))

# Initialize player
player = Player(200, 300, 5, 5, 0, 0.2)

# Pygame game loop
fps_limit = 24
playing = True
while playing:
    clock.tick(fps_limit)
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Handle input
    keys = pygame.key.get_pressed()  # checking pressed keys

    if keys[pygame.K_w]:
        player.move_forward()
    if keys[pygame.K_s]:
        player.move_backward()
    if keys[pygame.K_a]:
        player.turn_left()
    if keys[pygame.K_d]:
        player.turn_right()

    # Draw screen, map, and player
    screen.fill(BG_COLOR)
    draw_map()
    player.draw(screen, PLAYER_COLOR)

    # Update display
    pygame.display.update()