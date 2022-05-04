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
        self.background_color = background_color
        self.outline_thickness = 0
        self.outline_color = (255, 255, 255)
        self.outline_radius = 0
        
        self.font_bold = True
        self.animation_height = 1
        self.center = self.button_rect.center
        self.next_text = ''
        self.next_color = (0, 0, 0)
        self.next_outline_thickness = 0
        self.next_outline_color = (0, 0, 0)
        
        self.make_surface()

    def make_surface(self):
        font = pygame.font.SysFont(self.font, self.text_size)
        font.set_bold(self.font_bold)
        self.text_surface = font.render(self.text, True, self.text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.outline_color, self.button_rect, 
                             self.outline_thickness, self.outline_radius)
        
        text_width, text_height = self.text_surface.get_rect().size
        text_x = self.x - text_width / 2
        text_y = self.y - text_height / 2
        screen.blit(self.text_surface, (text_x, text_y))
    

    def set_outline_style(self, outline_color=None, outline_thickness=None, outline_radius=None):
        if outline_color:
            self.outline_color = outline_color
        if outline_thickness:
            self.outline_thickness = outline_thickness
        if outline_radius:
            self.outline_radius = outline_radius

    def set_text_properties(self, text=None, text_size=None, text_color=None, font=None):
        if text:
            self.text = text
        if text_size:
            self.text_size = text_size
        if text_size:
            self.text_color = text_color
        if font:
            self.font = font

        self.make_surface()
        
    def set_click_method(self, method):
        self.click_method = method

    def enable(self):
        self.enable = True

    def disable(self):
        self.enabled = False
        
    def set_background_color(self, background_color):
        self.background_color = background_color
        self.make_surface()