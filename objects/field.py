from OpenGL.GL import *

class Field:
    def __init__(self, screen_width, screen_height, padding=0.1):
        self.size = screen_height * (1 - padding)  # Поле чуть меньше экрана
        self.half_size = self.size / 2
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self):
        """ Рисует границы поля """
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(-self.half_size / self.screen_width, -self.half_size / self.screen_height)
        glVertex2f( self.half_size / self.screen_width, -self.half_size / self.screen_height)
        glVertex2f( self.half_size / self.screen_width,  self.half_size / self.screen_height)
        glVertex2f(-self.half_size / self.screen_width,  self.half_size / self.screen_height)
        glEnd()
