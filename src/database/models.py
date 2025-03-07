from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Таблица Clubs (Клубы)
class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    working_hours = Column(String(255), nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    rating = Column(String(50), nullable=True)

    # Связь с категориями через промежуточную таблицу
    categories = relationship('Category', secondary='club_categories')

    def __repr__(self):
        return f"<Club(name='{self.name}', address='{self.address}')>"

# Таблица Clusters (Кластеры)
class Cluster(Base):
    __tablename__ = 'clusters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    # Связь с категориями
    categories = relationship('Category', back_populates='cluster')

    def __repr__(self):
        return f"<Cluster(name='{self.name}')>"

# Таблица Categories (Категории)
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    cluster_id = Column(Integer, ForeignKey('clusters.id'), nullable=False)

    # Связи
    cluster = relationship('Cluster', back_populates='categories')
    clubs = relationship('Club', secondary='club_categories')

    def __repr__(self):
        return f"<Category(name='{self.name}', cluster_id={self.cluster_id})>"

# Таблица Club_Categories (Связь клубов и категорий)
class ClubCategory(Base):
    __tablename__ = 'club_categories'

    club_id = Column(Integer, ForeignKey('clubs.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)

    def __repr__(self):
        return f"<ClubCategory(club_id={self.club_id}, category_id={self.category_id})>"
    
    