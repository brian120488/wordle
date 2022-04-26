import pygame
from settings import *

class Button:
    def __init__(self, coords, size, font, text, text_size, text_color, background_color):
        self.x, self.y = coords
        self.width, self.height = size
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height) # comment here
        self.font = font
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.enabled = False
        self.click_method = None
        self.make_surface()
        self.background_color = background_color
        self.outline_thickness = 0
        self.outline_color = (255, 255, 255)
        self.outline_radius = 0

    def make_surface(self):
        font = pygame.font.SysFont(self.font, self.text_size)
        self.text_surface = font.render(self.text, True, self.text_color)

    def draw(self, window):
        pygame.draw.rect(window, self.background_color, self.button_rect)
        # come up with a mechanism to make sure that the letter/text is in the middle of the button
        window.blit(self.text_surface, (self.x, self.y))
        if self.outline_thickness != 0: # comment here
            pygame.draw.rect(window, self.outline_color, self.button_rect, self.outline_radius)

    def set_outline_style(self, outline_color, outline_thickness, outline_radius):
        self.outline_color = outline_color
        # outline thickness acts as a toggle = 0 is off
        self.outline_thickness = outline_thickness
        self.outline_radius = outline_radius

    def set_text_properties(self, *, text=None, text_size=None, text_color=None, font=None):
        # comment here
        if text != None:
            self.text = text
        if text_size != None:
            self.text_size = text_size
        if text_size != None:
            self.text_color = text_color
        if font != None:
            self.font = font

        self.make_surface()