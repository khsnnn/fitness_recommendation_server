from database import engine, get_db
from server.src.database.models import Base, Club, Cluster, Category, ClubCategory

Base.metadata.create_all(bind=engine)

def add_sample_data():
    db = next(get_db())
    
    cluster = Cluster(name="Фитнес и общая физическая активность")
    db.add(cluster)
    db.commit()

    category = Category(name="Фитнес", cluster_id=cluster.id)
    db.add(category)
    db.commit()

    club = Club(
        name="DDX Fitness",
        address="Тюмень, улица Чернышевского, 1Б",
        description="Фитнес-клуб с премиальными тренажерами",
        working_hours="Скоро открытие!",
        lat=57.1584488,
        lon=65.5094521,
        rating="4,5/4 оценки"
    )
    db.add(club)
    db.commit()

    club_category = ClubCategory(club_id=club.id, category_id=category.id)
    db.add(club_category)
    db.commit()

    print("Данные успешно добавлены!")

if __name__ == "__main__":
    add_sample_data()