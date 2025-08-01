import pygame
import math

# Initialize pygame
pygame.init()
pygame.display.set_caption("Raycast")

fov_var = 2.5
SCREEN_DIM = SCREEN_WIDTH, SCREEN_HEIGHT = 512*fov_var, 512
screen = pygame.display.set_mode(SCREEN_DIM)
clock = pygame.time.Clock()

# Set colors
PLAYER_COLOR = (255, 0, 0) # red
GRID_COLOR = (100, 100, 100) # light gray
BG_COLOR = (73, 82, 76)
ONE_COLOR = (121, 128, 123)
TWO_COLOR = (173, 136, 61)
THREE_COLOR = (173, 111, 49)

# Set up map
map_walls = [
    ['1','1','1','1','1','1','1','1'],
    ['1','0','0','0','0','0','0','1'],
    ['1','2','2','2','0','0','0','1'],
    ['1','0','0','2','2','0','0','1'],
    ['1','0','0','0','2','2','0','1'],
    ['1','0','2','0','0','2','3','3'],
    ['1','0','0','0','0','0','0','1'],
    ['1','1','1','1','1','1','1','1'],
]
map_width, map_height = len(map_walls[0]), len(map_walls)
gridline_width = 1 # map square offset, adds negative space background outline around blocks
sq = 64 # square dimensions

# Textures
textures = [
    [
        ['1','0','0','1','1','1','0','1', '1','1','0','0','0','0','1','1'],
        ['1','0','1','1','1','0','1','1', '1','1','1','0','0','1','1','1'],
        ['0','1','1','1','1','0','1','1', '1','1','1','0','0','0','1','1'],
        ['0','0','1','1','1','0','1','1', '1','1','0','0','1','0','0','0'],
        ['1','1','0','0','0','0','0','1', '0','0','1','1','1','1','0','0'],
        ['1','1','0','1','1','1','0','0', '0','1','1','1','1','1','1','0'],
        ['1','1','0','1','1','1','1','0', '0','0','1','1','1','1','0','0'],
        ['1','1','1','0','0','0','0','1', '1','1','0','0','0','0','0','0'],

        ['0','1','1','1','1','0','1','1', '1','1','1','1','1','1','0','0'],
        ['0','1','1','1','1','0','0','0', '1','1','1','1','0','0','1','1'],
        ['0','0','1','1','0','0','0','0', '0','1','1','0','0','1','1','1'],
        ['0','0','0','0','0','1','1','1', '1','0','0','0','1','1','1','1'],
        ['0','1','1','1','0','0','1','1', '1','1','0','0','1','1','1','0'],
        ['1','1','1','1','0','0','0','0', '0','1','1','0','1','1','1','0'],
        ['0','1','1','1','1','1','1','0', '0','0','1','0','0','0','0','0'],
        ['1','0','1','1','1','0','0','1', '1','1','0','0','1','1','0','1'],
    ],
    [
        ['1','1','1','1','1','1','0','1', '1','1','1','1','1','1','0','1'],
        ['1','1','1','1','1','1','0','1', '1','1','1','1','1','1','0','1'],
        ['1','1','1','1','1','1','0','1', '1','1','1','1','1','1','0','1'],
        ['0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0'],
        ['1','1','0','1','1','1','1','1', '1','1','0','1','1','1','1','1'],
        ['1','1','0','1','1','1','1','1', '1','1','0','1','1','1','1','1'],
        ['1','1','0','1','1','1','1','1', '1','1','0','1','1','1','1','1'],
        ['0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0'],

        ['1','1','1','1','1','1','0','1', '1','1','1','1','1','1','0','1'],
        ['1','1','1','1','1','1','0','1', '1','1','1','1','1','1','0','1'],
        ['1','1','1','1','1','1','0','1', '1','1','1','1','1','1','0','1'],
        ['0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0'],
        ['1','1','0','1','1','1','1','1', '1','1','0','1','1','1','1','1'],
        ['1','1','0','1','1','1','1','1', '1','1','0','1','1','1','1','1'],
        ['1','1','0','1','1','1','1','1', '1','1','0','1','1','1','1','1'],
        ['0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0'],
    ],
    [
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],

        ['1','0','0','1','0','1','1','0', '0','0','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '0','0','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
        ['1','0','0','1','0','1','1','1', '1','1','1','0','1','0','0','1'],
    ],
]

x_resolution = 128

# Set up player class
class Player:
    def __init__(self, x, y, radius, move_speed, rotation, rotation_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.move_speed = move_speed
        self.rotation = rotation # rotation in radians [0,2pi)
        self.rotation_speed = rotation_speed

    def move(self, signfb, signlr):
        if signfb == 0 and signlr == 0:
            return

        dx = self.move_speed * math.cos(self.rotation) * signfb
        dy = self.move_speed * math.sin(self.rotation) * signfb
        grid_x = int((self.x + 1.5 * dx) / 64) # collision detection
        grid_y = int((self.y + 1.5 * dy) / 64)
        if (map_walls[grid_y][grid_x] != '0'):
            return
        self.x += dx
        self.y += dy

        dx = self.move_speed * math.cos(self.rotation + math.pi/2) * signlr
        dy = self.move_speed * math.sin(self.rotation + math.pi/2) * signlr
        grid_x = int((self.x + 1.5 * dx) / 64) # collision detection
        grid_y = int((self.y + 1.5 * dy) / 64)
        if (map_walls[grid_y][grid_x] != '0'):
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

    def interact(self):
        dx = self.radius * 8 * math.cos(self.rotation)
        dy = self.radius * 8 * math.sin(self.rotation)
        sx, sy = map_at_ray((self.x + dx, self.y + dy))
        map_wall = map_walls[sy][sx]
        if map_wall == '3':
            map_walls[sy][sx] = '0'

    def draw_rays(self):
        distances = []
        half_range = int(x_resolution / 2)
        for i in range(-half_range, half_range):
            dtheta = 1.7 * i * math.pi / 180 * (64 / x_resolution)
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
                sx, sy = map_at_ray(h_rayloc)
                map_block = map_walls[sy][sx]
                color = map_to_color(side, map_block)
                distances.append((h_dist, side, map_block, h_rayloc, self.rotation))
            else:
                rx, ry = v_rayloc
                side = 'V'
                sx, sy = map_at_ray(v_rayloc)
                map_block = map_walls[sy][sx]
                color = map_to_color(side, map_block)
                distances.append((v_dist, side, map_block, v_rayloc, self.rotation))

            pygame.draw.line(screen, color, (self.x, self.y), (rx, ry), 2)

        return distances

    def ray_in_wall(self, ray):
        sx, sy = map_at_ray(ray)
        return map_walls[sy][sx] != '0'

def map_at_ray(ray):
    rx, ry = ray
    sx = int(rx / sq)
    sy = int(ry / sq)
    if sx > 7 or sx < 0 or sy > 7 or sy < 0:
        return (0, 0)
    return (sx, sy)

# Draws map on screen from variable map where value == 1
def draw_map():
    # Loop through each value in map
    for h in range(map_height):
        for w in range(map_width):
            # Top left coords of square
            start_x = w * sq
            start_y = h * sq

            # If map position != 0, draw rect
            if map_walls[h][w] != '0':
                pygame.draw.rect(screen, map_to_color('M', map_walls[h][w]), (start_x, start_y, sq, sq))

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
    ivar = (SCREEN_WIDTH - 512) / 128
    for i, ray_info in enumerate(rays):
        start_x = 512 + i * ivar
        dist, side, map_type, rayloc, rot = ray_info
        rx, ry = rayloc

        height_scalar = 0.5
        slice_height = 64 * SCREEN_HEIGHT / dist * height_scalar
        start_y = SCREEN_HEIGHT / 2 - slice_height / 2
        y_slice = slice_height / 16

        if side == "V":
            tx = math.floor(rx % 64 / 4)
            if rot < math.pi:
                tx = 15 - tx
        elif side == "H":
            tx = math.floor(ry % 64 / 4)
            if rot > math.pi / 2 and rot < 3 * math.pi / 2:
                tx = 15 - tx
        for ty in range(16):
            color = get_pixel_color(map_type, side, (tx, ty))
            pygame.draw.rect(screen, color, (start_x, start_y, ivar, y_slice+1))
            start_y += y_slice

def get_pixel_color(map_type, side, texture_loc):
    tx, ty = texture_loc
    color = map_to_color(side, map_type)
    if map_type in ['1', '2', '3']:
        pixel_loc = textures[int(map_type)-1][ty][tx]
        if pixel_loc == '0':
            color = color_shift(color, 0.8)
        elif pixel_loc == '1':
            color = color_shift(color, 1.2)
    return color

def map_to_color(side, map_type):
    color = (0, 0, 0)
    if map_type == '1':
        color = ONE_COLOR
    elif map_type == '2':
        color = TWO_COLOR
    elif map_type == '3':
        color = THREE_COLOR

    if side == "M":
        return color
    elif side == "H":
        color = color_shift(color, 1.1)
    elif side == "V":
        color = color_shift(color, 0.9)
    return color

def color_shift(color, scalar):
    r, g, b = color
    r = min(r * scalar, 255)
    g = min(g * scalar, 255)
    b = min(b * scalar, 255)
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

    signfb, signlr = 0, 0
    if keys[pygame.K_w]:
        signfb += 1
    if keys[pygame.K_s]:
        signfb -= 1
    if keys[pygame.K_a]:
        signlr -= 1
    if keys[pygame.K_d]:
        signlr += 1
    if signfb != 0 and signlr != 0:
        sqrhf = math.sqrt(1/2)
        signfb *= sqrhf
        signfb *= sqrhf
    player.move(signfb, signlr)

    if keys[pygame.K_LEFT]:
        player.turn(-1)
    if keys[pygame.K_RIGHT]:
        player.turn(1)
    if keys[pygame.K_e]:
        player.interact()

    # Draw screen, map, and player
    screen.fill(BG_COLOR)
    draw_map()
    rays = player.draw_rays()
    draw_3d(rays)
    player.draw()

    # Update display
    pygame.display.update()