import pygame
from settings import *

class Button:
    def __init__(self, coords, size, font, text, text_size, text_color, background_color):
        self.x, self.y = coords
        self.width, self.height = size
        self.button_rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, 
                                       self.width, self.height)
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.button_rect)
        
        text_width, text_height = self.text_surface.get_rect().size
        text_x = self.x - text_width / 2
        text_y = self.y - text_height / 2
        screen.blit(self.text_surface, (text_x, text_y))
        
        if self.outline_thickness:
            pygame.draw.rect(screen, self.outline_color, self.button_rect, 
                             self.outline_thickness, self.outline_radius)

    def set_outline_style(self, outline_color, outline_thickness, outline_radius):
        self.outline_color = outline_color
        # outline thickness acts as a toggle = 0 is off
        self.outline_thickness = outline_thickness
        self.outline_radius = outline_radius

    def set_text_properties(self, *, text=None, text_size=None, text_color=None, font=None):
        # comment here
        if text:
            self.text = text
        if text_size:
            self.text_size = text_size
        if text_size:
            self.text_color = text_color
        if font:
            self.font = font

        self.make_surface()