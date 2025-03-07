import pandas as pd
from collections import Counter
import re
from io import StringIO


# Создаем DataFrame
df = pd.read_csv("/home/khsn/Learn/Uni/sports_project/server/fitness_clubs.csv")

# Функция для очистки и нормализации текста
def normalize_text(text):
    if not isinstance(text, str):
        return ''
    # Удаляем лишние пробелы, приводим к нижнему регистру для сравнения
    text = re.sub(r'\s+', ' ', text.strip())
    # Удаляем лишние символы, оставляем буквы, цифры и основные знаки
    text = re.sub(r'[^\w\s:/-]', '', text)
    # Приводим первую букву к верхнему регистру
    return text.capitalize()

# Функция для очистки категорий
def clean_categories(categories_str):
    if not isinstance(categories_str, str):
        return []
    
    # Разбиваем по разделителю "|"
    categories = [cat.strip() for cat in categories_str.split('|')]
    
    # Словарь для хранения очищенных категорий и их подкатегорий
    cleaned_dict = {}
    
    for cat in categories:
        # Разделяем основную категорию и подкатегории
        parts = cat.split(':')
        main_cat = normalize_text(parts[0])
        
        if not main_cat or main_cat == 'Нет подкатегорий':
            continue
            
        # Если есть подкатегории, обрабатываем их
        if len(parts) > 1:
            subcats = [normalize_text(sub.strip()) for sub in parts[1].split(',')]
            subcats = [sub for sub in subcats if sub and sub != 'Нет подкатегорий']
            cleaned_dict[main_cat] = subcats
        else:
            cleaned_dict[main_cat] = []
    
    # Преобразуем словарь в список основных категорий
    cleaned_categories = sorted(cleaned_dict.keys())
    
    return cleaned_categories

# Применяем очистку к столбцу "Категории"
df['Категории_очищенные'] = df['Категории'].apply(clean_categories)

# Функция для красивого вывода
def format_categories(cats):
    return ' | '.join(cats)

# Применяем форматирование для вывода
df['Категории_очищенные_формат'] = df['Категории_очищенные'].apply(format_categories)

# Выводим результаты
print("Оригинальные категории и очищенные:")
for index, row in df.iterrows():
    print(f"\nНазвание: {row['Название']}")
    print(f"Оригинальные категории: {row['Категории']}")
    print(f"Очищенные категории: {row['Категории_очищенные_формат']}")

# Подсчет частоты категорий
all_categories = [cat for sublist in df['Категории_очищенные'] for cat in sublist]
category_counts = Counter(all_categories)
print("\nЧастота категорий:")
for cat, count in category_counts.most_common():
    print(f"{cat}: {count}")

# Сохраняем результат (раскомментируйте для сохранения)
df.to_csv('cleaned_fitness_clubs_dynamic.csv', index=False)