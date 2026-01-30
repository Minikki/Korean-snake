# Установка корейских шрифтов для игры Clever Snake

Для корректного отображения корейских символов в игре необходимо установить корейские шрифты на вашей системе.

## Windows

### Windows 10/11 (рекомендуется)
1. Откройте **Параметры** → **Время и язык** → **Язык**
2. Нажмите **Добавить язык**
3. Найдите и выберите **한국어 (Korean)**
4. Установите языковой пакет
5. Перезагрузите компьютер

### Альтернативный способ
1. Скачайте шрифт **Noto Sans CJK KR** с [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
2. Установите файлы .ttf в папку `C:\Windows\Fonts\`

## macOS

1. Откройте **Системные настройки** → **Язык и регион**
2. Нажмите **+** и добавьте **한국어**
3. Перезагрузите компьютер

### Альтернативный способ
1. Скачайте **Noto Sans CJK KR** с [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
2. Дважды кликните на файлы .ttf и нажмите **Установить шрифт**

## Linux (Ubuntu/Debian)

```bash
# Установка корейских шрифтов
sudo apt-get update
sudo apt-get install fonts-nanum fonts-nanum-coding

# Или установка Noto шрифтов
sudo apt-get install fonts-noto-cjk
```

## Linux (CentOS/RHEL/Fedora)

```bash
# Для CentOS/RHEL
sudo yum install google-noto-cjk-fonts

# Для Fedora
sudo dnf install google-noto-cjk-fonts
```

## Проверка установки

После установки шрифтов запустите игру:
```bash
python snake_game.py
```

Если корейские символы отображаются корректно, установка прошла успешно.

## Альтернативные шрифты

Если стандартные шрифты не работают, попробуйте установить:

1. **Noto Sans CJK KR** - [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
2. **Source Han Sans KR** - [Adobe Fonts](https://github.com/adobe-fonts/source-han-sans)
3. **Nanum Gothic** - [Naver Fonts](https://hangeul.naver.com/font)

## Устранение проблем

### Проблема: Корейские символы отображаются как квадратики
**Решение**: Установите корейские шрифты согласно инструкции выше

### Проблема: Игра не запускается
**Решение**: Убедитесь, что установлен Python 3.7+ и pygame:
```bash
pip install pygame
```

### Проблема: Шрифты установлены, но не работают
**Решение**: Перезагрузите компьютер и перезапустите игру

## Поддержка

Если у вас возникли проблемы с отображением корейских символов, создайте issue в репозитории проекта с указанием:
- Операционной системы
- Версии Python
- Версии pygame
- Скриншота проблемы

