import pygame, sys
from Button import *
from settings import *

pygame.init()
# set up pygame dependent environment
TITLEFONT = pygame.font.SysFont(TITLE_FONT, 25)
TITLE = TITLEFONT.render('Wordle', True, TITLE_COLOR)
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

guess_buttons = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letter = -1
for row in range(6):
    guess_row = []
    # comment here and establish algorithm to make sure guess tiles are in the middle of the screen
    for col in range(5):
        letter += 1
        x = LEFT_COL + col * (GUESS_TILE_SIZE[0] + GUESS_TILE_PADDING)
        y = TOP_ROW + row * (GUESS_TILE_SIZE[1] + GUESS_TILE_PADDING)
        button = Button((x, y), GUESS_TILE_SIZE, FONT, alphabet[letter], 16, GUESS_TEXTCOLOR, GUESS_BACKGROUND)
        button.set_outline_style(GUESS_OUTLINE_COLOR, GUESS_OUTLINE_THICKNESS, GUESS_RADIUS)
        guess_row.append(button)
        # testing letter placement and style - for testing only
        if letter >= len(alphabet) - 1:
            letter = -1
    # add column collection to row
    guess_buttons.append(guess_row)


keys = []

current_row = 0
current_letter = 0

while True:
    clock.tick(FPS)
    window.fill(BACKGROUND)
    # display title so that it is always in the center

    # display line across the screen

    # comment here and complete nested for loops to display guessing tiles
    for row in guess_buttons:
        for button in row:
            button.draw(window)

    for key in keys:
        key.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for key in keys:
                if key.enabled and key.button_rect.collidepoint(pos): # key was clicked!
                    key.click_method(current_row, current_letter)

    pygame.display.update()