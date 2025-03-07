import pandas as pd
import re

file_path = "/home/khsn/Learn/Uni/sports_project/server/fitness_clubs.csv"
df = pd.read_csv(file_path)

df.head(), df.columns

categories_series = df["Категории"].dropna().str.split(" | ")  # Разделение по " | "
all_categories = set()

for cat_list in categories_series:
    for cat in cat_list:
        main_category = cat.split(":")[0].strip()
        all_categories.add(main_category)

unique_categories = sorted(all_categories)
print(len(unique_categories), unique_categories[:20])


clean_categories = set()

for category in unique_categories:
    cleaned = re.sub(r"[^a-zA-Zа-яА-Я0-9ёЁ\s-]", "", category).strip()
    if cleaned and len(cleaned) > 1: 
        clean_categories.add(cleaned)

final_categories = sorted(clean_categories)
print(len(final_categories), final_categories)

with open("categories.txt", "w", encoding="utf-8") as file:
    for category in final_categories:
        file.write(category + "\n")