import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

# Функция для получения данных со страницы клуба с обновленными требованиями
def get_club_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        name_tag = soup.find("meta", property="og:title")
        name = name_tag["content"].strip() if name_tag else "Название не найдено"

        address_tag = soup.find("meta", property="og:description")
        address = "Адрес не найден"
        if address_tag:
            desc_content = address_tag["content"]
            if "полный адрес:" in desc_content:
                address = desc_content.split("полный адрес:")[-1].split("⭐️")[0].strip()

        description_tag = soup.find(
            "dd",
            class_="js-desc oh word-break expanding-description",
            attrs={"data-track-text-action": "description", "data-track-text-category": "service"}
        )
        if description_tag:
            paragraphs = description_tag.find_all("p", class_="description-text")
            description = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        else:
            description = "Описание не найдено"

        hours_tag = soup.find("dd", class_="upper-first")
        hours = hours_tag.text if hours_tag else "Часы работы не найдены"

        categories_data = {}
        category_tags = soup.find_all("dt", class_="js-service-type-name")
        for category_tag in category_tags:
            category_name = category_tag.get_text(strip=True)
            subcategories = []
            next_sibling = category_tag.find_next_sibling("dd")
            if next_sibling and next_sibling.get("class") and "js-service-links" in next_sibling.get("class"):
                subcategories = [a.get_text(strip=True) for a in next_sibling.find_all("a")]
            categories_data[category_name] = subcategories

        payment_info = "Стоимость не найдена"
        payment_tag = soup.find(string=lambda t: t and ("стоимость" in t.lower() or "цена" in t.lower()))
        if payment_tag:
            payment_info = payment_tag.strip()

        rating_tag = soup.find("div", class_="service-action__item")
        rating = rating_tag.get_text(strip=True) if rating_tag else "Рейтинг не найден"

        return {
            "name": name,
            "address": address,
            "description": description,
            "working_hours": hours,
            "сategories": categories_data, 
            "rating": rating,
        }
    else:
        print(f"Ошибка при запросе страницы клуба: {response.status_code}")
        return None

def parse_fitness_clubs(file):
    try:
        # with open("/home/khsn/Learn/Uni/sports_project/server/Utils/bbc.html", encoding="utf-8") as file:
        #     soup = BeautifulSoup(file, "html.parser")
        
        soup = BeautifulSoup(file, "html.parser")

        club_items = soup.select("li.minicard-item.js-results-item")
        clubs_data = []  # Список для хранения данных всех клубов

        for item in club_items:
            club_link_tag = item.select_one("a.title-link.js-item-url")
            club_url = club_link_tag["href"] if club_link_tag else None
            if club_url and not club_url.startswith("http"):
                club_url = "https://zoon.ru" + club_url

            name_tag = item.select_one("div.z-text--bold")
            name = name_tag.get_text(strip=True) if name_tag else "Название не найдено"
            
            lat = item.get("data-lat", "Нет данных")
            lon = item.get("data-lon", "Нет данных")

            if club_url:
                print(f"Парсинг клуба: {club_url}")
                club_data = get_club_details(club_url)
                if club_data:
                    club_data["name"] = name
                    club_data["coordinates"] = {
                        "lat": lat,
                        "lon": lon
                    }
                    clubs_data.append(club_data)
                    print(f"Данные сохранены для клуба: {club_data['name']}")
                print("-" * 40)

        actual_time = datetime.now()
        # Сохраняем загруженную страницу в файл
        with open(f"./Data/{actual_time}_fitness_clubs.html", "w", encoding="utf-8") as html:
            html.write(file)
        print(f"HTML-страница успешно сохранена в '{actual_time}_fitness_clubs.html'.")
        
        # Сохранение данных в JSON файл
        with open(f"./Data/{actual_time}_fitness_clubs.json", "w", encoding="utf-8") as file:
            json.dump(clubs_data, file, ensure_ascii=False, indent=4)
        print(f"Все данные успешно сохранены в {actual_time}_fitness_clubs.json")
        return(f"{actual_time}_fitness_clubs.json")
    except FileNotFoundError:
        print("Файл html не найден.")

# # Запуск парсера
# parse_fitness_clubs()