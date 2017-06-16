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

item1 = CategoryItem(name = 'Overwatch', description = 'In a time of global crisis, an international task force of heroes banded together to restore peace to a war-torn world: OVERWATCH.', genre = 'FPS', category  = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = 'Rocket League', description = 'Soccer meets driving once again in the long-awaited, physics-based multiplayer-focused sequel to Supersonic Acrobatic Rocket-Powered Battle-Cars!', genre = 'Sports', category = category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name = 'Prey', description = 'FIGHT THE INVASION – Your Mind. The Station. Earth Itself. Nothing is safe from the alien threat.', genre = 'FPS', category = category1)

session.add(item3)
session.commit()

item4 = CategoryItem(name = 'Uncharted 4', description = 'Several years after his last adventure, retired fortune hunter, Nathan Drake, is forced back into the world of thieves with the stakes much more personal.', genre = 'Action Adventure', category = category1)

session.add(item4)
session.commit()

item5 = CategoryItem(name = 'FIFA 17', description = 'EA SPORTS™ FIFA 18 blurs the line between the virtual and real worlds, bringing to life the players, teams, and atmospheres of The World’s Game.', genre = 'Sports', category = category1)

session.add(item5)
session.commit()


# Category Xbox One
category2 = Category(name = 'Xbox One')

session.add(category2)
session.commit()

item1 = CategoryItem(name = 'Forza Horizon 3', description = 'More than a race car game, Forza Horizon 3 for Xbox is a game for car enthusiasts.', genre = 'Racing', category  = category2)

session.add(item1)
session.commit()

item2 = CategoryItem(name = 'Gears of War 4', description = 'A new saga begins for one of the most acclaimed video game franchises in history. After narrowly escaping an attack on their village, JD Fenix and his friends, Kait and Del, must rescue the ones they love and discover the source of a monstrous new enemy.', genre = 'TPS', category = category2)

session.add(item2)
session.commit()

item3 = CategoryItem(name = 'Battlefield 1', description = 'The game is set in the period of World War I, and is inspired by historic events. Players can make use of World War I weapons, including bolt-action rifles, automatic and semi-automatic rifles, artillery, flamethrowers, and mustard gas to combat opponents.', genre = 'FPS', category = category2)

session.add(item3)
session.commit()

item4 = CategoryItem(name = 'Titanfall 2', description = 'Following the death of his mentor, Cooper inherits BT-7274, a Vanguard-class Titan, and the two join forces against the Interstellar Manufacturing Corporation and their hired mercenaries.', genre = 'FPS', category = category2)

session.add(item4)
session.commit()

item5 = CategoryItem(name = 'NBA 2K17', description = 'NBA 2K17 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 18th installment in the NBA 2K franchise.', genre = 'Sports', category = category2)

session.add(item5)
session.commit()


# Category PC
category3 = Category(name = 'PC')

session.add(category3)
session.commit()

item1 = CategoryItem(name = 'Dishonored 2', description = 'Dishonored 2 is an action-adventure stealth video game developed by Arkane Studios and published by Bethesda Softworks.', genre = 'Action Adventure', category  = category3)

session.add(item1)
session.commit()

item2 = CategoryItem(name = 'H1Z1', description = 'H1Z1: Just Survive is an upcoming survival sandbox massively multiplayer online game developed and published by Daybreak Game Company for Microsoft Windows.', genre = 'TPS', category = category3)

session.add(item2)
session.commit()

item3 = CategoryItem(name = 'Dead Rising 4', description = 'Dead Rising 4 is an open world survival horror beat em up video game developed by Capcom Vancouver and published by Microsoft Studios.', genre = 'Survival Horror', category = category3)

session.add(item3)
session.commit()

item4 = CategoryItem(name = 'DOOM', description = 'Doom is a first-person shooter video game developed by id Software and published by Bethesda Softworks. A reboot of the Doom franchise.', genre = 'FPS', category = category3)

session.add(item4)
session.commit()

item5 = CategoryItem(name = 'League of Legends', description = 'League of Legends is a multiplayer online battle arena video game developed and published by Riot Games for Microsoft Windows and macOS.', genre = 'Battle Arena', category = category3)

session.add(item5)
session.commit()


# Category Phone
category4 = Category(name = 'Mobile')

session.add(category4)
session.commit()

item1 = CategoryItem(name = 'Pokemon GO', description = 'Pokémon Go is a free-to-play, location-based augmented reality game developed by Niantic for iOS and Android devices.', genre = 'Augmented Reality', category  = category4)

session.add(item1)
session.commit()

item2 = CategoryItem(name = 'Clash Royale', description = 'Clash Royale is a freemium mobile strategy video game developed and published by Supercell. The game combines elements from collectible card games, tower defense, and multiplayer online battle arena.', genre = 'Strategy', category = category4)

session.add(item2)
session.commit()

item3 = CategoryItem(name = 'Super Mario Run', description = 'Super Mario Run is a side-scrolling, auto-running video game developed and published by Nintendo for iOS and Android devices.', genre = 'Auto-Running', category = category4)

session.add(item3)
session.commit()

item4 = CategoryItem(name = 'Mini Metro', description = 'Mini Metro is a puzzle strategy video game developed by indie development team Dinosaur Polo Club.', genre = 'Strategy', category = category4)

session.add(item4)
session.commit()


print 'You added items to the catalog!'
