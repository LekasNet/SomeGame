import random
import math


def generate_spawn_positions(field, npc_size, num_npcs, max_attempts=1000):
    """
    Генерирует список координат для спавна NPC без пересечений.

    :param field: Объект игрового поля
    :param npc_size: Размер NPC
    :param num_npcs: Количество NPC
    :param max_attempts: Количество попыток для корректного спавна
    :return: Список (x, y) для спавна NPC
    """
    half_size = field.half_size
    positions = []

    for _ in range(num_npcs):
        for _ in range(max_attempts):  # Попытки найти свободное место
            x = random.uniform(-half_size + npc_size, half_size - npc_size)
            y = random.uniform(-half_size + npc_size, half_size - npc_size)

            # Проверяем, не пересекается ли с уже существующими NPC
            if all(math.dist((x, y), (px, py)) >= npc_size * 1.1 for px, py in positions):
                positions.append((x, y))
                break  # Успешно найдено место

    return positions


def generate_powerup_position(field, npcs):
    """Возвращает точку, наиболее удалённую от всех NPC"""
    best_x, best_y = None, None
    max_distance = 0

    for _ in range(100):
        x = random.uniform(-field.half_size + 50, field.half_size - 50)
        y = random.uniform(-field.half_size + 50, field.half_size - 50)

        min_distance = min(math.dist((x, y), (npc.x, npc.y)) for npc in npcs)
        if min_distance > max_distance:
            max_distance = min_distance
            best_x, best_y = x, y

    return best_x, best_y