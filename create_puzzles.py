import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quest_project.settings')
django.setup()

from quest_app.models import Puzzle

# Данные загадок - все 60 загадок для 4 комнат (12 основных + 3 сложных с подвохом)
puzzles_data = [
    # 🖥️ СЕРВЕРНАЯ (15 загадок)
    {'room': 'server', 'name': 'Бинарный перевод', 'description': 'Расшифруй название компонента компьютера из двоичного кода ASCII: 01001000 01000100 01000100. Ответ введите на латинской раскладке.', 'solution': 'hdd', 'difficulty': 1, 'order': 1},
    {'room': 'server', 'name': 'Вычисление памяти', 'description': 'В компьютере 2 платы оперативной памяти по 8 Гб каждая. Каков общий объём? Ответ введите только число.', 'solution': '16', 'difficulty': 1, 'order': 2},
    {'room': 'server', 'name': 'Порты подключения', 'description': 'Какой порт чаще всего используется для подключения мышки и клавиатуры? Ответ введите на латинской раскладке (аббревиатура).', 'solution': 'usb', 'difficulty': 1, 'order': 3},
    {'room': 'server', 'name': 'Цифровая магистраль', 'description': 'Я — цифровая магистраль для данных от процессора к памяти. Как меня называют? Ответ введите на русском (одно слово).', 'solution': 'шина', 'difficulty': 2, 'order': 4},
    {'room': 'server', 'name': 'Компонент для изображения', 'description': 'Без меня ты не увидишь ни игры, ни рабочий стол. Что я? Ответ введите на русском (одно слово).', 'solution': 'видеокарта', 'difficulty': 2, 'order': 5},
    {'room': 'server', 'name': 'Шифр Атбаш', 'description': 'РГХСХГХЬХЧГ — это важнейшая часть компьютера. (А=Я, Б=Ю, В=Э, Г=Ь, Д=Ы...). Ответ введите на русском.', 'solution': 'процессор', 'difficulty': 3, 'order': 6},
    {'room': 'server', 'name': 'Скорость процессора', 'description': 'Процессор 3.5 ГГц выполняет сколько тактов в секунду? Ответ введите в научном формате (Xe9).', 'solution': '3.5e9', 'difficulty': 3, 'order': 7},
    {'room': 'server', 'name': 'Тип памяти', 'description': 'Какой тип памяти сохраняет данные при выключении? HDD, RAM или CPU? Ответ введите на латинской раскладке (аббревиатура).', 'solution': 'hdd', 'difficulty': 2, 'order': 8},
    {'room': 'server', 'name': 'Разъем монитора', 'description': 'Какой разъем чаще для монитора? VGA, HDMI или USB? Ответ введите на латинской раскладке (аббревиатура).', 'solution': 'hdmi', 'difficulty': 2, 'order': 9},
    {'room': 'server', 'name': 'Охлаждение', 'description': 'Что охлаждает кулер в системном блоке? Ответ введите на русском (одно слово).', 'solution': 'процессор', 'difficulty': 1, 'order': 10},
    {'room': 'server', 'name': 'Хранение данных', 'description': 'Устройство, использующее лазер для чтения данных? Ответ введите на русском (одно слово).', 'solution': 'дисковод', 'difficulty': 1, 'order': 11},
    {'room': 'server', 'name': 'Сетевой подключение', 'description': 'Какой кабель для проводного интернета? USB, HDMI или Ethernet? Ответ введите на латинской раскладке (одно слово).', 'solution': 'ethernet', 'difficulty': 1, 'order': 12},
    
    # Сложные с подвохом (добавлены)
    {'room': 'server', 'name': 'Подвох с памятью', 'description': 'Компьютер с 4 Гб RAM и файлом подкачки 2 Гб. Сколько всего памяти доступно? Ответ введите только число.', 'solution': '6', 'difficulty': 3, 'order': 13},
    {'room': 'server', 'name': 'Ловушка процессора', 'description': 'Процессор с 4 ядрами по 2.5 ГГц. Общая частота = 10 ГГц? Ответ: да или нет.', 'solution': 'нет', 'difficulty': 3, 'order': 14},
    {'room': 'server', 'name': 'Хитрый бинарный код', 'description': '01010011 01010011 01000100 — что это? Ответ введите на латинской раскладке (аббревиатура).', 'solution': 'ssd', 'difficulty': 3, 'order': 15},

    # 📚 БИБЛИОТЕКА (15 загадок)
    {'room': 'library', 'name': 'Первый компьютер', 'description': 'Создатель первого механического компьютера? Ответ введите фамилию на русском.', 'solution': 'бэббидж', 'difficulty': 2, 'order': 1},
    {'room': 'library', 'name': 'Расчет дискет', 'description': 'Дискета 1.44 Мб. Песня 5 Мб. Сколько дискет нужно? Ответ введите только число (округлить вверх).', 'solution': '4', 'difficulty': 2, 'order': 2},
    {'room': 'library', 'name': 'Первый браузер', 'description': 'Первый графический веб-браузер? Ответ введите на латинской раскладке (название).', 'solution': 'mosaic', 'difficulty': 2, 'order': 3},
    {'room': 'library', 'name': 'Азбука Морзе', 'description': 'Расшифруй имя первой программистки по азбуке Морзе: .- -.. .- Ответ введите на русском (имя).', 'solution': 'ада', 'difficulty': 3, 'order': 4},
    {'room': 'library', 'name': 'Создатель WWW', 'description': 'Первые буквы создателя Всемирной паутины: 20-10-14 (А=1, Б=2...). Ответ введите на русском (имя).', 'solution': 'тим', 'difficulty': 3, 'order': 5},
    {'room': 'library', 'name': 'Язык программирования', 'description': 'Язык 1995 года, первоначально Oak? Ответ введите на латинской раскладке (название языка).', 'solution': 'java', 'difficulty': 2, 'order': 6},
    {'room': 'library', 'name': 'Первая женщина-программист', 'description': 'Первая женщина-программист? Ответ введите имя и фамилию на русском.', 'solution': 'ада лавлейс', 'difficulty': 2, 'order': 7},
    {'room': 'library', 'name': 'Первый электронный компьютер', 'description': 'Первый электронный компьютер 1946 года? Ответ введите на латинской раскладке (аббревиатура).', 'solution': 'eniac', 'difficulty': 3, 'order': 8},
    {'room': 'library', 'name': 'Создатель Linux', 'description': 'Создатель ядра Linux? Ответ введите только имя на русском.', 'solution': 'линус', 'difficulty': 2, 'order': 9},
    {'room': 'library', 'name': 'Год рождения Python', 'description': 'В каком году создан Python? Ответ введите только число.', 'solution': '1991', 'difficulty': 3, 'order': 10},
    {'room': 'library', 'name': 'Первый сайт', 'description': 'Тема первого в мире веб-сайта? Ответ введите на русском.', 'solution': 'всемирная паутина', 'difficulty': 3, 'order': 11},
    {'room': 'library', 'name': 'Изобретатель мыши', 'description': 'Изобретатель компьютерной мыши? Ответ введите фамилию на русском.', 'solution': 'энгельбарт', 'difficulty': 3, 'order': 12},
    
    # Сложные с подвохом
    {'room': 'library', 'name': 'Подвох с годами', 'description': 'Python старше Java? (Python:1991, Java:1995). Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 13},
    {'room': 'library', 'name': 'Ловушка с браузером', 'description': 'Первый браузер назывался WorldWideWeb? Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 14},
    {'room': 'library', 'name': 'Хитрый вопрос о мыши', 'description': 'Первая компьютерная мышь была деревянной? Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 15},

    # 🎮 АРКАДНЫЕ АВТОМАТЫ (15 загадок)
    {'room': 'arcade', 'name': 'Самая продаваемая игра', 'description': 'Игра со строительством из кубиков? Ответ введите на латинской раскладке (название игры).', 'solution': 'minecraft', 'difficulty': 1, 'order': 1},
    {'room': 'arcade', 'name': 'Ребус', 'description': 'Классическая игра: PAC + - + ЧЕЛОВЕК. Ответ введите на латинской раскладке (название игры).', 'solution': 'pacman', 'difficulty': 2, 'order': 2},
    {'room': 'arcade', 'name': 'Игровой жанр', 'description': 'Жанр: строить базу, собирать ресурсы, управлять армией? Ответ введите на русском (название жанра).', 'solution': 'стратегия', 'difficulty': 1, 'order': 3},
    {'room': 'arcade', 'name': 'Шифр Цезаря', 'description': 'Расшифруй игру про ежа: ТПОЙЛ (сдвиг +1). Ответ введите на латинской раскладке (название игры).', 'solution': 'соник', 'difficulty': 3, 'order': 4},
    {'room': 'arcade', 'name': 'Клавиатурный шифр', 'description': 'Расшифруй популярную игру: Nubwxe\dr (смещение влево на клавиатуре). Ответ введите на латинской раскладке (название игры).', 'solution': 'minecraft', 'difficulty': 3, 'order': 5},
    {'room': 'arcade', 'name': 'Подсчет очков', 'description': 'Тетрис: 1 линия=100, 2=300, 3=500. 2+3 линии? Ответ введите только число.', 'solution': '800', 'difficulty': 2, 'order': 6},
    {'room': 'arcade', 'name': 'Игровой персонаж', 'description': 'Главный герой Doom? Ответ введите на русском (имя персонажа).', 'solution': 'думгай', 'difficulty': 2, 'order': 7},
    {'room': 'arcade', 'name': 'Игровая консоль', 'description': 'Первая консоль с дисководами? PlayStation, Xbox, Nintendo. Ответ введите на латинской раскладке (название консоли).', 'solution': 'playstation', 'difficulty': 2, 'order': 10},
    {'room': 'arcade', 'name': 'Киберспорт', 'description': 'Игра с турнирами на миллионы: Dota 2, FIFA, Minecraft? Ответ введите на латинской раскладке (название игры).', 'solution': 'dota 2', 'difficulty': 1, 'order': 11},
    {'room': 'arcade', 'name': 'Игровая механика', 'description': 'Способность мгновенно перемещаться в играх? Ответ введите на русском (одно слово).', 'solution': 'телепортация', 'difficulty': 1, 'order': 12},
    
    # Сложные с подвохом
    {'room': 'arcade', 'name': 'Подвох с Minecraft', 'description': 'Minecraft была создана в конце двухтысячных? Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 13},
    {'room': 'arcade', 'name': 'Ловушка с Pac-Man', 'description': 'Pac-Man изначально назывался Puck-Man? Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 14},
    {'room': 'arcade', 'name': 'Хитрый вопрос о Тетрисе', 'description': 'Тетрис был создан в США? Ответ: да или нет.', 'solution': 'нет', 'difficulty': 3, 'order': 15},

    # 🏙️ КРЫША (15 загадок)
    {'room': 'roof', 'name': 'Беспилотный транспорт', 'description': 'Автомобиль без водителя? Ответ введите на русском (одно слово).', 'solution': 'беспилотный', 'difficulty': 1, 'order': 1},
    {'room': 'roof', 'name': 'Искусственный интеллект', 'description': 'ИИ, обыгравший чемпиона по Go? Ответ введите на латинской раскладке (название системы).', 'solution': 'alphago', 'difficulty': 2, 'order': 2},
    {'room': 'roof', 'name': 'Цифровые деньги', 'description': 'Деньги, которые добывают компьютерами? Ответ введите на русском (одно слово).', 'solution': 'криптовалюта', 'difficulty': 2, 'order': 3},
    {'room': 'roof', 'name': 'Умные часы', 'description': 'Умные часы: "High HR detected while inactive" - что обнаружили? Ответ введите на русском.', 'solution': 'высокий пульс', 'difficulty': 3, 'order': 4},
    {'room': 'roof', 'name': 'Норма шагов', 'description': '6000 шагов = 85% от нормы. Норма? Ответ введите только число (округлить).', 'solution': '7059', 'difficulty': 3, 'order': 5},
    {'room': 'roof', 'name': 'Профессия в AI', 'description': 'Создатель искусственного интеллекта? Ответ введите на русском (название профессии).', 'solution': 'датасайентист', 'difficulty': 2, 'order': 6},
    {'room': 'roof', 'name': 'Технология будущего', 'description': 'Интернет через лампочки? Ответ введите на латинской раскладке (название технологии).', 'solution': 'li-fi', 'difficulty': 3, 'order': 7},
    {'room': 'roof', 'name': 'Виртуальная реальность', 'description': 'Очки для погружения в виртуальный мир? Ответ введите на латинской раскладке (аббревиатура).', 'solution': 'vr', 'difficulty': 1, 'order': 8},
    {'room': 'roof', 'name': 'Умный дом', 'description': 'Система управления домашними устройствами через интернет? Ответ введите на русском.', 'solution': 'умный дом', 'difficulty': 1, 'order': 9},
    {'room': 'roof', 'name': 'Блокчейн', 'description': 'Технология основы биткоина? Ответ введите на латинской раскладке (название технологии).', 'solution': 'blockchain', 'difficulty': 3, 'order': 10},
    {'room': 'roof', 'name': 'Квантовые компьютеры', 'description': 'Компьютеры с кубитами вместо битов? Ответ введите на русском.', 'solution': 'квантовые', 'difficulty': 3, 'order': 11},
    {'room': 'roof', 'name': 'IT-профессия', 'description': 'Защитник компьютерных систем от взломов? Ответ введите на русском (название профессии).', 'solution': 'кибербезопасник', 'difficulty': 2, 'order': 12},
    
    # Сложные с подвохом
    {'room': 'roof', 'name': 'Подвох с беспилотниками', 'description': 'Беспилотные автомобили используют только GPS? Ответ: да или нет.', 'solution': 'нет', 'difficulty': 3, 'order': 13},
    {'room': 'roof', 'name': 'Ловушка с криптовалютой', 'description': 'Биткоин был создан в 2008 году? Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 14},
    {'room': 'roof', 'name': 'Хитрый вопрос о VR', 'description': 'VR очки можно использовать без компьютера? Ответ: да или нет.', 'solution': 'да', 'difficulty': 3, 'order': 15},
]

# Очистка старых и добавление новых загадок
Puzzle.objects.all().delete()
for data in puzzles_data:
    Puzzle.objects.create(**data)

print(f"Создано {len(puzzles_data)} загадок успешно!")