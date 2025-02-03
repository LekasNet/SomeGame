import random
from OpenGL.GL import *
import math

class NPC:
    def __init__(self, field, x, y, size=200, speed=4, mode=1):
        self.size = size
        self.half_size = size / 2
        self.field = field  # Ссылка на объект игрового поля
        self.x = x
        self.y = y
        self.mode = mode
        self.speed = speed if mode == 1 else 0  # Движение только в mode 1
        self.velocity_x = self.speed * random.choice([-1, 1]) * random.uniform(0.5, 1.0)
        self.velocity_y = self.speed * random.choice([-1, 1]) * random.uniform(0.5, 1.0)
        self.color = (random.random(), random.random(), random.random())

        self.health = 3  # Стартовое здоровье
        self.has_spikes = False  # Флаг наличия шипов

    def update(self, npcs):
        """ Обновляет позицию NPC, проверяет столкновения с границами и другими NPC """
        if self.mode == 0:
            return  # Если mode = 0, NPC не двигается

        prev_x, prev_y = self.x, self.y

        # Обновление позиции
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Столкновение с границами поля
        if self.x + self.half_size > self.field.half_size or self.x - self.half_size < -self.field.half_size:
            self.velocity_x *= -1
            self.x = prev_x  # Откат к предыдущей позиции

        if self.y + self.half_size > self.field.half_size or self.y - self.half_size < -self.field.half_size:
            self.velocity_y *= -1
            self.y = prev_y  # Откат к предыдущей позиции

        # Проверяем столкновения с другими NPC
        for npc in npcs:
            if npc is not self and self.check_collision(npc):
                self.resolve_collision(npc)

    def check_collision(self, other):
        """ Проверяет столкновение по границам квадратов с допуском (penetration depth) """
        overlap_x = self.size - abs(self.x - other.x)
        overlap_y = self.size - abs(self.y - other.y)

        return overlap_x > 0 and overlap_y > 0  # Если есть пересечение по обеим осям

    def resolve_collision(self, other):
        """ Улучшенное отражение при столкновении с учётом уровня проникновения """
        # Если у одного из NPC есть шипы - наносим урон
        if self.has_spikes:
            other.health -= 1  # Уменьшаем здоровье у другого NPC
            self.has_spikes = False  # Шипы пропадают после удара

        if other.has_spikes:
            self.health -= 1
            other.has_spikes = False

        delta_x = self.x - other.x
        delta_y = self.y - other.y

        # Определяем глубину проникновения
        overlap_x = self.size - abs(delta_x)
        overlap_y = self.size - abs(delta_y)

        if overlap_x > overlap_y:
            # Вертикальное столкновение (Y)
            penetration_depth = overlap_y / 2 + 1  # +1 пиксель, чтобы избежать повторного залипания
            if self.y > other.y:
                self.y += penetration_depth
                other.y -= penetration_depth
            else:
                self.y -= penetration_depth
                other.y += penetration_depth

            # Разделяем скорости только по Y
            self.velocity_y, other.velocity_y = other.velocity_y, self.velocity_y

        else:
            # Горизонтальное столкновение (X)
            penetration_depth = overlap_x / 2 + 1
            if self.x > other.x:
                self.x += penetration_depth
                other.x -= penetration_depth
            else:
                self.x -= penetration_depth
                other.x += penetration_depth

            # Разделяем скорости только по X
            self.velocity_x, other.velocity_x = other.velocity_x, self.velocity_x

        # Проверяем столкновение с границами ещё раз, если объект прижался к стене
        self.correct_wall_collision()
        other.correct_wall_collision()

    def correct_wall_collision(self):
        """ Исправляет возможное застревание объекта в стене """
        if self.x + self.half_size > self.field.half_size:
            self.x = self.field.half_size - self.half_size
            self.velocity_x *= -1

        if self.x - self.half_size < -self.field.half_size:
            self.x = -self.field.half_size + self.half_size
            self.velocity_x *= -1

        if self.y + self.half_size > self.field.half_size:
            self.y = self.field.half_size - self.half_size
            self.velocity_y *= -1

        if self.y - self.half_size < -self.field.half_size:
            self.y = -self.field.half_size + self.half_size
            self.velocity_y *= -1

    def draw(self):
        """ Рисует NPC """
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f((self.x - self.half_size) / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)
        glVertex2f((self.x + self.half_size) / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)
        glVertex2f((self.x + self.half_size) / self.field.screen_width, (self.y + self.half_size) / self.field.screen_height)
        glVertex2f((self.x - self.half_size) / self.field.screen_width, (self.y + self.half_size) / self.field.screen_height)
        glEnd()

        # Рисуем шипы, если они есть
        if self.has_spikes:
            glColor3f(0.5, 0.5, 0.5)  # Серый цвет шипов
            glBegin(GL_TRIANGLES)
            glVertex2f(self.x / self.field.screen_width, (self.y + self.half_size) / self.field.screen_height)  # Верхний угол
            glVertex2f((self.x - self.half_size) / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)  # Левый угол
            glVertex2f((self.x + self.half_size) / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)  # Правый угол
            glEnd()
