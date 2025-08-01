import pygame
import math

# Initialize pygame
pygame.init()
pygame.display.set_caption("Raycast")
SCREEN_DIM = SCREEN_WIDTH, SCREEN_HEIGHT = 512*2, 512
screen = pygame.display.set_mode(SCREEN_DIM)
clock = pygame.time.Clock()

# Set colors
PLAYER_COLOR = (255, 0, 0) # red
GRID_COLOR = (100, 100, 100) # light gray
BG_COLOR = (73, 82, 76)
ONE_COLOR = (121, 128, 123)
TWO_COLOR = (173, 136, 61)

# Set up map
map = [
    ['1','1','1','1','1','1','1','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','2','2','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','2','0','1'],
    ['1','0','2','0','0','2','0','1'],
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
        if (map[grid_y][grid_x] != '0'):
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
        for i in range(-32, 32):
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
            h_dist = math.sqrt(hdx * hdx + hdy * hdy) * math.cos(dtheta)

            vx, vy = v_rayloc
            vdx, vdy = vx - self.x, vy - self.y
            v_dist = math.sqrt(vdx * vdx + vdy * vdy) * math.cos(dtheta)

            if h_dist < v_dist:
                rx, ry = h_rayloc
                side = 'H'
                map = map_at_ray(h_rayloc)
                color = map_to_color(side, map)
                distances.append((h_dist, side, map))
            else:
                rx, ry = v_rayloc
                side = 'V'
                map = map_at_ray(v_rayloc)
                color = map_to_color(side, map)
                distances.append((v_dist, side, map))

            pygame.draw.line(screen, color, (self.x, self.y), (rx, ry), 2)

        return distances

    def ray_in_wall(self, ray):
        return map_at_ray(ray) != '0'

def map_at_ray(ray):
    rx, ry = ray
    sx = int(rx / sq)
    sy = int(ry / sq)
    if sx > 7 or sx < 0 or sy > 7 or sy < 0:
        return None
    return map[sy][sx]

# Draws map on screen from variable map where value == 1
def draw_map():
    # Loop through each value in map
    for h in range(map_height):
        for w in range(map_width):
            # Top left coords of square
            start_x = w * sq
            start_y = h * sq

            # If map position != 0, draw rect
            if map[h][w] != '0':
                pygame.draw.rect(screen, map_to_color('M', map[h][w]), (start_x, start_y, sq, sq))

            top_left = (start_x, start_y)
            top_right = (start_x + sq, start_y)
            bottom_left = (start_x, start_y + sq)
            bottom_right = (start_x + sq, start_y + sq)
            # Draw grid lines
            pygame.draw.line(screen, GRID_COLOR, top_left, top_right, gridline_width) # top
            pygame.draw.line(screen, GRID_COLOR, top_left, bottom_left, gridline_width) # left
            pygame.draw.line(screen, GRID_COLOR, top_right, bottom_right, gridline_width) # right
            pygame.draw.line(screen, GRID_COLOR, bottom_left, bottom_right, gridline_width) # bottom

def draw_3d(rays):
    start_x, start_y = 0, 0
    for i, ray_info in enumerate(rays):
        start_x = 512 + i * 8
        start_y = 0
        dist, side, map_type = ray_info
        color = map_to_color(side, map_type)

        slice_height = 64 * SCREEN_HEIGHT / dist
        start_y = SCREEN_HEIGHT / 2 - slice_height / 2
        pygame.draw.rect(screen, color, (start_x, start_y, 8, slice_height))

def map_to_color(side, map_type):
    color = (0, 0, 0)
    if map_type == '1':
        color = ONE_COLOR
    elif map_type == '2':
        color = TWO_COLOR

    if side == "M":
        return color
    elif side == "H":
        r, g, b = color
        r = min(r * 1.1, 255)
        g = min(g * 1.1, 255)
        b = min(b * 1.1, 255)
        color = (r, g, b)
    elif side == "V":
        r, g, b = color
        r *= 0.9
        g *= 0.9
        b *= 0.9
        color = (r, g, b)
    return color

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
    rays = player.draw_rays()
    draw_3d(rays)
    player.draw()

    # Update display
    pygame.display.update()