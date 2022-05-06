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
word = "carab"

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
            dx = (j + 1 - GUESS_COLS / 2) * (GUESS_TILE_SIZE[0] + GUESS_TILE_MARGIN) - GUESS_TILE_SIZE[0] / 2
            x = CENTER_X + dx
            y = TOP_ROW + i * (GUESS_TILE_SIZE[1] + GUESS_TILE_MARGIN)
            tile = Button((x, y), GUESS_TILE_SIZE, FONT, '', 16, GUESS_TEXT_COLOR, GUESS_BACKGROUND)
            tile.set_outline_style(GUESS_OUTLINE_COLOR, GUESS_OUTLINE_THICKNESS, GUESS_RADIUS)
            row.append(tile)
        tiles.append(row)
    return tiles

def build_key(keys, coords, text, button_size, method):
    key = Button(coords, button_size, FONT, text, KEY_TEXT_SIZE, KEY_TEXT_COLOR, KEY_BACKGROUND)
    key.set_outline_style(outline_color=KEY_BACKGROUND, outline_radius=KEY_RADIUS)
    key.set_click_method(method)
    key.enable()
    keys[text] = key

def build_keys():
    keys = dict()
    y = TOP_ROW + 6 * (GUESS_TILE_SIZE[1] + GUESS_TILE_MARGIN)
    build_row(keys, KEYROW1, y)
    y += KEY_TILE_SIZE[1] + KEY_MARGIN_Y
    build_row(keys, KEYROW2, y)
    y += KEY_TILE_SIZE[1] + KEY_MARGIN_Y
    build_row(keys, KEYROW3, y)
    return keys
    
def build_row(keys, key_row, y):
    for i, letter in enumerate(key_row):
        if key_row == KEYROW3:
            width = KEY_TILE_SIZE[0] * 1.5 + KEY_MARGIN_X / 2
            height = KEY_TILE_SIZE[1]
            if i == 0:
                x = CENTER_X - 4.25 * KEY_TILE_SIZE[0] - 3.75 * KEY_MARGIN_X
                build_key(keys, (x, y), 'ENTER', (width, height), enter)
            if i == len(key_row) - 1:
                x = CENTER_X + 4.25 * KEY_TILE_SIZE[0] + 4.75 * KEY_MARGIN_X
                build_key(keys, (x, y), 'DEL', (width, height), delete)
        dx = (i + 1 - len(key_row) / 2) * (KEY_TILE_SIZE[0] + KEY_MARGIN_X) - KEY_TILE_SIZE[0] / 2
        x = CENTER_X + dx
        build_key(keys, (x, y), letter, KEY_TILE_SIZE, keyPress)

def keyPress(key):
    global current_letter, current_row

    if current_letter < 5:
        tile = tiles[current_row][current_letter]
        tile.set_text_properties(text=key)
        tile.set_outline_style(outline_color=GUESSING_OUTLINE_COLOR)
        current_letter += 1

def delete(key):
    global current_letter, current_row
    
    if current_letter > 0:
        current_letter -= 1
        tile = tiles[current_row][current_letter]
        tile.set_text_properties(text='')
        tile.set_outline_style(outline_color=GUESS_OUTLINE_COLOR)  

def enter(key):
    global current_letter, current_row
    
    if current_letter == 5:
        for i in range(5):
            tile = tiles[current_row][i]
            if tile.text == word[i]:
                new_color = GUESS_CORRECT
            elif tile.text in word:
                new_color = GUESS_IN_ANSWER
            else:
                new_color = GUESS_WRONG
            tiles[current_row][i].set_next_properties(new_color, 0, None, GUESS)
            if i == 0:
                tiles[current_row][i].animation_change = -ANIMATION_SPEED
                animation.append((current, 0))
        current_row += 1

tiles = build_tiles()
keys = build_keys()
current_letter = 0
current_row = 0
animation = []  # current buttons being animated
while True:
    clock.tick(FPS)
    screen.fill(BACKGROUND)
    drawTitle(screen)
    pygame.draw.line(screen, 'black', (0, TOP_LINE), (SCREEN_WIDTH, TOP_LINE))
    
    for row in range(len(tiles)):
        for col in range(len(tiles[0])):
            tile = tiles[row][col]
            if (row, col) in animation:
                if len(animation) == 1 and col < 4 and tile.animation_height <= 0.2:
                    next_tile = tiles[row][col + 1]
                    next_tile.animation_change = -ANIMATION_SPEED
                    animation.append((row, col + 1))
                tile.animation_height += round(tile.animation_change, 2)
                if tile.animation_height <= 0:
                    tile.animation_change *= -1
                    tile.animation_height = round(tile.animation_change, 2)
                    tile.flip_next()
                elif tile.animation_height >= 1:
                    tile.animation_height = 1
                    tile.animation_change = 0
                    animation.remove((row, col))
                    if col == 4:
                        for i in range(5):
                            if keys[tiles[row][i].text].background_color != GUESS_CORRECT:
                                keys[tiles[row][i].text].background_color = tiles[row][i].background_color
                                keys[tiles[row][i].text].make_surface()
            tile.draw(screen)

    for key in keys.values():
        key.draw(screen)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for key in keys.values():
                if key.enabled and key.button_rect.collidepoint(pos):
                    key.click_method(key.text)

    pygame.display.update()