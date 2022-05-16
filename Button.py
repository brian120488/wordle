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
        self.outline_radius = 0
        
        self.font_bold = True
        self.animation_height = 1
        self.animation_change = 0
        self.dance_height = 25
        self.dance_change = 5
        self.dance_accel = 2
        self.center = self.button_rect.center
        self.next_text = ''
        self.next_background_color = None
        self.next_text_color = None
        self.next_outline_thickness = None
        self.next_outline_color = None
        
        self.make_surface()

    def make_surface(self):
        font = pygame.font.SysFont(self.font, self.text_size)
        font.set_bold(self.font_bold)
        self.text_surface = font.render(self.text, True, self.text_color)

    def draw(self, screen):
        if self.animation_height != 1:
            x, y = self.x - self.width / 2, self.y - self.height / 2
            animated_rect = pygame.Rect(x, y, self.width, self.height)
            animated_rect.height = self.animation_height * self.button_rect.height
            animated_rect.center = self.button_rect.center
            pygame.draw.rect(screen, self.background_color, animated_rect, self.outline_thickness, self.outline_radius)
            
            animated_size = self.text_surface.get_size()
            animated_size = (animated_size[0], animated_size[1] * self.animation_height)
            animated_surface = pygame.transform.scale(self.text_surface, animated_size)

            text_width, text_height = animated_surface.get_rect().size
            text_x = self.x - text_width / 2
            text_y = self.y - text_height / 2
            screen.blit(animated_surface, (text_x, text_y))
            return
        
        self.button_rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, 
                                       self.width, self.height)
        pygame.draw.rect(screen, self.background_color, self.button_rect, self.outline_thickness, self.outline_radius) 
        text_width, text_height = self.text_surface.get_rect().size
        text_x = self.x - text_width / 2
        text_y = self.y - text_height / 2
        screen.blit(self.text_surface, (text_x, text_y))

    def set_outline_style(self, outline_color=None, outline_thickness=None, outline_radius=None):
        if outline_color is not None:
            self.background_color = outline_color
        if outline_thickness is not None:
            self.outline_thickness = outline_thickness
        if outline_radius is not None:
            self.outline_radius = outline_radius

    def set_text_properties(self, text=None, text_size=None, text_color=None, font=None):
        if text is not None:
            self.text = text
        if text_size is not None:
            self.text_size = text_size
        if text_size is not None:
            self.text_color = text_color
        if font is not None:
            self.font = font

        self.make_surface()
   
    def set_next_properties(self, next_background_color=None, next_outline_thickness=None, next_text_color=None):
        if next_background_color is not None:
            self.next_background_color = next_background_color
        if next_outline_thickness is not None:
            self.next_outline_thickness = next_outline_thickness
        if next_text_color is not None:
            self.next_text_color = next_text_color

    def flip_next(self):
        if self.next_text_color is not None:
            self.text_color = self.next_text_color
            self.next_text_color = None
        if self.next_background_color is not None:
            self.background_color = self.next_background_color
            self.next_background_color = None
        if self.next_outline_thickness is not None:
            self.outline_thickness = self.next_outline_thickness
            self.next_outline_thickness = None
            
        self.make_surface()

    def set_click_method(self, method):
        self.click_method = method

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        
    def set_background_color(self, background_color):
        self.background_color = background_color
        self.make_surface()
