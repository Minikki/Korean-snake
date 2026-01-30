#!/bin/bash

echo "Clever Snake"
echo "========================================"
echo

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не найден"
    echo "Установите Python3"
    exit 1
fi

# Проверяем наличие pygame
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Pygame не установлен. Устанавливаем..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "Ошибка при установке pygame"
        exit 1
    fi
fi

# Запускаем игру
echo "Запуск игры..."
python3 snake_game.py
