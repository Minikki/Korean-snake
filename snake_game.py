#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clever Snake
Игра "Clever Snake" с тремя режимами игры и многоязычной поддержкой
"""

# Настройка кодировки для поддержки корейских символов
import sys
import os
if sys.platform.startswith('win'):
    # Для Windows устанавливаем кодировку UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import pygame
import random
import json
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any

# Инициализация Pygame
pygame.init()

# Настройка кодировки для корректного отображения корейских символов
import locale
try:
    locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Korean_Korea.949')
    except:
        pass  # Используем системную кодировку по умолчанию

# Настройка pygame для поддержки Unicode
pygame.font.init()

def setup_korean_fonts():
    """Настраивает корейские шрифты для всех платформ"""
    try:
        # Пробуем разные способы проверки корейских шрифтов
        test_fonts = []
        
        # Пробуем системный шрифт через SysFont
        try:
            test_fonts.append(pygame.font.SysFont(None, 12))
        except:
            pass
        
        # Пробуем системный шрифт через Font
        try:
            test_fonts.append(pygame.font.Font(None, 12))
        except:
            pass
        
        # Проверяем каждый доступный шрифт
        korean_supported = False
        for test_font in test_fonts:
            try:
                test_surface = test_font.render("한글", True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    korean_supported = True
                    break
            except:
                continue

        if not korean_supported:
            # Корейские символы не поддерживаются, выводим предупреждение
            print("⚠ Предупреждение: Корейские шрифты не найдены на системе.")
            print("Для корректного отображения корейских символов установите:")
            print("- Windows: Korean Language Pack")
            print("- macOS: Korean fonts через System Preferences")
            print("- Linux: sudo apt-get install fonts-nanum fonts-noto-cjk")
            return False
        else:
            print("✓ Корейские шрифты доступны")
        return True
    except Exception as e:
        print(f"⚠ Ошибка при настройке корейских шрифтов: {e}")
        print("Попробуйте установить корейские шрифты вручную")
        return False

# Инициализация корейских шрифтов
setup_korean_fonts()

# Список корейских шрифтов для корректного отображения
KOREAN_FONTS = [
    # Windows шрифты
    "Malgun Gothic",  # Windows 10/11
    "맑은 고딕",  # Korean name
    "Gulim",  # Windows Korean font
    "굴림",  # Korean name
    "Dotum",  # Windows Korean font
    "돋움",  # Korean name
    "Batang",  # Windows Korean font
    "바탕",  # Korean name
    "Arial Unicode MS",  # Cross-platform
    # Linux шрифты
    "Noto Sans CJK KR",  # Google Noto font (Linux)
    "Nanum Gothic",  # Linux Korean font
    "NanumBarunGothic",  # Linux Korean font
    "Nanum Myeongjo",  # Linux Korean font
    "DejaVu Sans",  # Linux fallback
    "Liberation Sans",  # Linux fallback
    # macOS шрифты
    "AppleGothic",  # macOS
    "Apple SD Gothic Neo",  # macOS
    # Общие fallback
    "Helvetica",  # Fallback
    "Arial"  # Fallback
]

def get_korean_font(size):
    """Получает шрифт с поддержкой корейских символов"""
    # Сначала пробуем использовать SysFont для лучшей поддержки системных шрифтов
    for font_name in KOREAN_FONTS:
        try:
            # Используем SysFont вместо Font для лучшей поддержки системных шрифтов
            font = pygame.font.SysFont(font_name, size)
            # Проверяем, поддерживает ли шрифт корейские символы
            test_surface = font.render("한글", True, (255, 255, 255))
            if test_surface.get_width() > 0:
                return font
        except:
            try:
                # Пробуем также через Font
                font = pygame.font.Font(font_name, size)
                test_surface = font.render("한글", True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    return font
            except:
                continue

    # Пробуем найти корейские шрифты в списке доступных системных шрифтов
    try:
        available_fonts = pygame.font.get_fonts()
        # Ищем шрифты, которые могут содержать корейские символы
        korean_keywords = ['nanum', 'noto', 'malgun', 'gulim', 'dotum', 'batang', 'gothic', 'arial']
        for font_name in available_fonts:
            if any(keyword in font_name.lower() for keyword in korean_keywords):
                try:
                    font = pygame.font.SysFont(font_name, size)
                    test_surface = font.render("한글", True, (255, 255, 255))
                    if test_surface.get_width() > 0:
                        return font
                except:
                    continue
    except:
        pass

    # Пробуем системный шрифт через SysFont
    try:
        system_font = pygame.font.SysFont(None, size)
        test_surface = system_font.render("한글", True, (255, 255, 255))
        if test_surface.get_width() > 0:
            return system_font
    except:
        pass

    # Пробуем системный шрифт через Font
    try:
        system_font = pygame.font.Font(None, size)
        test_surface = system_font.render("한글", True, (255, 255, 255))
        if test_surface.get_width() > 0:
            return system_font
    except:
        pass

    # В крайнем случае используем системный шрифт без проверки
    try:
        return pygame.font.SysFont(None, size)
    except:
        return pygame.font.Font(None, size)

# Константы
RESOLUTIONS = {
    "800x600": (800, 600),
    "1000x700": (1000, 700),
    "1200x800": (1200, 800),
    "1366x768": (1366, 768),
    "1920x1080": (1920, 1080)
}

DEFAULT_RESOLUTION = "1000x700"
WINDOW_WIDTH, WINDOW_HEIGHT = RESOLUTIONS[DEFAULT_RESOLUTION]
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 150, 0)

class GameMode(Enum):
    CLASSIC = 1
    QUIZ = 2
    WORD_COLLECTION = 3

class Language(Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"
    KOREAN = "ko"

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Localization:
    def __init__(self):
        self.current_lang = Language.RUSSIAN
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Загружает переводы из файла локализации"""
        translations = {
            "ru": {
                "title": "Clever Snake",
                "classic_mode": "Классическая змейка",
                "quiz_mode": "Викторина",
                "word_mode": "Змейка со словами",
                "play": "Играть",
                "settings": "Настройки",
                "exit": "Выход",
                "score": "Счет",
                "pause": "Пауза",
                "resume": "Продолжить",
                "game_over": "Игра окончена",
                "final_score": "Финальный счет",
                "restart": "Перезапустить",
                "back_to_menu": "В главное меню",
                "language": "Язык",
                "interface_lang": "Язык интерфейса",
                "game_lang": "Язык игры",
                "resolution": "Разрешение экрана",
                "question": "Вопрос",
                "answer": "Ответ",
                "correct": "Правильно!",
                "wrong": "Неправильно!",
                "collect_word": "Соберите слово",
                "word": "Слово",
                "controls": "Управление",
                "up": "Вверх - W",
                "down": "Вниз - S",
                "left": "Влево - A",
                "right": "Вправо - D",
                "pause_key": "Пауза - C",
                "resume_key": "Продолжить - V",
                "quit_key": "Выход - Q"
            },
            "en": {
                "title": "Clever Snake",
                "classic_mode": "Classic Snake",
                "quiz_mode": "Quiz",
                "word_mode": "Snake with Words",
                "play": "Play",
                "settings": "Settings",
                "exit": "Exit",
                "score": "Score",
                "pause": "Pause",
                "resume": "Resume",
                "game_over": "Game Over",
                "final_score": "Final Score",
                "restart": "Restart",
                "back_to_menu": "Back to Menu",
                "language": "Language",
                "interface_lang": "Interface Language",
                "game_lang": "Game Language",
                "resolution": "Screen Resolution",
                "question": "Question",
                "answer": "Answer",
                "correct": "Correct!",
                "wrong": "Wrong!",
                "collect_word": "Collect the word",
                "word": "Word",
                "controls": "Controls",
                "up": "Up - W",
                "down": "Down - S",
                "left": "Left - A",
                "right": "Right - D",
                "pause_key": "Pause - C",
                "resume_key": "Resume - V",
                "quit_key": "Quit - Q"
            },
            "ko": {
                "title": "클리버 스네이크",
                "classic_mode": "클래식 뱀",
                "quiz_mode": "퀴즈",
                "word_mode": "단어 뱀",
                "play": "플레이",
                "settings": "설정",
                "exit": "종료",
                "score": "점수",
                "pause": "일시정지",
                "resume": "계속",
                "game_over": "게임 오버",
                "final_score": "최종 점수",
                "restart": "다시 시작",
                "back_to_menu": "메뉴로 돌아가기",
                "language": "언어",
                "interface_lang": "인터페이스 언어",
                "game_lang": "게임 언어",
                "resolution": "화면 해상도",
                "question": "문제",
                "answer": "답",
                "correct": "정답!",
                "wrong": "오답!",
                "collect_word": "단어를 모으세요",
                "word": "단어",
                "controls": "조작법",
                "up": "위 - W",
                "down": "아래 - S",
                "left": "왼쪽 - A",
                "right": "오른쪽 - D",
                "pause_key": "일시정지 - C",
                "resume_key": "계속 - V",
                "quit_key": "종료 - Q"
            }
        }
        return translations

    def get_text(self, key: str) -> str:
        """Получает переведенный текст"""
        return self.translations.get(self.current_lang.value, {}).get(key, key)

    def set_language(self, lang: Language):
        """Устанавливает язык"""
        self.current_lang = lang

class Snake:
    def __init__(self, x: int, y: int, grid_width: int, grid_height: int):
        self.body = [(x, y)]
        self.direction = Direction.RIGHT
        self.grow_pending = False
        self.grid_width = grid_width
        self.grid_height = grid_height

    def move(self):
        """Двигает змейку"""
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        # Проверка выхода за границы (телепортация) — используем размеры текущего поля
        new_head = (new_head[0] % self.grid_width, new_head[1] % self.grid_height)

        self.body.insert(0, new_head)

        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        """Увеличивает змейку"""
        self.grow_pending = True

    def change_direction(self, new_direction: Direction):
        """Изменяет направление змейки"""
        # Предотвращает движение в противоположном направлении
        if (self.direction == Direction.UP and new_direction == Direction.DOWN) or \
           (self.direction == Direction.DOWN and new_direction == Direction.UP) or \
           (self.direction == Direction.LEFT and new_direction == Direction.RIGHT) or \
           (self.direction == Direction.RIGHT and new_direction == Direction.LEFT):
            return
        self.direction = new_direction

    def check_collision(self) -> bool:
        """Проверяет столкновение с собой"""
        head = self.body[0]
        return head in self.body[1:]

    def draw(self, screen: pygame.Surface):
        """Отрисовывает змейку"""
        for i, (x, y) in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

class Apple:
    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.generate_position()
        self.color = RED

    def generate_position(self) -> Tuple[int, int]:
        """Генерирует случайную позицию для яблока"""
        return (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))

    def respawn(self, snake_body: List[Tuple[int, int]]):
        """Перемещает яблоко в новую позицию"""
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break

    def draw(self, screen: pygame.Surface):
        """Отрисовывает яблоко"""
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

class QuizApple(Apple):
    def __init__(self, grid_width: int, grid_height: int, question: str, correct_answer: str, wrong_answers: List[str], answer_number: int):
        super().__init__(grid_width, grid_height)
        self.question = question
        self.correct_answer = correct_answer
        self.wrong_answers = wrong_answers
        self.answer_number = answer_number  # Номер ответа (1, 2, 3, 4)
        self.color = RED  # Все яблоки красные

    def get_answers(self) -> List[str]:
        """Возвращает перемешанные ответы"""
        answers = [self.correct_answer] + self.wrong_answers
        random.shuffle(answers)
        return answers

    def draw(self, screen: pygame.Surface):
        """Отрисовывает яблоко с номером ответа"""
        super().draw(screen)
        font = get_korean_font(24)
        text = font.render(str(self.answer_number), True, WHITE)
        text_rect = text.get_rect(center=(self.position[0] * GRID_SIZE + GRID_SIZE // 2,
                                        self.position[1] * GRID_SIZE + GRID_SIZE // 2))
        screen.blit(text, text_rect)

class WordApple(Apple):
    def __init__(self, grid_width: int, grid_height: int, letter: str, is_correct: bool = False):
        super().__init__(grid_width, grid_height)
        self.letter = letter
        self.is_correct = is_correct
        self.color = RED  # Все яблоки одного цвета, чтобы не выдавать правильную букву

    def draw(self, screen: pygame.Surface):
        """Отрисовывает яблоко с буквой"""
        super().draw(screen)
        font = get_korean_font(24)
        text = font.render(self.letter, True, WHITE)
        text_rect = text.get_rect(center=(self.position[0] * GRID_SIZE + GRID_SIZE // 2,
                                        self.position[1] * GRID_SIZE + GRID_SIZE // 2))
        screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.current_resolution = DEFAULT_RESOLUTION
        self.window_width, self.window_height = RESOLUTIONS[self.current_resolution]
        self.grid_width = self.window_width // GRID_SIZE
        self.grid_height = self.window_height // GRID_SIZE
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Clever Snake")
        self.clock = pygame.time.Clock()
        self.localization = Localization()
        self.interface_lang = Language.RUSSIAN
        self.game_lang = Language.RUSSIAN
        self.running = True
        self.current_screen = "menu"
        self.game_mode = None
        self.snake = None
        self.apple = None
        self.score = 0
        self.paused = False
        self.quiz_questions = self._load_quiz_questions()
        self.word_targets = self._load_word_targets()
        self.current_word = ""  # Слово на языке интерфейса (для отображения)
        self.current_word_game_lang = ""  # Слово на языке игры (для сбора букв)
        self.collected_letters = []
        self.quiz_question = None
        self.quiz_answers = []
        self.quiz_correct_answer = ""
        self.quiz_correct_number = 0  # Номер правильного ответа
        self.quiz_apples = []  # Список яблок с номерами ответов
        self.word_apples: List[WordApple] = [] # Список яблок для режима сбора слов
        self.quiz_result = None
        self.quiz_result_timer = 0
        self.used_questions = []  # Список использованных вопросов
        self.quiz_completed = False  # Флаг завершения викторины

    def change_resolution(self, resolution: str):
        """Изменяет разрешение экрана"""
        if resolution in RESOLUTIONS:
            self.current_resolution = resolution
            self.window_width, self.window_height = RESOLUTIONS[resolution]
            self.grid_width = self.window_width // GRID_SIZE
            self.grid_height = self.window_height // GRID_SIZE
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))
            return True
        return False

    def _load_quiz_questions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Загружает вопросы для викторины"""
        return {
            "ru": [
                # Вопросы о Южной Корее
                {"question": "Как называется главный флаг Южной Кореи?", "correct": "Тхэгыкки", "wrong": ["Восходящее Солнце", "Четыре Дракона", "Звезда и Полумесяц"]},
                {"question": "Какой цветок является национальным символом Кореи?", "correct": "Мугунхва (Гибискус)", "wrong": ["Сакура (Вишня)", "Лотос", "Роза"]},
                {"question": "Какое животное считается священным в корейских мифах?", "correct": "Дракон/Тигр", "wrong": ["Единорог", "Змея", "Феникс"]},
                {"question": "Как называется традиционная корейская одежда?", "correct": "Ханбок", "wrong": ["Кимоно", "Кипао", "Сари"]},
                {"question": "Какой большой азиатский праздник отмечается осенью в честь сбора урожая?", "correct": "Чхусок", "wrong": ["Соллаль", "Дивали", "Тет"]},
                {"question": "Как называется традиционное корейское боевое искусство?", "correct": "Тхэквондо", "wrong": ["Каратэ", "Кунг-фу", "Айкидо"]},
                {"question": "Как называется корейский алфавит?", "correct": "Хангыль", "wrong": ["Кандзи", "Кириллица", "Иероглифы"]},
                {"question": "Какое самое известное острое блюдо из ферментированной капусты?", "correct": "Кимчи", "wrong": ["Рамен", "Суши", "Пульгоги"]},
                {"question": "Как называется популярное корейское блюдо из риса, мяса, овощей и острого соуса?", "correct": "Бибимбап", "wrong": ["Кимбап", "Чапчхэ", "Ттокпокки"]},
                {"question": "Как называют корейские сериалы?", "correct": "Дорамы", "wrong": ["Аниме", "Теленовеллы", "Ситкомы"]},

                # Вопросы об Англии
                {"question": "Как называется знаменитый дворец в Лондоне, где живет король?", "correct": "Букингемский дворец", "wrong": ["Версаль", "Тауэр", "Виндзорский замок"]},
                {"question": "Как называется самая известная достопримечательность Лондона — большая башня с часами?", "correct": "Биг-Бен (Башня Елизаветы)", "wrong": ["Эмпайр-стейт-билдинг", "Вестминстер", "Пизанская башня"]},
                {"question": "Какое животное является национальным символом Англии?", "correct": "Лев", "wrong": ["Орел", "Бык", "Барсук"]},
                {"question": "Как называется красный автобус с двумя этажами, который можно увидеть в Лондоне?", "correct": "Даблдекер", "wrong": ["Трамвай", "Метро", "Минивэн"]},
                {"question": "Какое самое известное блюдо из жареной рыбы и картошки?", "correct": "Фиш энд чипс", "wrong": ["Пицца", "Гамбургер", "Плов"]},
                {"question": "Как называется традиционный английский напиток, который англичане пьют с молоком?", "correct": "Чай", "wrong": ["Кофе", "Сок", "Лимонад"]},
                {"question": "Как называется древнее сооружение из камней, расположенное на равнине?", "correct": "Стоунхендж", "wrong": ["Пирамиды", "Колизей", "Мачу-Пикчу"]},
                {"question": "Какой сказочный король собрал вокруг себя рыцарей Круглого стола?", "correct": "Король Артур", "wrong": ["Король Ричард", "Король Лир", "Король Генрих"]},
                {"question": "Какой вид спорта очень популярен в Англии?", "correct": "Футбол", "wrong": ["Баскетбол", "Бейсбол", "Крикет"]},
                {"question": "Какую фразу говорят, чтобы пожелать кому-то удачи перед представлением?", "correct": "Break a leg!", "wrong": ["Good luck!", "Nice to meet you!", "See you later!"]},

                # Вопросы о России
                {"question": "Какое животное является одним из самых известных национальных символов России?", "correct": "Медведь", "wrong": ["Волк", "Лиса", "Олень"]},
                {"question": "Какой самый большой город и столица России?", "correct": "Москва", "wrong": ["Санкт-Петербург", "Киев", "Казань"]},
                {"question": "Как называется самая длинная река в Европе, которая протекает через Россию?", "correct": "Волга", "wrong": ["Дон", "Нева", "Обь"]},
                {"question": "Как называется всемирно известный архитектурный комплекс в Москве, окруженный стенами?", "correct": "Кремль", "wrong": ["Эрмитаж", "Зимний Дворец", "Большой театр"]},
                {"question": "Как называются расписные деревянные куклы, вложенные одна в другую?", "correct": "Матрешка", "wrong": ["Неваляшка", "Буратино", "Дымковская игрушка"]},
                {"question": "Какой вид транспорта на тройке лошадей был популярен для зимних путешествий?", "correct": "Тройка (Санки)", "wrong": ["Карета", "Плот", "Дирижабль"]},
                {"question": "Как называется традиционный русский суп из капусты и мяса?", "correct": "Щи", "wrong": ["Борщ", "Рассольник", "Уха"]},
                {"question": "Как называются тонкие, круглые лепешки, которые часто едят со сметаной, вареньем или икрой?", "correct": "Блины", "wrong": ["Оладьи", "Пышки", "Лаваш"]},
                {"question": "Как называется холодный летний суп, который готовят на квасе?", "correct": "Окрошка", "wrong": ["Гаспачо", "Свекольник", "Холодник"]},
                {"question": "Какой сказочный персонаж умеет летать в ступе и живет в избушке на курьих ножках?", "correct": "Баба-Яга", "wrong": ["Кощей Бессмертный", "Змей Горыныч", "Леший"]},
                {"question": "Как зовут девушку, которая помогает Деду Морозу и всегда одета в голубое или белое?", "correct": "Снегурочка", "wrong": ["Аленушка", "Василиса", "Снежная Королева"]},
                {"question": "Какой музыкальный инструмент, похожий на треугольник, является символом русской народной музыки?", "correct": "Балалайка", "wrong": ["Гусли", "Гармонь", "Домра"]}
            ],
            "en": [
                # South Korea Questions
                {"question": "What is the name of South Korea's main flag?", "correct": "Taegukgi", "wrong": ["Rising Sun", "Four Dragons", "Star and Crescent"]},
                {"question": "What flower is the national symbol of Korea?", "correct": "Mugunghwa (Rose of Sharon)", "wrong": ["Cherry Blossom (Sakura)", "Lotus", "Rose"]},
                {"question": "Which animal is considered sacred or symbolic in Korean myths?", "correct": "Dragon/Tiger", "wrong": ["Unicorn", "Snake", "Phoenix"]},
                {"question": "What is the name of the traditional Korean clothing with bright colors and full skirts?", "correct": "Hanbok", "wrong": ["Kimono", "Qipao", "Sari"]},
                {"question": "What major Asian holiday is celebrated in the autumn to give thanks for the harvest?", "correct": "Chuseok", "wrong": ["Seollal", "Diwali", "Tet"]},
                {"question": "What is the name of the traditional Korean martial art that involves a lot of kicking?", "correct": "Taekwondo", "wrong": ["Karate", "Kung Fu", "Aikido"]},
                {"question": "What is the Korean alphabet called that looks like circles, squares, and sticks?", "correct": "Hangeul", "wrong": ["Kanji", "Cyrillic", "Hieroglyphs"]},
                {"question": "What is the most famous spicy dish made of fermented cabbage, eaten with almost every meal?", "correct": "Kimchi", "wrong": ["Ramen", "Sushi", "Bulgogi"]},
                {"question": "What is the popular Korean dish of rice, meat, vegetables, and spicy sauce served in a bowl?", "correct": "Bibimbap", "wrong": ["Gimbap", "Japchae", "Tteokbokki"]},
                {"question": "What are Korean TV series called?", "correct": "Dramas", "wrong": ["Anime", "Telenovelas", "Sitcoms"]},

                # England Questions
                {"question": "What is the name of the famous palace in London where the King lives?", "correct": "Buckingham Palace", "wrong": ["Versailles", "The Tower", "Windsor Castle"]},
                {"question": "What is the most famous landmark in London — the large clock tower?", "correct": "Big Ben (Elizabeth Tower)", "wrong": ["Empire State Building", "Westminster", "Leaning Tower of Pisa"]},
                {"question": "Which animal is the national symbol of England, often shown on coats of arms?", "correct": "Lion", "wrong": ["Eagle", "Bull", "Badger"]},
                {"question": "What is the name of the red, two-story bus seen in London?", "correct": "Double-decker", "wrong": ["Tram", "Subway", "Minivan"]},
                {"question": "What is the most famous dish of deep-fried fish and potatoes, traditionally wrapped in newspaper?", "correct": "Fish and Chips", "wrong": ["Pizza", "Hamburger", "Pilaf"]},
                {"question": "What is the traditional English drink that people often drink with milk?", "correct": "Tea", "wrong": ["Coffee", "Juice", "Lemonade"]},
                {"question": "What is the name of the ancient stone structure located on a plain with many legends about it?", "correct": "Stonehenge", "wrong": ["The Pyramids", "The Colosseum", "Machu Picchu"]},
                {"question": "What legendary king, according to legends, gathered knights of the Round Table around him?", "correct": "King Arthur", "wrong": ["King Richard", "King Lear", "King Henry"]},
                {"question": "What sport, played with feet and a ball, is very popular in England?", "correct": "Football", "wrong": ["Basketball", "Baseball", "Cricket"]},
                {"question": "What phrase is said to wish someone good luck before a performance?", "correct": "Break a leg!", "wrong": ["Good luck!", "Nice to meet you!", "See you later!"]},

                # Russia Questions
                {"question": "Which animal is one of the most famous national symbols of Russia?", "correct": "Bear", "wrong": ["Wolf", "Fox", "Deer"]},
                {"question": "What is the largest city and capital of Russia?", "correct": "Moscow", "wrong": ["St. Petersburg", "Kyiv", "Kazan"]},
                {"question": "What is the longest river in Europe that flows through Russia?", "correct": "Volga", "wrong": ["Don", "Neva", "Ob"]},
                {"question": "What is the world-famous architectural complex in Moscow, surrounded by walls?", "correct": "The Kremlin", "wrong": ["The Hermitage", "The Winter Palace", "The Bolshoi Theatre"]},
                {"question": "What are the painted wooden dolls, nested one inside the other, called?", "correct": "Matryoshka", "wrong": ["Tumbler doll", "Pinocchio", "Dymkovo toy"]},
                {"question": "What is the three-horse sled that was popular for winter travel called?", "correct": "Troika (Sled)", "wrong": ["Carriage", "Raft", "Airship"]},
                {"question": "What is the traditional Russian soup made of cabbage and meat?", "correct": "Shchi", "wrong": ["Borsch", "Rassolnik", "Ukha"]},
                {"question": "What are the thin, round pancakes often eaten with sour cream, jam, or caviar called?", "correct": "Blini", "wrong": ["Oladyi", "Pyshki", "Lavash"]},
                {"question": "What is the cold summer soup made with kvass called?", "correct": "Okroshka", "wrong": ["Gazpacho", "Svekólnik", "Kholodnik"]},
                {"question": "What fairy tale character can fly in a mortar and lives in a hut on chicken legs?", "correct": "Baba Yaga", "wrong": ["Koschei the Deathless", "Zmey Gorynych", "Leshy"]},
                {"question": "What is the name of the girl who helps Ded Moroz and is always dressed in blue or white?", "correct": "Snegurochka", "wrong": ["Alyonushka", "Vasilisa", "The Snow Queen"]},
                {"question": "What musical instrument, shaped like a triangle, is a symbol of Russian folk music?", "correct": "Balalaika", "wrong": ["Gusli", "Garmon", "Domra"]}
            ],
            "ko": [
                # 한국 문화 질문
                {"question": "대한민국의 국기 이름은 무엇인가요?", "correct": "태극기", "wrong": ["떠오르는 태양", "네 마리의 용", "별과 초승달"]},
                {"question": "한국의 나라를 상징하는 꽃은 무엇인가요?", "correct": "무궁화", "wrong": ["벚꽃", "연꽃", "장미"]},
                {"question": "한국 신화에서 신성하거나 상징적인 동물은 무엇인가요?", "correct": "용/호랑이", "wrong": ["유니콘", "뱀", "불사조"]},
                {"question": "화려한 색상과 풍성한 치마가 있는 전통 한국 옷은 무엇이라고 부르나요?", "correct": "한복", "wrong": ["기모노", "치파오", "사리"]},
                {"question": "가을에 수확에 감사하며 기념하는 큰 명절은 무엇인가요?", "correct": "추석", "wrong": ["설날", "디왈리", "뗏"]},
                {"question": "발차기 동작이 많은 전통 한국 무술은 무엇인가요?", "correct": "태권도", "wrong": ["가라데", "쿵푸", "아이키도"]},
                {"question": "동그라미, 네모, 선 모양으로 이루어진 한국의 글자는 무엇인가요?", "correct": "한글", "wrong": ["한자", "키릴 문자", "상형 문자"]},
                {"question": "거의 모든 식사에 곁들여 먹는 발효된 양배추로 만든 가장 유명하고 매운 음식은 무엇인가요?", "correct": "김치", "wrong": ["라면", "초밥", "불고기"]},
                {"question": "밥, 고기, 채소, 매운 소스를 그릇에 담아 비벼 먹는 인기 있는 한국 음식은 무엇인가요?", "correct": "비빔밥", "wrong": ["김밥", "잡채", "떡볶이"]},
                {"question": "한국 TV 드라마 시리즈는 무엇이라고 부르나요?", "correct": "드라마", "wrong": ["애니메이션", "텔레노벨라", "시트콤"]},

                # 영국 문화 질문
                {"question": "런던에 있는 왕이 사는 유명한 궁궐의 이름은 무엇인가요?", "correct": "버킹엄 궁전", "wrong": ["베르사유", "타워", "윈저 성"]},
                {"question": "런던에서 가장 유명한 랜드마크인 큰 시계탑은 무엇이라고 부르나요?", "correct": "빅 벤", "wrong": ["엠파이어 스테이트 빌딩", "웨스트민스터", "피사의 사탑"]},
                {"question": "문장에 자주 등장하는, 영국을 상징하는 동물은 무엇인가요?", "correct": "사자", "wrong": ["독수리", "황소", "오소리"]},
                {"question": "런던에서 볼 수 있는 두 층짜리 빨간 버스는 무엇이라고 부르나요?", "correct": "이층 버스/더블데커", "wrong": ["전차", "지하철", "미니밴"]},
                {"question": "튀긴 생선과 감자로 만든, 전통적으로 신문에 싸서 먹던 가장 유명한 음식은 무엇인가요?", "correct": "피시 앤 칩스", "wrong": ["피자", "햄버거", "필라프"]},
                {"question": "영국 사람들이 우유와 함께 마시는 전통 음료는 무엇인가요?", "correct": "차", "wrong": ["커피", "주스", "레모네이드"]},
                {"question": "평원에 위치하며 많은 전설이 전해지는, 돌로 만들어진 고대 구조물은 무엇인가요?", "correct": "스톤헨지", "wrong": ["피라미드", "콜로세움", "마추픽추"]},
                {"question": "전설에 따르면 원탁의 기사들을 모았다고 하는 전설적인 왕은 누구인가요?", "correct": "아더 왕", "wrong": ["리처드 왕", "리어 왕", "헨리 왕"]},
                {"question": "발을 사용하여 공을 차는 스포츠로, 영국에서 매우 인기 있는 종목은 무엇인가요?", "correct": "축구", "wrong": ["농구", "야구", "크리켓"]},
                {"question": "공연 전에 누군가에게 행운을 빌어줄 때 하는 말은 무엇인가요?", "correct": "Break a leg!", "wrong": ["Good luck!", "Nice to meet you!", "See you later!"]},

                # 러시아 문화 질문
                {"question": "러시아의 가장 유명한 국가 상징 중 하나이며 동화에 자주 등장하는 동물은 무엇인가요?", "correct": "곰", "wrong": ["늑대", "여우", "사슴"]},
                {"question": "러시아의 가장 큰 도시이자 수도는 어디인가요?", "correct": "모스크바", "wrong": ["상트페테르부르크", "키이우", "카잔"]},
                {"question": "유럽을 가로질러 흐르는 가장 긴 강은 무엇인가요?", "correct": "볼가 강", "wrong": ["돈 강", "네바 강", "오브 강"]},
                {"question": "벽으로 둘러싸여 있으며 궁전과 성당이 있는 모스크바의 세계적으로 유명한 건축 단지는 무엇인가요?", "correct": "크렘린", "wrong": ["에르미타주", "겨울 궁전", "볼쇼이 극장"]},
                {"question": "가장 큰 것부터 가장 작은 것까지, 하나 안에 다른 인형들이 들어 있는 칠해진 나무 인형은 무엇이라고 부르나요?", "correct": "마트료시카", "wrong": ["오뚝이 인형", "피노키오", "딤코보 장난감"]},
                {"question": "세 마리 말이 끄는 썰매는 겨울철 여행에 인기 있는 운송 수단이었습니다. 이것을 무엇이라고 부르나요?", "correct": "트로이카/썰매", "wrong": ["마차", "뗏목", "비행선"]},
                {"question": "양배추와 고기로 만든 전통 러시아 수프는 무엇인가요?", "correct": "시", "wrong": ["보르시", "라솔니크", "우하"]},
                {"question": "사워 크림, 잼 또는 캐비어와 함께 자주 먹는 얇고 둥근 팬케이크는 무엇이라고 부르나요?", "correct": "블리니", "wrong": ["올라디", "푸시키", "라바시"]},
                {"question": "크바스(발효 음료)로 만드는 차가운 여름 수프는 무엇인가요?", "correct": "오크로시카", "wrong": ["가스파초", "스베콜니크", "홀로드니크"]},
                {"question": "절구통을 타고 날아다니고 닭다리 위에 지어진 오두막에 사는 동화 속 캐릭터는 누구인가요?", "correct": "바바 야가", "wrong": ["코셰이", "즈메이 고리니치", "레시"]},
                {"question": "데드 모로즈(Ded Moroz, 러시아판 산타클로스)를 돕고 항상 파란색이나 흰색 옷을 입는 소녀의 이름은 무엇인가요?", "correct": "스네구로치카", "wrong": ["알료누시카", "바실리사", "눈의 여왕"]},
                {"question": "삼각형처럼 생겼으며 러시아 민속 음악의 상징인 악기는 무엇인가요?", "correct": "발랄라이카", "wrong": ["구슬리", "가르몬", "돔라"]}
            ]
        }

    RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    KOREAN_ALPHABET = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ" # Только основные согласные и гласные

    def _load_word_targets(self) -> Dict[str, List[str]]:
        """Загружает слова для режима сбора слов"""
        return {
            "ru": ["КОД", "ИГРА", "ЗМЕЙКА", "ЯБЛОКО", "ПИТОН", "ПРОГРАММА", "БАБУШКА", "МАМА", "ПАПА", "СЫН", "ДОЧЬ"],
            "en": ["CODE", "GAME", "SNAKE", "APPLE", "PYTHON", "PROGRAM", "GRANDMA", "MOM", "DAD", "SON", "DAUGHTER"],
            "ko": ["코드", "게임", "뱀", "사과", "파이썬", "프로그램", "할머니", "엄마", "아빠", "아들", "딸"]
        }

    def _get_word_translation(self, word: str, from_lang: str, to_lang: str) -> str:
        """Получает перевод слова из одного языка в другой"""
        word_dict = {
            "КОД": {"en": "CODE", "ko": "코드"},
            "ИГРА": {"en": "GAME", "ko": "게임"},
            "ЗМЕЙКА": {"en": "SNAKE", "ko": "뱀"},
            "ЯБЛОКО": {"en": "APPLE", "ko": "사과"},
            "ПИТОН": {"en": "PYTHON", "ko": "파이썬"},
            "ПРОГРАММА": {"en": "PROGRAM", "ko": "프로그램"},
            "БАБУШКА": {"en": "GRANDMA", "ko": "할머니"},
            "МАМА": {"en": "MOM", "ko": "엄마"},
            "ПАПА": {"en": "DAD", "ko": "아빠"},
            "СЫН": {"en": "SON", "ko": "아들"},
            "ДОЧЬ": {"en": "DAUGHTER", "ko": "딸"},
            # Обратные переводы
            "CODE": {"ru": "КОД", "ko": "코드"},
            "GAME": {"ru": "ИГРА", "ko": "게임"},
            "SNAKE": {"ru": "ЗМЕЙКА", "ko": "뱀"},
            "APPLE": {"ru": "ЯБЛОКО", "ko": "사과"},
            "PYTHON": {"ru": "ПИТОН", "ko": "파이썬"},
            "PROGRAM": {"ru": "ПРОГРАММА", "ko": "프로그램"},
            "GRANDMA": {"ru": "БАБУШКА", "ko": "할머니"},
            "MOM": {"ru": "МАМА", "ko": "엄마"},
            "DAD": {"ru": "ПАПА", "ko": "아빠"},
            "SON": {"ru": "СЫН", "ko": "아들"},
            "DAUGHTER": {"ru": "ДОЧЬ", "ko": "딸"},
            # Корейские слова
            "코드": {"ru": "КОД", "en": "CODE"},
            "게임": {"ru": "ИГРА", "en": "GAME"},
            "뱀": {"ru": "ЗМЕЙКА", "en": "SNAKE"},
            "사과": {"ru": "ЯБЛОКО", "en": "APPLE"},
            "파이썬": {"ru": "ПИТОН", "en": "PYTHON"},
            "프로그램": {"ru": "ПРОГРАММА", "en": "PROGRAM"},
            "할머니": {"ru": "БАБУШКА", "en": "GRANDMA"},
            "엄마": {"ru": "МАМА", "en": "MOM"},
            "아빠": {"ru": "ПАПА", "en": "DAD"},
            "아들": {"ru": "СЫН", "en": "SON"},
            "딸": {"ru": "ДОЧЬ", "en": "DAUGHTER"}
        }
        
        if word in word_dict and to_lang in word_dict[word]:
            return word_dict[word][to_lang]
        return word  # Если перевода нет, возвращаем исходное слово

    def _get_random_letter(self, lang: Language) -> str:
        """Возвращает случайную букву из алфавита выбранного языка"""
        if lang == Language.RUSSIAN:
            return random.choice(self.RUSSIAN_ALPHABET)
        elif lang == Language.ENGLISH:
            return random.choice(self.ENGLISH_ALPHABET)
        elif lang == Language.KOREAN:
            # Для корейского нужны только одиночные символы из алфавита
            return random.choice(self.KOREAN_ALPHABET)
        return "" # Дефолтное значение

    def start_game(self, mode: GameMode):
        """Начинает игру в выбранном режиме"""
        self.game_mode = mode
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.grid_width, self.grid_height)
        self.score = 0
        self.paused = False
        self.current_screen = "game"
        self.used_questions = []  # Сбрасываем использованные вопросы
        self.quiz_completed = False  # Сбрасываем флаг завершения

        if mode == GameMode.CLASSIC:
            self.apple = Apple(self.grid_width, self.grid_height)
        elif mode == GameMode.QUIZ:
            self._spawn_quiz_apple()
        elif mode == GameMode.WORD_COLLECTION:
            self.current_word = ""
            self.current_word_game_lang = ""
            self.collected_letters = []
            self._spawn_word_apple()

    def _spawn_quiz_apple(self):
        """Создает яблоки с номерами ответов для викторины"""
        questions = self.quiz_questions.get(self.game_lang.value, [])
        available_questions = [q for q in questions if q not in self.used_questions]

        if not available_questions:
            # Все вопросы использованы - игра завершена
            self.quiz_completed = True
            self.current_screen = "quiz_completed"
            return

        if available_questions:
            q = random.choice(available_questions)
            self.used_questions.append(q)  # Добавляем вопрос в использованные
            self.quiz_question = q["question"]
            self.quiz_answers = [q["correct"]] + q["wrong"]
            random.shuffle(self.quiz_answers)
            self.quiz_correct_answer = q["correct"]
            self.quiz_correct_number = self.quiz_answers.index(q["correct"]) + 1

            # Создаем яблоки с номерами ответов
            self.quiz_apples = []
            for i in range(len(self.quiz_answers)):
                apple = QuizApple(self.grid_width, self.grid_height, q["question"], q["correct"], q["wrong"], i + 1)
                # Размещаем яблоки в случайных позициях, избегая змейки
                apple.position = self._get_random_quiz_apple_position()
                self.quiz_apples.append(apple)

            # Устанавливаем первое яблоко как текущее для отображения
            self.apple = self.quiz_apples[0]

    def _get_random_quiz_apple_position(self) -> Tuple[int, int]:
        """Получает случайную позицию для яблока викторины, избегая змейки"""
        while True:
            x = random.randint(2, self.grid_width - 3)
            y = random.randint(2, self.grid_height - 3)
            position = (x, y)

            # Проверяем, что позиция не занята змейкой
            if position not in self.snake.body:
                return position

    def _spawn_word_apple(self):
        """Создает яблоки для режима сбора слов: одно правильное и несколько неправильных"""
        if not self.current_word:
            # Берем слово из словаря языка интерфейса (для отображения)
            words = self.word_targets.get(self.interface_lang.value, [])
            if words:
                self.current_word = random.choice(words)
                # Получаем перевод этого слова на язык игры (для сбора букв)
                self.current_word_game_lang = self._get_word_translation(
                    self.current_word, 
                    self.interface_lang.value, 
                    self.game_lang.value
                )
                self.collected_letters = []
            else:
                return  # Нет слов для сбора

        # Проверяем по слову на языке игры (так как буквы собираем на языке игры)
        if len(self.collected_letters) >= len(self.current_word_game_lang):
            # Слово собрано, начинаем новое
            self.score += 10
            self.current_word = ""
            self.current_word_game_lang = ""
            self.collected_letters = []
            self._spawn_word_apple()
            return

        self.word_apples = []
        occupied_positions = list(self.snake.body)

        # 1. Создаем правильное яблоко (буква из слова на языке игры)
        correct_letter = self.current_word_game_lang[len(self.collected_letters)]
        correct_pos = self._get_unique_position(occupied_positions)
        correct_apple = WordApple(self.grid_width, self.grid_height, correct_letter, is_correct=True)
        correct_apple.position = correct_pos
        self.word_apples.append(correct_apple)
        occupied_positions.append(correct_pos)

        # 2. Создаем неправильные яблоки (от 2 до 4)
        num_wrong_apples = random.randint(2, 4)
        for _ in range(num_wrong_apples):
            wrong_letter = self._get_random_letter(self.game_lang)
            # Убедимся, что неправильная буква не является текущей правильной
            while wrong_letter == correct_letter:
                wrong_letter = self._get_random_letter(self.game_lang)

            wrong_pos = self._get_unique_position(occupied_positions)
            wrong_apple = WordApple(self.grid_width, self.grid_height, wrong_letter, is_correct=False)
            wrong_apple.position = wrong_pos
            self.word_apples.append(wrong_apple)
            occupied_positions.append(wrong_pos)

    def _get_unique_position(self, occupied_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Генерирует уникальную позицию, не занятую другими объектами"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            new_position = (x, y)
            if new_position not in occupied_positions:
                return new_position

    def handle_events(self):
        """Обрабатывает события"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # Универсальная обработка клавиш R, M, Q, ESC
                if event.key == pygame.K_r:
                    self._handle_restart_key()
                elif event.key == pygame.K_m:
                    self._handle_menu_key()
                elif event.key == pygame.K_q:
                    self._handle_quit_key()
                elif event.key == pygame.K_ESCAPE:
                    self._handle_escape_key()
                else:
                    # Специфичная обработка для каждого экрана
                    if self.current_screen == "menu":
                        self._handle_menu_events(event)
                    elif self.current_screen == "settings":
                        self._handle_settings_events(event)
                    elif self.current_screen == "game":
                        self._handle_game_events(event)
                    elif self.current_screen == "quiz_completed":
                        self._handle_quiz_completed_events(event)

    def _handle_restart_key(self):
        """Универсальная обработка клавиши R (перезапуск)"""
        if self.current_screen == "game_over":
            # Перезапуск игры в том же режиме
            if self.game_mode:
                self.start_game(self.game_mode)
        elif self.current_screen == "quiz_completed":
            # Перезапуск викторины
            self.start_game(GameMode.QUIZ)
        elif self.current_screen == "game":
            # Перезапуск текущей игры
            if self.game_mode:
                self.start_game(self.game_mode)

    def _handle_menu_key(self):
        """Универсальная обработка клавиши M (главное меню)"""
        if self.current_screen in ["game_over", "quiz_completed", "game"]:
            self.current_screen = "menu"

    def _handle_quit_key(self):
        """Универсальная обработка клавиши Q (выход)"""
        if self.current_screen == "game":
            self.current_screen = "menu"
        elif self.current_screen == "menu":
            self.running = False
        elif self.current_screen == "settings":
            self.current_screen = "menu"

    def _handle_escape_key(self):
        """Универсальная обработка клавиши ESC (назад)"""
        if self.current_screen == "settings":
            self.current_screen = "menu"
        elif self.current_screen == "game":
            self.current_screen = "menu"
        elif self.current_screen == "quiz_completed":
            self.current_screen = "menu"

    def _handle_menu_events(self, event):
        """Обрабатывает события главного меню"""
        if event.key == pygame.K_1:
            self.start_game(GameMode.CLASSIC)
        elif event.key == pygame.K_2:
            self.start_game(GameMode.QUIZ)
        elif event.key == pygame.K_3:
            self.start_game(GameMode.WORD_COLLECTION)
        elif event.key == pygame.K_s:
            self.current_screen = "settings"
        # Клавиша Q теперь обрабатывается универсально

    def _handle_settings_events(self, event):
        """Обрабатывает события настроек"""
        # Клавиша ESC теперь обрабатывается универсально
        if event.key == pygame.K_1:
            self.interface_lang = Language.RUSSIAN
            self.localization.set_language(Language.RUSSIAN)
        elif event.key == pygame.K_2:
            self.interface_lang = Language.ENGLISH
            self.localization.set_language(Language.ENGLISH)
        elif event.key == pygame.K_3:
            self.interface_lang = Language.KOREAN
            self.localization.set_language(Language.KOREAN)
        elif event.key == pygame.K_4:
            self.game_lang = Language.RUSSIAN
        elif event.key == pygame.K_5:
            self.game_lang = Language.ENGLISH
        elif event.key == pygame.K_6:
            self.game_lang = Language.KOREAN
        elif event.key == pygame.K_7:
            self.change_resolution("800x600")
        elif event.key == pygame.K_8:
            self.change_resolution("1000x700")
        elif event.key == pygame.K_9:
            self.change_resolution("1200x800")
        elif event.key == pygame.K_0:
            self.change_resolution("1366x768")
        elif event.key == pygame.K_MINUS:
            self.change_resolution("1920x1080")

    def _handle_game_events(self, event):
        """Обрабатывает события игры"""
        if event.key == pygame.K_w:
            self.snake.change_direction(Direction.UP)
        elif event.key == pygame.K_s:
            self.snake.change_direction(Direction.DOWN)
        elif event.key == pygame.K_a:
            self.snake.change_direction(Direction.LEFT)
        elif event.key == pygame.K_d:
            self.snake.change_direction(Direction.RIGHT)
        elif event.key == pygame.K_c:
            self.paused = not self.paused
        elif event.key == pygame.K_v and self.paused:
            self.paused = False
        # Клавиша Q теперь обрабатывается универсально

    def _handle_quiz_events(self, event):
        """Обрабатывает события викторины"""
        # Викторина теперь работает через поедание яблок, события не нужны
        pass

    def _handle_quiz_completed_events(self, event):
        """Обрабатывает события экрана завершения викторины"""
        # Клавиши R и M теперь обрабатываются универсально
        pass

    def _check_quiz_answer(self, apple_number: int):
        """Проверяет ответ на вопрос викторины по номеру съеденного яблока"""
        if apple_number == self.quiz_correct_number:
            self.quiz_result = True
            self.score += 10
            self.quiz_result_timer = 30  # Показываем результат 0.5 секунды
            # Создаем новый вопрос
            self._spawn_quiz_apple()
        else:
            # Неправильный ответ - игра заканчивается
            self.current_screen = "game_over"

    def update(self):
        """Обновляет состояние игры"""
        if self.current_screen == "game" and not self.paused:
            self.snake.move()

            # Проверка столкновения с собой
            if self.snake.check_collision():
                self.current_screen = "game_over"
                return

            # Проверка поедания яблока
            if self.game_mode == GameMode.QUIZ:
                # Проверяем столкновение с любым из яблок викторины
                for apple in self.quiz_apples:
                    if self.snake.body[0] == apple.position:
                        self.snake.grow()
                        self._check_quiz_answer(apple.answer_number)
                        break
            elif self.game_mode == GameMode.WORD_COLLECTION:
                # Проверяем столкновение с яблоками в режиме сбора слов
                for apple in list(self.word_apples): # Используем list(), чтобы избежать изменения списка во время итерации
                    if self.snake.body[0] == apple.position:
                        if apple.is_correct:
                            self.snake.grow()
                            self.collected_letters.append(apple.letter)
                            self.score += 1
                            # После сбора правильной буквы, пересоздаем все яблоки
                            self._spawn_word_apple()
                        else:
                            # Съели неправильное яблоко - конец игры
                            self.current_screen = "game_over"
                        break # Выходим после обработки первого столкновения
            else:
                # Обычная логика для других режимов (CLASSIC)
                if self.snake.body[0] == self.apple.position:
                    self.snake.grow()
                    self.score += 1
                    self.apple.respawn(self.snake.body)

        # Обновление таймера результата викторины
        if self.quiz_result_timer > 0:
            self.quiz_result_timer -= 1
            if self.quiz_result_timer == 0:
                self.quiz_result = None


    def draw(self):
        """Отрисовывает игру"""
        self.screen.fill(GRAY)

        if self.current_screen == "menu":
            self._draw_menu()
        elif self.current_screen == "settings":
            self._draw_settings()
        elif self.current_screen == "game":
            self._draw_game()
        elif self.current_screen == "game_over":
            self._draw_game_over()
        elif self.current_screen == "quiz_completed":
            self._draw_quiz_completed()

        pygame.display.flip()

    def _draw_menu(self):
        """Отрисовывает главное меню"""
        font_large = get_korean_font(48)
        font_medium = get_korean_font(32)
        font_small = get_korean_font(24)

        # Заголовок
        title = font_large.render(self.localization.get_text("title"), True, WHITE)
        title_rect = title.get_rect(center=(self.window_width // 2, 100))
        self.screen.blit(title, title_rect)

        # Режимы игры
        y_offset = 200
        modes = [
            (1, self.localization.get_text("classic_mode")),
            (2, self.localization.get_text("quiz_mode")),
            (3, self.localization.get_text("word_mode"))
        ]

        for key, mode_name in modes:
            text = font_medium.render(f"{key}. {mode_name}", True, WHITE)
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50

        # Кнопки
        play_text = font_medium.render(self.localization.get_text("play"), True, GREEN)
        play_rect = play_text.get_rect(center=(self.window_width // 2, y_offset + 50))
        self.screen.blit(play_text, play_rect)

        settings_text = font_medium.render(f"S. {self.localization.get_text('settings')}", True, YELLOW)
        settings_rect = settings_text.get_rect(center=(self.window_width // 2, y_offset + 100))
        self.screen.blit(settings_text, settings_rect)

        exit_text = font_medium.render(f"Q. {self.localization.get_text('exit')}", True, RED)
        exit_rect = exit_text.get_rect(center=(self.window_width // 2, y_offset + 150))
        self.screen.blit(exit_text, exit_rect)

        # Управление
        controls_y = self.window_height - 150
        controls_text = font_small.render(self.localization.get_text("controls"), True, GRAY)
        controls_rect = controls_text.get_rect(center=(self.window_width // 2, controls_y))
        self.screen.blit(controls_text, controls_rect)

        control_items = [
            self.localization.get_text("up"),
            self.localization.get_text("down"),
            self.localization.get_text("left"),
            self.localization.get_text("right"),
            self.localization.get_text("pause_key"),
            self.localization.get_text("resume_key"),
            self.localization.get_text("quit_key")
        ]

        for i, item in enumerate(control_items):
            text = font_small.render(item, True, GRAY)
            text_rect = text.get_rect(center=(self.window_width // 2, controls_y + 20 + i * 15))
            self.screen.blit(text, text_rect)

    def _draw_settings(self):
        """Отрисовывает настройки"""
        font_large = get_korean_font(48)
        font_medium = get_korean_font(32)
        font_small = get_korean_font(24)

        # Заголовок
        title = font_large.render(self.localization.get_text("settings"), True, WHITE)
        title_rect = title.get_rect(center=(self.window_width // 2, 100))
        self.screen.blit(title, title_rect)

        # Язык интерфейса
        y_offset = 200
        interface_text = font_medium.render(self.localization.get_text("interface_lang"), True, WHITE)
        interface_rect = interface_text.get_rect(center=(self.window_width // 2, y_offset))
        self.screen.blit(interface_text, interface_rect)

        languages = [
            (1, "Русский", Language.RUSSIAN),
            (2, "English", Language.ENGLISH),
            (3, "한국어", Language.KOREAN)
        ]

        for key, name, lang in languages:
            color = GREEN if lang == self.interface_lang else WHITE
            text = font_small.render(f"{key}. {name}", True, color)
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset + 30 + key * 25))
            self.screen.blit(text, text_rect)

        # Язык игры
        y_offset += 150
        game_text = font_medium.render(self.localization.get_text("game_lang"), True, WHITE)
        game_rect = game_text.get_rect(center=(self.window_width // 2, y_offset))
        self.screen.blit(game_text, game_rect)

        for key, name, lang in languages:
            color = GREEN if lang == self.game_lang else WHITE
            text = font_small.render(f"{key + 3}. {name}", True, color)
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset + 30 + key * 25))
            self.screen.blit(text, text_rect)

        # Разрешение экрана
        y_offset += 150
        resolution_text = font_medium.render(self.localization.get_text("resolution"), True, WHITE)
        resolution_rect = resolution_text.get_rect(center=(self.window_width // 2, y_offset))
        self.screen.blit(resolution_text, resolution_rect)

        resolution_options = [
            (7, "800x600"),
            (8, "1000x700"),
            (9, "1200x800"),
            (0, "1366x768"),
            ("-", "1920x1080")
        ]

        for key, res in resolution_options:
            color = GREEN if res == self.current_resolution else WHITE
            text = font_small.render(f"{key}. {res}", True, color)
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset + 30 + resolution_options.index((key, res)) * 25))
            self.screen.blit(text, text_rect)

        # Инструкции
        esc_text = font_small.render("ESC - Назад в меню", True, GRAY)
        esc_rect = esc_text.get_rect(center=(self.window_width // 2, self.window_height - 50))
        self.screen.blit(esc_text, esc_rect)

    def _draw_game(self):
        """Отрисовывает игровое поле"""
        # Отрисовка змейки
        self.snake.draw(self.screen)

        # Отрисовка яблок
        if self.game_mode == GameMode.QUIZ:
            # Для викторины отображаем все яблоки с номерами
            for apple in self.quiz_apples:
                apple.draw(self.screen)
        elif self.game_mode == GameMode.WORD_COLLECTION:
            # Для режима сбора слов отображаем все яблоки с буквами
            for apple in self.word_apples:
                apple.draw(self.screen)
        else:
            # Для других режимов отображаем обычное яблоко
            self.apple.draw(self.screen)

        # Счет
        font = get_korean_font(36)
        score_text = font.render(f"{self.localization.get_text('score')}: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Пауза
        if self.paused:
            font_large = get_korean_font(72)
            pause_text = font_large.render(self.localization.get_text("pause"), True, YELLOW)
            pause_rect = pause_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(pause_text, pause_rect)

        # Результат викторины
        if self.quiz_result is not None:
            font_large = get_korean_font(48)
            if self.quiz_result:
                result_text = font_large.render(self.localization.get_text("correct"), True, GREEN)
            else:
                result_text = font_large.render(self.localization.get_text("wrong"), True, RED)
            result_rect = result_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(result_text, result_rect)

        # Вопрос викторины (отображается поверх игрового поля)
        if self.game_mode == GameMode.QUIZ and self.quiz_question:
            self._draw_quiz_overlay()

        # Цель для режима сбора слов
        if self.game_mode == GameMode.WORD_COLLECTION and self.current_word:
            font = get_korean_font(24)
            # Целевое слово на языке интерфейса (сверху)
            word_text = font.render(f"{self.localization.get_text('word')}: {self.current_word}", True, WHITE)
            self.screen.blit(word_text, (10, 50))

            # Собранные буквы на языке игры (снизу)
            collected_text = font.render(f"{self.localization.get_text('collect_word')}: {''.join(self.collected_letters)}", True, WHITE)
            self.screen.blit(collected_text, (10, 80))

    def _draw_quiz_overlay(self):
        """Отрисовывает вопрос викторины поверх игрового поля"""
        font_large = get_korean_font(36)
        font_medium = get_korean_font(28)
        font_small = get_korean_font(24)

        # Прозрачный фон для вопроса (такой же как игровое поле)
        overlay = pygame.Surface((self.window_width, 200))
        overlay.set_alpha(150)  # Прозрачность для видимости змейки
        overlay.fill(GRAY)  # Тот же цвет, что и игровое поле
        self.screen.blit(overlay, (0, 0))

        # Вопрос
        question_text = font_large.render(self.localization.get_text("question"), True, WHITE)
        question_rect = question_text.get_rect(center=(self.window_width // 2, 30))
        self.screen.blit(question_text, question_rect)

        # Текст вопроса
        question_content = font_medium.render(self.quiz_question, True, WHITE)
        question_content_rect = question_content.get_rect(center=(self.window_width // 2, 70))
        self.screen.blit(question_content, question_content_rect)

        # Ответы с номерами
        y_offset = 120
        for i, answer in enumerate(self.quiz_answers):
            text = font_small.render(f"{i + 1}. {answer}", True, WHITE)
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset + i * 25))
            self.screen.blit(text, text_rect)

    def _draw_quiz_completed(self):
        """Отрисовывает экран завершения викторины"""
        font_large = get_korean_font(72)
        font_medium = get_korean_font(36)
        font_small = get_korean_font(24)

        # Поздравление
        congrats_text = font_large.render("Молодец!", True, GREEN)
        congrats_rect = congrats_text.get_rect(center=(self.window_width // 2, 200))
        self.screen.blit(congrats_text, congrats_rect)

        # Сообщение о завершении
        message_text = font_medium.render("Ты ответил на все вопросы и прошел игру!", True, WHITE)
        message_rect = message_text.get_rect(center=(self.window_width // 2, 300))
        self.screen.blit(message_text, message_rect)

        # Финальный счет
        score_text = font_medium.render(f"{self.localization.get_text('final_score')}: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.window_width // 2, 350))
        self.screen.blit(score_text, score_rect)

        # Кнопки
        restart_text = font_medium.render(f"R. {self.localization.get_text('restart')}", True, GREEN)
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, 450))
        self.screen.blit(restart_text, restart_rect)

        menu_text = font_medium.render(f"M. {self.localization.get_text('back_to_menu')}", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(self.window_width // 2, 500))
        self.screen.blit(menu_text, menu_rect)

    def _draw_game_over(self):
        """Отрисовывает экран окончания игры"""
        font_large = get_korean_font(72)
        font_medium = get_korean_font(36)
        font_small = get_korean_font(24)

        # Game Over
        game_over_text = font_large.render(self.localization.get_text("game_over"), True, RED)
        game_over_rect = game_over_text.get_rect(center=(self.window_width // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)

        # Финальный счет
        score_text = font_medium.render(f"{self.localization.get_text('final_score')}: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.window_width // 2, 300))
        self.screen.blit(score_text, score_rect)

        # Кнопки
        restart_text = font_medium.render(f"R. {self.localization.get_text('restart')}", True, GREEN)
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, 400))
        self.screen.blit(restart_text, restart_rect)

        menu_text = font_medium.render(f"M. {self.localization.get_text('back_to_menu')}", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(self.window_width // 2, 450))
        self.screen.blit(menu_text, menu_rect)

    def run(self):
        """Запускает главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS для змейки

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
