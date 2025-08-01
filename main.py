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
GRID_COLOR = (100, 100, 100) # light gray
BG_COLOR = (0, 0, 0) # black

# Set up map
map = [
    ['1','1','1','1','1','1','1','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','1','1','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','1','0','1'],
    ['1','0','1','0','0','1','0','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','1','1','1','1','1','1','1'],
]
map_width, map_height = len(map[0]), len(map)
gridline_width = 1 # map square offset, adds negative space background outline around blocks
sq = 64 # square dimensions

# Set up player class
class Player:
    def __init__(self, x, y, radius, move_speed, rotation, rotation_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.move_speed = move_speed
        self.rotation = rotation # rotation in radians [0,2pi)
        self.rotation_speed = rotation_speed

    def move(self, sign):
        if sign not in [1, -1]:
            raise ValueError("sign must be 1 or -1")

        dx = self.move_speed * math.cos(self.rotation) * sign
        dy = self.move_speed * math.sin(self.rotation) * sign
        grid_x = int((self.x + 1.5 * dx) / 64) # collision detection
        grid_y = int((self.y + 1.5 * dy) / 64)
        if (map[grid_y][grid_x] == '1'):
            return
        self.x += dx
        self.y += dy

    def turn(self, sign):
        if sign not in [1, -1]:
            raise ValueError("sign must be 1 or -1")

        self.rotation += self.rotation_speed * sign
        if self.rotation < 0:
            self.rotation += 2 * math.pi
        if self.rotation > 2 * math.pi:
            self.rotation -= 2 * math.pi

    def draw(self):
        pygame.draw.circle(screen, PLAYER_COLOR, (self.x, self.y), self.radius, self.radius)  # body
        dx = self.radius * 1.5 * math.cos(self.rotation)
        dy = self.radius * 1.5 * math.sin(self.rotation)
        pygame.draw.line(screen, PLAYER_COLOR, (self.x, self.y), (self.x + dx, self.y + dy), 3)

    def draw_rays(self):
        distances = []
        for i in range(-30, 30):
            dtheta = i * math.pi / 180
            theta = self.rotation + dtheta
            if theta > 2 * math.pi:
                theta -= 2 * math.pi
            elif theta < 0:
                theta += 2 * math.pi
            tanth = math.tan(theta)
            atanth = 1 / tanth

            # Horizontal
            rx, ry = self.x, self.y
            if theta < math.pi:
                ry = math.ceil(self.y / sq) * sq + 0.0001
                dy = sq
            else:
                ry = math.floor(self.y / sq) * sq - 0.0001
                dy = -sq
            rx = self.x + (ry - self.y) * atanth
            if rx > SCREEN_WIDTH:
                rx = SCREEN_WIDTH
                ry = self.y + (rx - self.x) * tanth
            elif rx < 0:
                rx = 0
                ry = self.y + (rx - self.x) * tanth
            # (rx, ry) at this point is the first vertical contact the ray makes

            dx = dy * atanth
            while not self.ray_in_wall((rx, ry)):
                rx += dx
                ry += dy
            v_rayloc = (rx, ry)

            # Horizontal
            rx, ry = self.x, self.y
            if theta < math.pi / 2 or theta > 3 * math.pi / 2:
                rx = math.ceil(self.x / sq) * sq + 0.0001
                dx = sq
            else:
                rx = math.floor(self.x / sq) * sq - 0.0001
                dx = -sq
            ry = self.y + (rx - self.x) * tanth
            if ry > SCREEN_HEIGHT:
                ry = SCREEN_HEIGHT
                rx = self.x + (ry - self.y) * atanth
            elif ry < 0:
                ry = 0
                rx = self.x + (ry - self.y) * atanth
            # (rx, ry) at this point is the first horizontal contact the ray makes

            dy = dx * tanth
            while not self.ray_in_wall((rx, ry)):
                rx += dx
                ry += dy
            h_rayloc = (rx, ry)

            # Find shortest ray
            hx, hy = h_rayloc
            hdx, hdy = hx - self.x, hy - self.y
            h_dist = math.sqrt(hdx * hdx + hdy * hdy)

            vx, vy = v_rayloc
            vdx, vdy = vx - self.x, vy - self.y
            v_dist = math.sqrt(vdx * vdx + vdy * vdy)

            if h_dist < v_dist:
                rx, ry = h_rayloc
                distances.append(h_dist)
            else:
                rx, ry = v_rayloc
                distances.append(v_dist)

            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (rx, ry), 2)

        return distances

    def ray_in_wall(self, ray):
        rx, ry = ray
        sx = int(rx / sq)
        sy = int(ry / sq)
        if sx > 7 or sx < 0 or sy > 7 or sy < 0:
            return True
        #print("({}, {})".format(sx, sy))
        return map[sy][sx] != '0'

# Draws map on screen from variable map where value == 1
def draw_map():
    # Loop through each value in map
    for h in range(map_height):
        for w in range(map_width):
            # Top left coords of square
            start_x = w * sq
            start_y = h * sq

            # If map position == 1, draw rect
            if map[h][w] == '1':
                pygame.draw.rect(screen, MAP_COLOR, (start_x, start_y, sq, sq))

            top_left = (start_x, start_y)
            top_right = (start_x + sq, start_y)
            bottom_left = (start_x, start_y + sq)
            bottom_right = (start_x + sq, start_y + sq)
            # Draw grid lines
            pygame.draw.line(screen, GRID_COLOR, top_left, top_right, gridline_width) # top
            pygame.draw.line(screen, GRID_COLOR, top_left, bottom_left, gridline_width) # left
            pygame.draw.line(screen, GRID_COLOR, top_right, bottom_right, gridline_width) # right
            pygame.draw.line(screen, GRID_COLOR, bottom_left, bottom_right, gridline_width) # bottom

# Initialize player
player = Player(200, 300, 5, 3, .5, 0.1)

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
        player.move(1)
    if keys[pygame.K_s]:
        player.move(-1)
    if keys[pygame.K_a]:
        player.turn(-1)
    if keys[pygame.K_d]:
        player.turn(1)

    # Draw screen, map, and player
    screen.fill(BG_COLOR)
    draw_map()
    print(player.draw_rays())
    player.draw()

    # Update display
    pygame.display.update()