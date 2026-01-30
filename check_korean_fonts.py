#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки и установки корейских шрифтов
"""

import pygame
import sys
import os
import platform

def check_korean_fonts():
    """Проверяет доступность корейских шрифтов"""
    print("Проверка корейских шрифтов...")
    
    pygame.font.init()
    
    # Список корейских шрифтов для проверки
    korean_fonts = [
        "Malgun Gothic",
        "맑은 고딕", 
        "Gulim",
        "굴림",
        "Dotum",
        "돋움",
        "Batang",
        "바탕",
        "Arial Unicode MS",
        "Noto Sans CJK KR",
        "AppleGothic"
    ]
    
    available_fonts = []
    
    for font_name in korean_fonts:
        try:
            font = pygame.font.Font(font_name, 12)
            test_surface = font.render("한글", True, (255, 255, 255))
            if test_surface.get_width() > 0:
                available_fonts.append(font_name)
                print(f"✓ {font_name} - доступен")
            else:
                print(f"✗ {font_name} - недоступен")
        except:
            print(f"✗ {font_name} - недоступен")
    
    # Проверяем системный шрифт
    try:
        system_font = pygame.font.Font(None, 12)
        test_surface = system_font.render("한글", True, (255, 255, 255))
        if test_surface.get_width() > 0:
            available_fonts.append("System Font")
            print("✓ System Font - поддерживает корейские символы")
        else:
            print("✗ System Font - не поддерживает корейские символы")
    except:
        print("✗ System Font - ошибка при проверке")
    
    return available_fonts

def get_installation_instructions():
    """Возвращает инструкции по установке для текущей ОС"""
    system = platform.system().lower()
    
    if system == "windows":
        return """
Для Windows:
1. Откройте Settings → Time & Language → Language
2. Нажмите Add a language
3. Найдите и выберите 한국어 (Korean)
4. Установите языковой пакет
5. Перезагрузите компьютер

Альтернативно:
1. Скачайте Noto Sans CJK KR с https://fonts.google.com/noto/specimen/Noto+Sans+KR
2. Установите файлы .ttf в C:\\Windows\\Fonts\\
"""
    elif system == "darwin":  # macOS
        return """
Для macOS:
1. Откройте System Preferences → Language & Region
2. Нажмите + и добавьте 한국어
3. Перезагрузите компьютер

Альтернативно:
1. Скачайте Noto Sans CJK KR с https://fonts.google.com/noto/specimen/Noto+Sans+KR
2. Дважды кликните на файлы .ttf и нажмите Install Font
"""
    else:  # Linux
        return """
Для Linux (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install fonts-nanum fonts-nanum-coding

Для Linux (CentOS/RHEL/Fedora):
sudo yum install google-noto-cjk-fonts  # CentOS/RHEL
sudo dnf install google-noto-cjk-fonts  # Fedora
"""

def main():
    """Главная функция"""
    print("Clever Snake - Проверка корейских шрифтов")
    print("=" * 50)
    
    # Проверяем pygame
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} установлен")
    except ImportError:
        print("✗ Pygame не установлен")
        print("Установите pygame: pip install pygame")
        sys.exit(1)
    
    # Проверяем корейские шрифты
    available_fonts = check_korean_fonts()
    
    print("\n" + "=" * 50)
    
    if available_fonts:
        print(f"✓ Найдено {len(available_fonts)} корейских шрифтов:")
        for font in available_fonts:
            print(f"  - {font}")
        print("\nКорейские символы должны отображаться корректно в игре!")
    else:
        print("✗ Корейские шрифты не найдены")
        print("\nДля корректного отображения корейских символов установите корейские шрифты:")
        print(get_installation_instructions())
        print("После установки перезапустите этот скрипт для проверки.")
    
    print("\nДля запуска игры используйте: python snake_game.py")

if __name__ == "__main__":
    main()

