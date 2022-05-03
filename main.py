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

guess_buttons = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(GUESS_ROWS):
    row = []
    # comment here and establish algorithm to make sure guess tiles are in the middle of the screen
    for j in range(GUESS_COLS):
        center = SCREEN_WIDTH / 2
        dx = (j + 1 - GUESS_COLS / 2) * (GUESS_TILE_SIZE[0] + GUESS_TILE_MARGIN) - GUESS_TILE_SIZE[0] / 2
        x = center + dx
        y = TOP_ROW + i * (GUESS_TILE_SIZE[1] + GUESS_TILE_MARGIN)
        button = Button((x, y), GUESS_TILE_SIZE, FONT, alphabet[0], 16, GUESS_TEXT_COLOR, GUESS_BACKGROUND)
        button.set_outline_style(GUESS_OUTLINE_COLOR, GUESS_OUTLINE_THICKNESS, GUESS_RADIUS)
        row.append(button)
    guess_buttons.append(row)


keys = dict()

def build_key(coords, text, button_size, method):
    button = Button(coords, button_size, FONT, text, KEY_TEXT_SIZE, KEY_TEXT_COLOR, KEY_BACKGROUND)
    button.set_outline_style(outline_radius=KEY_RADIUS)
    button.set_click_method(method)
    button.enable()
    keys[text] = button

# y += SECTION_PADDING
# x = (SCREEN_WIDTH - ((KEY_TILE_SIZE[0] + KEY_MARGIN_X) * len(KEYROW1)) + KEY_MARGIN_X) / 2
# for letter in KEYROW1:
#     build_key((x, y), letter, KEY_TILE_SIZE, 'keyPress')
#     x += KEY_TILE_SIZE[0] + KEY_MARGIN_X
# y += KEY_MARGIN_Y + KEY_TILE_SIZE[1]
    
while True:
    clock.tick(FPS)
    screen.fill(BACKGROUND)
    # display title so that it is always in the center
    x = SCREEN_WIDTH / 2 - TITLE.get_width() / 2
    y = TOP_LINE / 2 - TITLE.get_height() / 2
    screen.blit(TITLE, (x, y))
    
    # display line across the screen
    pygame.draw.line(screen, 'black', (0, TOP_LINE), (SCREEN_WIDTH, TOP_LINE))
    
    for row in guess_buttons:
        for button in row:
            button.draw(screen)

    for key in keys:
        key.draw(screen)
        
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