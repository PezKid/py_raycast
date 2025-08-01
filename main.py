import pygame

pygame.init()

PLAYER_COLOR = (255, 0, 0) # red
MAP_COLOR = (255, 255, 255) # white
BG_COLOR = (0, 0, 0) # black

SCREEN_DIM = SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
screen = pygame.display.set_mode(SCREEN_DIM)

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
mso = 1 # map square offset

def drawMap():
    square_width = SCREEN_WIDTH // map_width
    square_height = SCREEN_HEIGHT // map_height
    for h in range(map_height):
        for w in range(map_width):
            if map[h][w] == '1':
                startx = w * square_height
                starty = h * square_width
                pygame.draw.rect(screen, MAP_COLOR, (startx+mso, starty+mso, square_width-mso, square_height-mso))

def drawPlayer():
    pygame.draw.rect(screen, PLAYER_COLOR, (200, 300, 10, 10))

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BG_COLOR)
    drawMap()
    drawPlayer()

    pygame.display.update()