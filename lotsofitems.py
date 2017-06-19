from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem

# Engine is bound to the metadata of the Base class so declaratives can be
# accessed through the DBSession instance
engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Creating DBSession.
session = DBSession()


# Category PS4
category1 = Category(name = "PS4")

session.add(category1)
session.commit()

item1 = CategoryItem(name = "Overwatch", description = "An international task force of heroes banded together to restore peace to a war-torn world.", genre = "FPS", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "Rocket League", description = "Soccer meets driving in the long-awaited, physics-based multiplayer-focused sequel to Supersonic Acrobatic Rocket-Powered Battle-Cars!", genre = "Sports", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Prey", description = "FIGHT THE INVASION.", genre = "FPS", category = category1)

session.add(item2)
session.commit()

item1 = CategoryItem(name = "Uncharted 4", description = "Nathan Drake is forced back into the world of thieves with the stakes much more personal.", genre = "Action Adventure", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "FIFA 17", description = "EA SPORTS FIFA 18 blurs the line between the virtual and real worlds of The Worlds Game.", genre = "Sports", category = category1)

session.add(item2)
session.commit()


# Category Xbox One
category1 = Category(name = "Xbox One")

session.add(category1)
session.commit()

item1 = CategoryItem(name = "Forza Horizon 3", description = "More than a race car game, Forza Horizon 3 for Xbox is a game for car enthusiasts.", genre = "Racing", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "Gears of War 4", description = "After narrowly escaping an attack on their village, JD Fenix and his friends must rescue the ones they love and discover the source of a new enemy.", genre = "TPS", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "Battlefield 1", description = "The game is set in the period of World War I, and is inspired by historic events. Players can make use of World War I weapons to combat opponents.", genre = "FPS", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Titanfall 2", description = "Cooper and a Vanguard-class Titan, and the two join forces against the Interstellar Manufacturing Corporation and their hired mercenaries.", genre = "FPS", category = category1)

session.add(item2)
session.commit()

item1 = CategoryItem(name = "NBA 2K17", description = "NBA 2K17 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports.", genre = "Sports", category = category1)

session.add(item1)
session.commit()


# Category PC
category1 = Category(name = "PC")

session.add(category1)
session.commit()

item1 = CategoryItem(name = "Dishonored 2", description = "Dishonored 2 is an action-adventure stealth video game developed by Arkane Studios and published by Bethesda Softworks.", genre = "Action Adventure", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "H1Z1", description = "H1Z1: Just Survive is an upcoming survival sandbox massively multiplayer online game.", genre = "TPS", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "Dead Rising 4", description = "Dead Rising 4 is an open world survival horror beat em up video game developed by Capcom Vancouver.", genre = "Survival Horror", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "DOOM", description = "Doom is a first-person shooter video game developed by id Software and published by Bethesda Softworks.", genre = "FPS", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "League of Legends", description = "League of Legends is a multiplayer online battle arena video game developed and published by Riot Games.", genre = "Battle Arena", category = category1)

session.add(item1)
session.commit()


# Category Phone
category1 = Category(name = "Mobile")

session.add(category1)
session.commit()

item1 = CategoryItem(name = "Pokemon GO", description = "Pokemon Go is a free to play, location-based augmented reality game developed by Niantic.", genre = "Augmented Reality", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "Clash Royale", description = "Clash Royale is a freemium mobile strategy video game developed and published by Supercell.", genre = "Strategy", category = category1)

session.add(item1)
session.commit()

item1 = CategoryItem(name = "Super Mario Run", description = "Super Mario Run is a side-scrolling, auto-running video game developed and published by Nintendo.", genre = "Auto-Running", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Mini Metro", description = "Mini Metro is a puzzle strategy video game developed by indie development team Dinosaur Polo Club.", genre = "Strategy", category = category1)

session.add(item2)
session.commit()


print "You added items to the catalog!"
