@echo off
chcp 65001 >nul
echo Clever Snake
echo ========================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не найден
    echo Установите Python с https://python.org
    pause
    exit /b 1
)

REM Проверяем наличие pygame
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Pygame не установлен. Устанавливаем...
    pip install pygame
    if errorlevel 1 (
        echo Ошибка при установке pygame
        pause
        exit /b 1
    )
)

REM Запускаем игру
echo Запуск игры...
python snake_game.py

pause
