# Configuration for DB
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# Creating Class definitions for DB

class Category(Base):

    __tablename__ = 'category'

    # Mappers for our class category
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

class CategoryItem(Base):

    __tablename__ = 'category_item'

    # Mappers for our class category
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    genre = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        # This returns object data in serialized format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'genre' : self.genre,
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
