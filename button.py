import pygame


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text  # Текст кнопки
        self.x = x  # Позиция х кнопки
        self.y = y  # Позиция у кнопки
        self.w = w  # Ширина кнопки
        self.h = h  # Высота кнопки

    def create_button(self, surface, font, color):
        """Создает кнопку на экране"""
        pygame.draw.rect(surface, color, (self.x, self.y, self.w, self.h), 1)
        surface.blit(font.render(self.text, 1, color), (self.x, self.y))


if __name__ == "__main__":
    print("This module is not for direct call!")