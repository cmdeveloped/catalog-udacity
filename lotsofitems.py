from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem

# Engine is bound to the metadata of the Base class so declaratives can be
# accessed through the DBSession instance
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Creating DBSession.
session = DBSession()


# Category PS4
category1 = Category(name = 'PS4')

session.add(category1)
session.commit()


# Category Xbox One
category2 = Category(name = 'Xbox One')

session.add(category2)
session.commit()


# Category PC
category3 = Category(name = 'PC')

session.add(category3)
session.commit()


# Category Phone
category4 = Category(name = 'Mobile')

session.add(category4)
session.commit()
