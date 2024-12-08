# goit-cs-hw-05
Тема 10. Вступ до паралельних обчислень

Перед початком роботи:
1. Версія **Python: >=3.10**
2. Cтворюємо віртуальне середовище (Python: >=3.10) `.env`: `python -m venv .env`
3. Активуємо (відповідно до своєї ОС): `source .env/bin/activate`
4. Інсталюємо залежності: `pip install -r requirements.txt`
5. По завершенню роботи деактивовуємо: `deactivate`

## Завдання 1
Напишіть Python-скрипт, який буде читати всі файли у вказаній користувачем вихідній папці (source folder) і розподіляти їх по підпапках у директорії призначення (output folder) на основі розширення файлів. Скрипт повинен виконувати сортування асинхронно для більш ефективної обробки великої кількості файлів.

**Покрокова інструкція**
1. Імпортуйте необхідні асинхронні бібліотеки.
2. Створіть об'єкт `ArgumentParser` для обробки аргументів командного рядка.
3. Додайте необхідні аргументи для визначення вихідної та цільової папок.
4. Ініціалізуйте асинхронні шляхи для вихідної та цільової папок.
5. Напишіть асинхронну функцію `read_folder`, яка рекурсивно читає всі файли у вихідній папці та її підпапках.
5. Напишіть асинхронну функцію `copy_file`, яка копіює кожен файл у відповідну підпапку у цільовій папці на основі його розширення.
6. Налаштуйте логування помилок.
7. Запустіть асинхронну функцію `read_folder` у головному блоці.

### Критерії прийняття
- Код виконує асинхронне читання та копіювання файлів.
- Файли розподілено по підпапках на основі їх розширень.
- Програма обробляє аргументи командного рядка.
- Усі помилки логовано.
- Код читабельний та відповідає стандартам `PEP 8`.

### Запуск та перевірка
Для генерації файлів та папок потрібно запустити `file_generator.py` та вказати в параметрі бажану назву директорії (код взято та оновлено із завдання [goit-algo-hw-03](https://github.com/nickolas-z/goit-algo-hw-03/blob/main/file_generator.py)).
Далі запускаємо `task1.py` в параметрі вказуємо директорію яку потрібно обробити (назву яку ми вказували для генерації).
Як результат, буде створена за замовчуванням директорія `dst` із відсортованими файлами.
Усі операції логуються у файлі: `task1.log`.
Опис усіх доступних параметрів: `task1.py -h`.

### Ресурси
- [task1.py](./task1.py)
- [file_generator.py](./file_generator.py)

## Завдання 2
Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси, аналізує частоту використання слів у тексті за допомогою парадигми `MapReduce` і візуалізує топ-слова з найвищою частотою використання у тексті.

**Покрокова інструкція**
1. Імпортуйте необхідні модулі (matplotlib та інші).
2. Візьміть код реалізації `MapReduce` з конспекту.
3. Створіть функцію `visualize_top_words` для візуалізації результатів.
4. У головному блоці коду отримайте текст за `URL`, застосуйте `MapReduce` та візуалізуйте результати.

### Критерії прийняття
- Код завантажує текст із заданої URL-адреси.
- Код виконує аналіз частоти слів із використанням `MapReduce`.
- Візуалізація відображає топ-слова за частотою використання.
- Код використовує багатопотоковість.
- Код читабельний та відповідає стандартам `PEP 8`.

### Запуск та перевірка
Для демонстрайії потрібно запустити `task2.py` за замовчуванням скрипт завантажить `https://www.gutenberg.org/files/98/98-0.txt`, зробить розрахунки та виведе діаграму із 10-ма найбільш вживанішими словами в тексті.
Усі операції логуються у файлі: `task2.log`.
Опис усіх доступних параметрів: `task2.py -h`.

### Ресурси
- [task2.py](./task2.py)

## Додатково
- [Домашнє завдання до модуля "Асинхронна обробка"](https://www.edu.goit.global/uk/learn/25315460/19336208/21189584/homework)
- [https://github.com/nickolas-z/goit-cs-hw-05](https://github.com/nickolas-z/goit-cs-hw-05)
- [goit-cs-hw-05-main.zip]()
- [Computer-Systems-and-Their-Fundamentals](https://github.com/nickolas-z/Computer-Systems-and-Their-Fundamentals)