import pygame, sys
from settings import *
from Button import *

pygame.init()
pygame.display.set_caption('Wordle')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
TITLEFONT = pygame.font.SysFont(TITLE_FONT, 25)
TITLEFONT.set_bold(True)
TITLE = TITLEFONT.render('Wordle', True, TITLE_COLOR)

def drawTitle(screen):
    x = SCREEN_WIDTH / 2 - TITLE.get_width() / 2
    y = TOP_LINE / 2 - TITLE.get_height() / 2
    screen.blit(TITLE, (x, y))

def build_tiles():
    tiles = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(GUESS_ROWS):
        row = []
        for j in range(GUESS_COLS):
            center = SCREEN_WIDTH / 2
            dx = (j + 1 - GUESS_COLS / 2) * (GUESS_TILE_SIZE[0] + GUESS_TILE_MARGIN) - GUESS_TILE_SIZE[0] / 2
            x = center + dx
            y = TOP_ROW + i * (GUESS_TILE_SIZE[1] + GUESS_TILE_MARGIN)
            tile = Button((x, y), GUESS_TILE_SIZE, FONT, alphabet[0], 16, GUESS_TEXT_COLOR, GUESS_BACKGROUND)
            tile.set_outline_style(GUESS_OUTLINE_COLOR, GUESS_OUTLINE_THICKNESS, GUESS_RADIUS)
            row.append(tile)
        tiles.append(row)
    return tiles

def build_key(coords, text, button_size, method):
    keys = dict()
    key = Button(coords, button_size, FONT, text, KEY_TEXT_SIZE, KEY_TEXT_COLOR, KEY_BACKGROUND)
    key.set_outline_style(outline_radius=KEY_RADIUS)
    key.set_click_method(method)
    key.enable()
    keys[text] = key

def build_keys():
    pass
    # y += SECTION_PADDING
    # x = (SCREEN_WIDTH - ((KEY_TILE_SIZE[0] + KEY_MARGIN_X) * len(KEYROW1)) + KEY_MARGIN_X) / 2
    # for letter in KEYROW1:
    #     build_key((x, y), letter, KEY_TILE_SIZE, 'keyPress')
    #     x += KEY_TILE_SIZE[0] + KEY_MARGIN_X
    # y += KEY_MARGIN_Y + KEY_TILE_SIZE[1]
    
tiles = build_tiles()
keys = build_keys()
while True:
    clock.tick(FPS)
    screen.fill(BACKGROUND)
    drawTitle(screen)
    # display line across the screen
    pygame.draw.line(screen, 'black', (0, TOP_LINE), (SCREEN_WIDTH, TOP_LINE))
    
    for row in tiles:
        for tile in row:
            tile.draw(screen)

    # for key in keys:
    #     key.draw(screen)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for key in keys:
                if key.enabled and key.button_rect.collidepoint(pos): # key was clicked!
                    key.click_method(current_row, current_letter)

    pygame.draw.line(screen, 'red', (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, 500))
    pygame.draw.line(screen, 'red', (0, TOP_ROW), (500, TOP_ROW))
    pygame.display.update()