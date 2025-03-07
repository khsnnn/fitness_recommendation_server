from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
import openrouteservice
import os
from unittest.mock import patch
import pytest
from pydantic import BaseModel, Field


# Инициализация приложения FastAPI
app = FastAPI()

# Разрешаем CORS для всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настраиваем клиента OpenRouteService
ORS_API_KEY = os.getenv("ORS_API_KEY", "mock_key")
client = openrouteservice.Client(key=ORS_API_KEY)


class Club(BaseModel):
    name: str = Field(..., alias="Название")
    address: str = Field(..., alias="Адрес")
    description: Optional[str] = Field(..., alias="Описание")
    working_hours: str = Field(..., alias="Часы работы")
    categories: str = Field(..., alias="Категории")
    lat: float = Field(..., alias="Координаты (lat)")
    lon: float = Field(..., alias="Координаты (lon)")
    rating: float = Field(..., alias="Рейтинг")


    class Config:
        allow_population_by_field_name = True

# Загрузка данных о клубах
def load_clubs():
    df = pd.read_csv("fitness_clubs.csv")
    df["lat"] = df["Координаты (lat)"]
    df["lon"] = df["Координаты (lon)"]
    # Очистка и преобразование рейтинга
    df["Рейтинг"] = df["Рейтинг"].str.replace(',', '.').str.extract(r'([\d.]+)')[0].astype(float)
    return df

# Функция для расчета расстояния
def get_route_distance(user_lat, user_lon, club_lat, club_lon):
    coords = ((user_lon, user_lat), (club_lon, club_lat))
    route = client.directions(
        coords, profile="foot-walking", format="geojson"
    )
    return route["features"][0]["properties"]["segments"][0]["distance"] / 1000

# Эндпоинт для получения списка клубов
@app.get("/clubs", response_model=List[Club])
def get_clubs(
    min_rating: float = Query(None),
    user_lat: float = Query(None), 
    user_lon: float = Query(None),
    max_distance: float = Query(None),
    sort_by: str = Query(None),
):
    clubs_df = load_clubs()

    if min_rating is not None:
        clubs_df = clubs_df[clubs_df["Рейтинг"] >= min_rating]

    if user_lat and user_lon and max_distance:
        clubs_df["distance"] = clubs_df.apply(
            lambda row: get_route_distance(user_lat, user_lon, row["lat"], row["lon"]),
            axis=1,
        )
        clubs_df = clubs_df[clubs_df["distance"] <= max_distance]

    if sort_by == "rating":
        clubs_df = clubs_df.sort_values(by="Рейтинг", ascending=False)
    elif sort_by == "distance":
        clubs_df = clubs_df.sort_values(by="distance", ascending=True)

    # ✅ Если данных нет — вернем пустой список
    if clubs_df.empty:
        return []

    # ✅ Преобразуем в список словарей
    clubs_data = clubs_df.head(5).to_dict(orient="records") or []

    # ✅ Приведение всех значений к строкам
    for club in clubs_data:
        for key in club:
            club[key] = str(club[key]) if club[key] is not None else ""
    return clubs_data
    

@app.get("/all-clubs", response_model=List[Club])
def get_all_clubs():
    clubs_df = load_clubs()

    # Преобразуем в список словарей
    clubs_data = clubs_df.to_dict(orient="records")

    # Приведение всех значений к строкам
    for club in clubs_data:
        for key in club:
            club[key] = str(club[key]) if club[key] is not None else ""

    return clubs_data


# Эндпоинт для получения данных о фитнес-клубе
@app.post("/fitness-club/")
async def create_fitness_club(club: Club):
    # Здесь просто возвращаем полученные данные в формате JSON
    return club

# Эндпоинт для получения маршрута
@app.get("/route")
def get_route(user_lat: float, user_lon: float, club_lat: float, club_lon: float):
    coords = ((user_lon, user_lat), (club_lon, club_lat))
    route = client.directions(coords, profile="foot-walking", format="geojson")
    return route

# uvicorn main:app --reload
# pytest main.py --disable-warnings
