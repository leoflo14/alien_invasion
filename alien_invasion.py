import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.background = pygame.image.load("images/bg_image.jpg").convert()
        self.background = pygame.transform.scale(
            self.background, (self.settings.screen_width, self.settings.screen_height)
        )
        # начальные координаты двух фонов
        self.bg_y1 = 0
        self.bg_y2 = -self.settings.screen_height
        # скорость прокрутки
        self.bg_speed = self.settings.bg_speed

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self.ship.blitme()
            # двигаем фон
            self._update_background()
            # При каждом проходе цикла перерисовывается экран.
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()
        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        # рисуем два фона
        self.screen.blit(self.background, (0, self.bg_y1))
        self.screen.blit(self.background, (0, self.bg_y2))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    def _update_background(self):
        """Прокрутка фонового изображения."""
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        # если фон ушёл за экран — возвращаем наверх
        if self.bg_y1 >= self.settings.screen_height:
            self.bg_y1 = -self.settings.screen_height
        if self.bg_y2 >= self.settings.screen_height:
            self.bg_y2 = -self.settings.screen_height


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
