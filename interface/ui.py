from OpenGL.GL import *
import math

class HealthBar:
    """Полоска здоровья над полем"""

    def __init__(self, field, max_health=3, height=20, spacing=5, gap=30, corner_radius=10):
        self.field = field
        self.max_health = max_health  # Начальное здоровье NPC
        self.height = height  # Высота полоски
        self.spacing = spacing  # Расстояние между делениями
        self.gap = gap  # Расстояние между полосками разных NPC
        self.corner_radius = corner_radius  # Радиус закруглений

    def draw_all(self, npcs):
        """Рисует полоски здоровья для всех NPC"""
        if not npcs:
            return

        # Определяем диапазон от верхней границы поля до верхней границы экрана
        top_screen_y = self.field.screen_height / 2  # Верхняя граница экрана
        field_top_y = self.field.half_size  # Верхняя граница игрового поля

        # Увеличиваем расстояние между полосками NPC
        num_npcs = len(npcs)
        step_y = (top_screen_y - field_top_y) / (num_npcs + 1) + self.gap

        for index, npc in enumerate(npcs):
            if npc.health <= 0:
                continue  # Не рисуем, если здоровье 0

            # Вычисляем Y-позицию для каждой полоски с учетом gap
            y_pos = field_top_y + step_y * (index + 1)

            # Если HP больше стартового, уменьшаем ширину каждого блока
            effective_max_health = max(self.max_health, npc.health)  # Учитываем переполнение HP
            bar_width = self.field.size  # Полоска здоровья = ширина игрового поля
            segment_width = (bar_width - (effective_max_health - 1) * self.spacing) / effective_max_health

            start_x = -self.field.half_size  # Начало отрисовки по X

            for i in range(effective_max_health):
                if i < npc.health:
                    glColor3f(*npc.color)  # Полоска имеет цвет NPC
                else:
                    glColor3f(0.5, 0.5, 0.5)  # Серый (потерянное HP)

                # Рисуем закруглённый прямоугольник
                self.draw_rounded_rect(
                    x=start_x + i * (segment_width + self.spacing),
                    y=y_pos,
                    width=segment_width,
                    height=self.height,
                    radius=self.corner_radius
                )

    def draw_rounded_rect(self, x, y, width, height, radius):
        """Рисует закругленный прямоугольник"""
        num_segments = 10  # Количество сегментов для закруглений

        # Центральная часть (основной прямоугольник)
        glBegin(GL_QUADS)
        glVertex2f(x / self.field.half_size, y / self.field.screen_height)
        glVertex2f((x + width) / self.field.half_size, y / self.field.screen_height)
        glVertex2f((x + width) / self.field.half_size, (y + height) / self.field.screen_height)
        glVertex2f(x / self.field.half_size, (y + height) / self.field.screen_height)
        glEnd()

        # Рисуем закругленные углы
        glBegin(GL_TRIANGLE_FAN)
        for corner_x, corner_y in [
            (x + radius, y + radius),  # Левый нижний
            (x + width - radius, y + radius),  # Правый нижний
            (x + width - radius, y + height - radius),  # Правый верхний
            (x + radius, y + height - radius)  # Левый верхний
        ]:
            for i in range(num_segments + 1):
                angle = math.pi / 2 * i / num_segments
                offset_x = math.cos(angle) * radius
                offset_y = math.sin(angle) * radius
                glVertex2f((corner_x + offset_x) / self.field.half_size, (corner_y + offset_y) / self.field.screen_height)
        glEnd()
