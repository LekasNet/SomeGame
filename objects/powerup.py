import random
from OpenGL.GL import *

class PowerUp:
    """Базовый класс для бонусов"""
    def __init__(self, field, x, y, size=50):
        self.field = field  # Теперь PowerUp знает размеры игрового поля
        self.x = x
        self.y = y
        self.size = size
        self.half_size = size / 2
        self.active = True

    def apply_effect(self, npc):
        pass

    def update(self, npcs):
        """ Проверяет, был ли бонус подобран NPC """
        if not self.active:
            return

        for npc in npcs:
            if self.check_collision(npc):
                self.apply_effect(npc)
                self.active = False

    def check_collision(self, npc):
        """ Проверяет, пересекается ли бонус с NPC """
        return (
            abs(self.x - npc.x) < (self.half_size + npc.half_size) and
            abs(self.y - npc.y) < (self.half_size + npc.half_size)
        )


class HealthPack(PowerUp):
    """Добавляет 1 здоровье NPC"""
    def __init__(self, field, x, y, size=50):
        super().__init__(field, x, y, size)

    def apply_effect(self, npc):
        npc.health += 1  # Добавляем 1 HP

    def draw(self):
        """Рисует зелёный `+` с правильным масштабированием"""
        if not self.active:
            return

        glColor3f(0, 1, 0)  # Зелёный цвет
        glBegin(GL_LINES)
        # Горизонтальная линия `+`
        glVertex2f((self.x - self.half_size) / self.field.screen_width, self.y / self.field.screen_height)
        glVertex2f((self.x + self.half_size) / self.field.screen_width, self.y / self.field.screen_height)
        # Вертикальная линия `+`
        glVertex2f(self.x / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)
        glVertex2f(self.x / self.field.screen_width, (self.y + self.half_size) / self.field.screen_height)
        glEnd()


class AttackUpgrade(PowerUp):
    """Добавляет NPC шипы, которые наносят урон"""
    def __init__(self, field, x, y, size=50):
        super().__init__(field, x, y, size)

    def apply_effect(self, npc):
        """ Устанавливает шипы, удаляя их у других NPC """
        for other_npc in npc.field.npcs:
            other_npc.has_spikes = False  # Убираем шипы у всех NPC
        npc.has_spikes = True  # У этого NPC появляются шипы

    def draw(self):
        """Рисует серый шип (треугольник) с правильным масштабированием"""
        if not self.active:
            return

        glColor3f(0.5, 0.5, 0.5)  # Серый цвет
        glBegin(GL_TRIANGLES)
        # Верхний угол
        glVertex2f(self.x / self.field.screen_width, (self.y + self.half_size) / self.field.screen_height)
        # Левый угол
        glVertex2f((self.x - self.half_size) / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)
        # Правый угол
        glVertex2f((self.x + self.half_size) / self.field.screen_width, (self.y - self.half_size) / self.field.screen_height)
        glEnd()
