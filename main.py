import pygame, sys
from settings import *
from Button import *

pygame.init()
pygame.display.set_caption('Wordle')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

TITLEFONT = pygame.font.SysFont(TITLE_FONT, 25)
TITLE = TITLEFONT.render('Wordle', True, TITLE_COLOR)

guess_buttons = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for row in range(GUESS_ROWS):
    button_row = []
    # comment here and establish algorithm to make sure guess tiles are in the middle of the screen
    for col in range(GUESS_COLS):
        center = SCREEN_WIDTH / 2
        dx = (col + 1 - GUESS_COLS / 2) * (GUESS_TILE_SIZE[0] + GUESS_TILE_PADDING) - GUESS_TILE_SIZE[0] / 2
        x = center + dx

        y = TOP_ROW + row * (GUESS_TILE_SIZE[1] + GUESS_TILE_PADDING)
        button = Button((x, y), GUESS_TILE_SIZE, FONT, alphabet[0], 16, GUESS_TEXTCOLOR, GUESS_BACKGROUND)
        button.set_outline_style(GUESS_OUTLINE_COLOR, GUESS_OUTLINE_THICKNESS, GUESS_RADIUS)
        button_row.append(button)
    guess_buttons.append(button_row)


keys = []

while True:
    clock.tick(FPS)
    screen.fill(BACKGROUND)
    # display title so that it is always in the center

    # display line across the screen

    # comment here and complete nested for loops to display guessing tiles
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
    pygame.display.update()