import logging
import os
from database.importer import import_data_to_db, load_json_data
from database.session import SessionLocal

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Путь к папке с данными
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# def update_database():
#     """Обновляет данные в базе данных из источника."""
#     session = SessionLocal()
#     try:
#         # Шаг 1: Получаем HTML-страницу
#         logger.info("Получение HTML-страницы...")
#         html_content = get_page_html()
#         if not html_content:
#             raise ValueError("Не удалось получить HTML-страницу")

#         # Шаг 2: Парсим HTML и получаем данные
#         logger.info("Парсинг данных из HTML...")
#         parsed_result = parse_fitness_clubs(html_content)
        
#         # Определяем, что вернул parse_fitness_clubs: имя файла или данные
#         if isinstance(parsed_result, str):
#             # Если возвращается имя файла
#             json_filename = parsed_result
#             logger.info(f"Загружаем данные из файла: {json_filename}")
#             json_data = load_json_data(json_filename)
#         else:
#             # Если возвращаются сами данные
#             json_data = parsed_result
#             json_filename = "parsed_data.json"  # Для логов
#             logger.info("Получены данные напрямую из парсера")

#         # Шаг 3: Импортируем данные в базу
#         logger.info(f"Импорт данных из {json_filename} в базу данных...")
#         import_data_to_db(json_data, session)
#         logger.info("Обновление базы данных завершено успешно")

#     except Exception as e:
#         session.rollback()
#         logger.error(f"Ошибка при обновлении базы данных: {str(e)}")
#         raise
#     finally:
#         session.close()

def main():
    """Точка входа для обновления данных."""
    # update_database()
    session = SessionLocal()
    json_data = load_json_data('2025-03-07 02:11:25.427901_fitness_clubs.json')
    import_data_to_db(json_data, session)

if __name__ == "__main__":
    main()