import pygame, sys, random, configparser
from settings import *
from Button import *

def draw_title(screen):
    TITLEFONT = pygame.font.SysFont(TITLE_FONT, 25)
    TITLEFONT.set_bold(True)
    TITLE = TITLEFONT.render('Wordle', True, TITLE_COLOR)
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

    if current_letter < 5 and current_row < 6:
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
    
    if current_letter != 5: return
    if not word_is_valid(solution, current_row): return

    for i in range(5):
        tile = tiles[current_row][i]
        if tile.text == solution[i]:
            new_color = GUESS_CORRECT
        elif tile.text in solution:
            new_color = GUESS_IN_ANSWER
        else:
            new_color = GUESS_WRONG
        tiles[current_row][i].set_next_properties(new_color, 0)
        if i == 0:
            tiles[current_row][i].animation_change = -ANIMATION_SPEED
            animation.append((current_row, 0))

def update_tile_animations(animation):
    for row, col in animation:
        tile = tiles[row][col]
        tile.animation_height += round(tile.animation_change, 2)

def updateKeyboard(tiles, keys):
    for i in range(5):
        if keys[tiles[row][i].text].background_color != GUESS_CORRECT:
            keys[tiles[row][i].text].background_color = tiles[row][i].background_color
        keys[tiles[row][i].text].text_color = tiles[row][i].text_color
        keys[tiles[row][i].text].make_surface()

def load_file_into_set(filename):
    L = set()
    with open(filename, 'r') as f:
        for line in f:
            for word in line.split(', '):
                L.add(word.strip("\""))
    return L

def word_is_valid(solution, current_row):
    global scores
    
    checker = ''
    for i in range(5):
        letter_string = str(tiles[current_row][i].text)
        checker += letter_string
    checker = checker.lower()
    if checker in valid_guesses or checker in solutions:
        return True
    
    invalid_button = Button(INVALID_GUESS_COORDS, INVALID_GUESS_SIZE, FONT, 
                'Not in word list', INVALID_GUESS_TEXT_SIZE, GUESS_TEXT_COLOR, (255, 255, 255))
    invalid_button.set_outline_style(None, 0, KEY_RADIUS)
    j = 0
    while j < 50:
        invalid_button.draw(screen)
        j += 1
        pygame.display.update()
    return False

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('scores.ini') 
def update_stats():
    scores = [int(score) for score in config['stats']['scores'].split(', ')]
    current_streak = int(config['stats']['current_streak'])
    max_streak = int(config['stats']['max_streak'])
    if current_row < 6:
        current_streak += 1
        if current_streak > max_streak:
            max_streak = current_streak
    else:
        streak = 0
    scores[current_row] = int(scores[current_row]) + 1
    config.set('stats', 'scores', scores)
    config.set('stats', 'current_streak', current_streak)
    config.set('stats', 'max_streak', max_streak)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def check_win(tiles):
    row_word = "".join([tile.text for tile in tiles[current_row]])
    return row_word == solution
  
def animate_win_screen(tiles):
    global dance_animation, current_dance
    if current_dance < 5:
        tile = tiles[current_row][current_dance]
        tile.prevY = tile.y
        dance_animation.append(tile)
        current_dance += 1
            
    for i in range(len(dance_animation) - 1, -1, -1):
        tile = dance_animation[i]
        tile.y -= tile.dance_change
        tile.dance_change += tile.dance_accel
        if tile.y <= tile.prevY - tile.dance_height:
            tile.dance_change *= -1
        if tile.y >= tile.prevY:
            tile.y = tile.prevY
            dance_animation.remove(tile)  
                
        if len(dance_animation) == 0: return

def display_answer(screen):
    font = pygame.font.SysFont(FONT, 20)
    text_surface = font.render(solution, True, (0, 0, 0))
    text_x = SCREEN_WIDTH / 2 - text_surface.get_width() / 2
    text_y = TOP_LINE * 1.2
    screen.blit(text_surface, (text_x, text_y)) 

pygame.init()
pygame.display.set_caption('Wordle')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()      
tiles = build_tiles()
keys = build_keys()
current_letter = 0
current_row = 0
animation = []  # current buttons being animated
solutions = load_file_into_set('solutions.txt')
valid_guesses = load_file_into_set('valid_guesses.txt')
solution = random.choice(tuple(solutions)).upper()
print(solution)
is_game_over = False
dance_animation = []
current_dance = 0
while True:
    clock.tick(FPS)
    screen.fill(BACKGROUND)
    draw_title(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for key in keys.values():
                if key.enabled and key.button_rect.collidepoint(pos):
                    key.click_method(key.text)

    pygame.draw.line(screen, 'black', (0, TOP_LINE), (SCREEN_WIDTH, TOP_LINE))
    update_tile_animations(animation) 
    for row in range(len(tiles)):
        for col in range(len(tiles[0])):
            tile = tiles[row][col]
            if (row, col) in animation:
                if len(animation) == 1 and col < 4 and tile.animation_height <= 0.2:
                    next_tile = tiles[row][col + 1]
                    next_tile.animation_change = -ANIMATION_SPEED
                    animation.append((row, col + 1))
                if tile.animation_height <= 0:
                    tile.animation_change *= -1
                    tile.animation_height = round(tile.animation_change, 2)
                    tile.flip_next()
                elif tile.animation_height > 1:
                    tile.animation_height = 1
                    tile.animation_change = 0
                    animation.remove((row, col))
                    if col == 4:
                        updateKeyboard(tiles, keys)
                        if check_win(tiles) and len(animation) == 0:
                            print('won')
                            current_row -= 1
                            is_game_over = True
                        current_row += 1
                        current_letter = 0
                        
            tile.draw(screen)

    for key in keys.values():
        key.draw(screen)
        
    if current_row >= 6:
        is_game_over = True
    
    if is_game_over:
        display_answer(screen)
        if current_row < 6:
            animate_win_screen(tiles)
    
    pygame.display.update()