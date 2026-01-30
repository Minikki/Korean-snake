#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска игры Clever Snake
"""

import sys
import os

# Настройка кодировки для поддержки корейских символов
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Устанавливаем кодировку консоли в UTF-8
    try:
        import subprocess
        subprocess.run(['chcp', '65001'], shell=True, capture_output=True)
    except:
        pass

def check_pygame():
    """Проверяет, установлен ли pygame"""
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} установлен")
        return True
    except ImportError:
        print("✗ Pygame не установлен")
        print("Установите pygame командой: pip install pygame")
        return False

def check_korean_fonts():
    """Проверяет доступность корейских шрифтов"""
    try:
        import pygame
        pygame.font.init()
        
        # Проверяем системный шрифт
        test_font = pygame.font.Font(None, 12)
        test_surface = test_font.render("한글", True, (255, 255, 255))
        
        if test_surface.get_width() > 0:
            print("✓ Корейские шрифты доступны")
            return True
        else:
            print("⚠ Корейские шрифты не найдены")
            print("Для корректного отображения корейских символов установите корейские шрифты")
            print("Подробные инструкции: python check_korean_fonts.py")
            return False
    except Exception as e:
        print(f"⚠ Ошибка при проверке корейских шрифтов: {e}")
        return False

def main():
    """Главная функция"""
    print("Clever Snake")
    print("=" * 40)
    
    # Проверяем pygame
    if not check_pygame():
        sys.exit(1)
    
    # Проверяем корейские шрифты
    check_korean_fonts()
    
    # Проверяем наличие основного файла игры
    if not os.path.exists("snake_game.py"):
        print("✗ Файл snake_game.py не найден")
        print("Убедитесь, что вы находитесь в правильной директории")
        sys.exit(1)
    
    print("✓ Файл игры найден")
    print("Запуск игры...")
    print()
    
    # Запускаем игру
    try:
        import snake_game
    except Exception as e:
        print(f"✗ Ошибка при запуске игры: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
