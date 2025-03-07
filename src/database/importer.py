import json
import os
from sqlalchemy.exc import IntegrityError
from .models import Club, Cluster, Category, Base
from .session import engine, SessionLocal

# Путь к папке с данными относительно корня проекта
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Data')

def load_json_data(filename):
    """Загружает данные из JSON-файла в папке /data/."""
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_or_create_club(session, club_data, clusters_cache, categories_cache):
    """Обновляет существующий клуб или создает новый."""
    # Ищем клуб по имени и адресу
    club = session.query(Club).filter_by(
        name=club_data.get('name', ''),
        address=club_data.get('address', '')
    ).first()

    if club:
        # Обновляем существующий клуб
        club.description = club_data.get('description', club.description)
        club.working_hours = club_data.get('working_hours', club.working_hours)
        club.lat = float(club_data['coordinates']['lat']) if club_data.get('coordinates') else club.lat
        club.lon = float(club_data['coordinates']['lon']) if club_data.get('coordinates') else club.lon
        club.rating = club_data.get('rating', club.rating)
    else:
        # Создаем новый клуб
        club = Club(
            name=club_data.get('name', ''),
            address=club_data.get('address', ''),
            description=club_data.get('description', ''),
            working_hours=club_data.get('working_hours', ''),
            lat=float(club_data['coordinates']['lat']) if club_data.get('coordinates') else None,
            lon=float(club_data['coordinates']['lon']) if club_data.get('coordinates') else None,
            rating=club_data.get('rating', '')
        )
        session.add(club)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            return None  # Если не удалось создать, пропускаем

    # Обрабатываем категории (с учетом опечатки 'сategories')
    categories_dict = club_data.get('categories', club_data.get('сategories', {}))
    new_categories = set()  # Храним новые категории для клуба

    for cluster_name, categories_list in categories_dict.items():
        # Создаем или получаем кластер
        if cluster_name not in clusters_cache:
            cluster = session.query(Cluster).filter_by(name=cluster_name).first()
            if not cluster:
                cluster = Cluster(name=cluster_name)
                session.add(cluster)
                session.flush()
            clusters_cache[cluster_name] = cluster
        else:
            cluster = clusters_cache[cluster_name]

        # Обрабатываем категории в кластере
        for category_name in categories_list:
            if category_name not in categories_cache:
                category = session.query(Category).filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name, cluster_id=cluster.id)
                    session.add(category)
                    session.flush()
                categories_cache[category_name] = category
            else:
                category = categories_cache[category_name]

            new_categories.add(category)

    # Обновляем связи с категориями
    current_categories = set(club.categories)
    categories_to_add = new_categories - current_categories
    categories_to_remove = current_categories - new_categories

    for category in categories_to_add:
        club.categories.append(category)
    for category in categories_to_remove:
        club.categories.remove(category)

    return club

def import_data_to_db(json_data, session):
    """Импортирует или актуализирует данные из JSON в базу данных."""
    clusters_cache = {}
    categories_cache = {}
    updated_count = 0
    created_count = 0

    for club_data in json_data:
        club = update_or_create_club(session, club_data, clusters_cache, categories_cache)
        if club:
            if club.id:  # Если клуб уже был в базе (id существует)
                updated_count += 1
            else:
                created_count += 1

    session.commit()
    print(f"Создано новых клубов: {created_count}, обновлено существующих: {updated_count}")

def initialize_database(filename='fitness_clubs.json'):
    """Инициализирует базу данных и загружает/обновляет данные из JSON."""
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    try:
        json_data = load_json_data(filename)
        import_data_to_db(json_data, session)
    except Exception as e:
        session.rollback()
        print(f"Ошибка при импорте/обновлении данных: {str(e)}")
    finally:
        session.close()