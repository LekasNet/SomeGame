import glfw
import time
import random
from OpenGL.GL import *

from objects import Field, NPC, generate_spawn_positions, HealthPack, AttackUpgrade, generate_powerup_position

from interface import HealthBar
from objects.npc import RAINBOW_COLORS

# Инициализация GLFW
if not glfw.init():
    raise Exception("GLFW не смог инициализироваться")

# Получаем размеры экрана
monitor = glfw.get_primary_monitor()
mode = glfw.get_video_mode(monitor)
screen_width, screen_height = mode.size

# Создаём полноэкранное окно
window = glfw.create_window(screen_width, screen_height, "OpenGL Fullscreen", monitor, None)
if not window:
    glfw.terminate()
    raise Exception("Не удалось создать окно")

glfw.make_context_current(window)

# Создаём объекты игрового мира
field = Field(screen_width, screen_height)
# Создаём UI для здоровья
health_bar = HealthBar(field)

# Количество NPC
num_npcs = 5
npc_size = 200
speed = 10

# Генерируем позиции для NPC
spawn_positions = generate_spawn_positions(field, npc_size, num_npcs)

# Создаём NPC в корректных местах с цветами из радуги
npcs = [NPC(field, x, y, size=npc_size, mode=1, speed=speed, color=RAINBOW_COLORS[i % len(RAINBOW_COLORS)]) for i, (x, y) in enumerate(spawn_positions)]

field.npcs = npcs  # Добавляем NPC в поле, чтобы PowerUps могли обращаться к ним

# Список активных PowerUps
powerups = []
last_spawn_time = time.time()  # Время последнего спавна бонуса

# Обработчик клавиш
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

glfw.set_key_callback(window, key_callback)

# Основной игровой цикл
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)

    for npc in npcs:
        npc.update(npcs)

    # Спавн PowerUp'ов раз в 5–10 секунд
    current_time = time.time()
    if current_time - last_spawn_time > random.uniform(5, 10):
        x, y = generate_powerup_position(field, npcs)
        if x is not None and y is not None:
            powerups.append(HealthPack(field, x, y) if random.random() < 0.25 else AttackUpgrade(field, x, y))
        last_spawn_time = current_time  # Обновляем таймер спавна

    for powerup in powerups:
        powerup.update(npcs)

    # Удаляем мёртвых NPC
    npcs = [npc for npc in npcs if npc.health > 0]

    # Проверяем, если остался 1 NPC → останавливаем его
    if len(npcs) == 1:
        npcs[0].mode = 0

    field.draw()

    for npc in npcs:
        npc.draw()

    health_bar.draw_all(npcs)  # Теперь рисуем все полоски разом

    for powerup in powerups:
        powerup.draw()

    glfw.swap_buffers(window)
    glfw.poll_events()

    time.sleep(1 / 60)

glfw.terminate()
