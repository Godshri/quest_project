import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quest_project.settings')
django.setup()

from quest_app.models import Puzzle

# Данные загадок - все 48 загадок для 4 комнат
puzzles_data = [
    # 🖥️ СЕРВЕРНАЯ (12 загадок)
    {'room': 'server', 'name': 'Бинарный перевод', 'description': 'Переведи: 01001000 01100101 01101100 01101100 01101111', 'solution': 'hello', 'difficulty': 1, 'order': 1},
    {'room': 'server', 'name': 'Шифр Цезаря', 'description': 'Kfcf со сдвигом 2', 'solution': 'code', 'difficulty': 1, 'order': 2},
    {'room': 'server', 'name': 'Логика сервера', 'description': '2 + 2 * 2', 'solution': '6', 'difficulty': 1, 'order': 3},
    {'room': 'server', 'name': 'Шестнадцатеричный код', 'description': 'Переведи HEX: 4A 61 76 61', 'solution': 'java', 'difficulty': 2, 'order': 4},
    {'room': 'server', 'name': 'Ошибка сервера', 'description': 'Самый известный код ошибки HTTP', 'solution': '404', 'difficulty': 1, 'order': 5},
    {'room': 'server', 'name': 'Порты', 'description': 'Стандартный порт для HTTP', 'solution': '80', 'difficulty': 2, 'order': 6},
    {'room': 'server', 'name': 'Протокол', 'description': 'Протокол для безопасного соединения', 'solution': 'https', 'difficulty': 2, 'order': 7},
    {'room': 'server', 'name': 'База данных', 'description': 'Язык запросов к базам данных', 'solution': 'sql', 'difficulty': 2, 'order': 8},
    {'room': 'server', 'name': 'Переменная', 'description': 'Что хранит значение в программировании?', 'solution': 'переменная', 'difficulty': 1, 'order': 9},
    {'room': 'server', 'name': 'Компиляция', 'description': 'Процесс превращения кода в программу', 'solution': 'компиляция', 'difficulty': 3, 'order': 10},
    {'room': 'server', 'name': 'Рекурсия', 'description': 'Когда функция вызывает саму себя', 'solution': 'рекурсия', 'difficulty': 3, 'order': 11},
    {'room': 'server', 'name': 'Git команда', 'description': 'Команда для сохранения изменений в Git', 'solution': 'commit', 'difficulty': 2, 'order': 12},

    # 📚 БИБЛИОТЕКА (12 загадок)
    {'room': 'library', 'name': 'Первый язык', 'description': 'Какой язык программирования считается первым?', 'solution': 'fortran', 'difficulty': 2, 'order': 1},
    {'room': 'library', 'name': 'Основатель Python', 'description': 'Кто создал язык Python?', 'solution': 'гвидо', 'difficulty': 2, 'order': 2},
    {'room': 'library', 'name': 'Принципы ООП', 'description': 'Назови три принципа ООП через запятую', 'solution': 'инкапсуляция,наследование,полиморфизм', 'difficulty': 3, 'order': 3},
    {'room': 'library', 'name': 'Язык веба', 'description': 'Какой язык выполняется в браузере?', 'solution': 'javascript', 'difficulty': 1, 'order': 4},
    {'room': 'library', 'name': 'Создатель Linux', 'description': 'Кто создал ядро Linux?', 'solution': 'линус', 'difficulty': 2, 'order': 5},
    {'room': 'library', 'name': 'Первый компьютер', 'description': 'Кто создал первую вычислительную машину?', 'solution': 'бэббидж', 'difficulty': 3, 'order': 6},
    {'room': 'library', 'name': 'Язык С', 'description': 'Кто создал язык программирования C?', 'solution': 'деннис ритчи', 'difficulty': 2, 'order': 7},
    {'room': 'library', 'name': 'Женщина-программист', 'description': 'Первая женщина-программист', 'solution': 'ада лавлейс', 'difficulty': 2, 'order': 8},
    {'room': 'library', 'name': 'Паттерн проектирования', 'description': 'Самый известный патtern "Одиночка" на английском', 'solution': 'singleton', 'difficulty': 3, 'order': 9},
    {'room': 'library', 'name': 'Алгоритм поиска', 'description': 'Алгоритм поиска в ширину на английском', 'solution': 'breadth first search', 'difficulty': 3, 'order': 10},
    {'room': 'library', 'name': 'Типы данных', 'description': 'Основной тип данных для true/false', 'solution': 'boolean', 'difficulty': 2, 'order': 11},
    {'room': 'library', 'name': 'Компилятор', 'description': 'Кто написала первый компилятор?', 'solution': 'грейс хоппер', 'difficulty': 2, 'order': 12},

    # 🎮 АРКАДНЫЕ АВТОМАТЫ (12 загадок)
    {'room': 'arcade', 'name': 'Алгоритм сортировки', 'description': 'Какой алгоритм сортировки самый быстрый?', 'solution': 'быстрая', 'difficulty': 2, 'order': 1},
    {'room': 'arcade', 'name': 'Структура данных LIFO', 'description': 'Структура данных по принципу "последний пришел - первый ушел"', 'solution': 'стек', 'difficulty': 2, 'order': 2},
    {'room': 'arcade', 'name': 'Рекурсивный случай', 'description': 'Что должно быть в рекурсивной функции?', 'solution': 'базовый случай', 'difficulty': 3, 'order': 3},
    {'room': 'arcade', 'name': 'Структура данных FIFO', 'description': 'Структура данных по принципу "первый пришел - первый ушел"', 'solution': 'очередь', 'difficulty': 2, 'order': 4},
    {'room': 'arcade', 'name': 'Сложность алгоритма', 'description': 'Сложность быстрой сортировки в лучшем случае', 'solution': 'n log n', 'difficulty': 3, 'order': 5},
    {'room': 'arcade', 'name': 'Поиск в массиве', 'description': 'Алгоритм поиска в отсортированном массиве', 'solution': 'бинарный поиск', 'difficulty': 2, 'order': 6},
    {'room': 'arcade', 'name': 'Хэш-таблица', 'description': 'Структура данных для быстрого поиска', 'solution': 'хэш таблица', 'difficulty': 3, 'order': 7},
    {'room': 'arcade', 'name': 'Графы', 'description': 'Алгоритм поиска кратчайшего пути', 'solution': 'дейкстра', 'difficulty': 3, 'order': 8},
    {'room': 'arcade', 'name': 'Связный список', 'description': 'Структура данных из узлов с указателями', 'solution': 'связный список', 'difficulty': 2, 'order': 9},
    {'room': 'arcade', 'name': 'Дерево', 'description': 'Сбалансированное бинарное дерево поиска', 'solution': 'avl дерево', 'difficulty': 3, 'order': 10},
    {'room': 'arcade', 'name': 'Сортировка', 'description': 'Алгоритм сортировки с временем O(n²)', 'solution': 'пузырьковая', 'difficulty': 2, 'order': 11},
    {'room': 'arcade', 'name': 'Динамическое программирование', 'description': 'Метод решения задач разбиением на подзадачи', 'solution': 'динамическое программирование', 'difficulty': 3, 'order': 12},

    # 🏙️ КРЫША (12 загадок)
    {'room': 'roof', 'name': 'Финальная загадка', 'description': 'Что имеет ключи, но не может открыть замки?', 'solution': 'клавиатура', 'difficulty': 1, 'order': 1},
    {'room': 'roof', 'name': 'Великий программист', 'description': 'Кто написал первый компилятор?', 'solution': 'грейс хоппер', 'difficulty': 2, 'order': 2},
    {'room': 'roof', 'name': 'Магическое число', 'description': 'Число 256 в программировании', 'solution': 'байт', 'difficulty': 2, 'order': 3},
    {'room': 'roof', 'name': 'Память компьютера', 'description': 'Наименьшая единица информации', 'solution': 'бит', 'difficulty': 2, 'order': 4},
    {'room': 'roof', 'name': 'Операционная система', 'description': 'Самая популярная ОС для серверов', 'solution': 'linux', 'difficulty': 2, 'order': 5},
    {'room': 'roof', 'name': 'Язык программирования', 'description': 'Язык назван в честь комедийного шоу', 'solution': 'python', 'difficulty': 1, 'order': 6},
    {'room': 'roof', 'name': 'Веб-технология', 'description': 'Язык разметки для веб-страниц', 'solution': 'html', 'difficulty': 1, 'order': 7},
    {'room': 'roof', 'name': 'База данных', 'description': 'Самая популярная реляционная БД с открытым исходным кодом', 'solution': 'mysql', 'difficulty': 2, 'order': 8},
    {'room': 'roof', 'name': 'Фреймворк', 'description': 'Популярный JavaScript фреймворк', 'solution': 'react', 'difficulty': 2, 'order': 9},
    {'room': 'roof', 'name': 'Мобильная разработка', 'description': 'Язык для разработки под iOS', 'solution': 'swift', 'difficulty': 2, 'order': 10},
    {'room': 'roof', 'name': 'Искусственный интеллект', 'description': 'Библиотека для машинного обучения на Python', 'solution': 'tensorflow', 'difficulty': 3, 'order': 11},
    {'room': 'roof', 'name': 'Кибербезопасность', 'description': 'Тип атаки на веб-приложения через выполнение кода', 'solution': 'sql инъекция', 'difficulty': 3, 'order': 12},
]

# Очистка старых и добавление новых загадок
Puzzle.objects.all().delete()
for data in puzzles_data:
    Puzzle.objects.create(**data)

print(f"Создано {len(puzzles_data)} загадок успешно!")