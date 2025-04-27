from main import app, db, Game

games = [
    {
        "name": "The Legend of Zelda: A Link to the Past",
        "price": "£4.99",
        "description": "A top-down action-adventure classic on the SNES. Rescue Princess Zelda and defeat Ganon in this beloved 16-bit epic.",
        "image": "zelda.jpg",
        "impact": "4 – Cartridge-based, low energy usage, minimal packaging emissions.",
        "platform": "SNES"
    },
    {
        "name": "Super Mario Bros.",
        "price": "£3.99",
        "description": "The iconic side-scroller that launched Mario into stardom. Navigate the Mushroom Kingdom and save Princess Peach!",
        "image": "mario.png",
        "impact": "3 – Very lightweight NES cartridge, minimal materials and power draw.",
        "platform": "NES"
    },
    {
        "name": "Mega Man 2",
        "price": "£4.49",
        "description": "One of the best entries in the classic Mega Man series. Defeat the Robot Masters and face off against Dr. Wily.",
        "image": "mega.jpg",
        "impact": "3 – Like other NES titles, low material and energy footprint.",
        "platform": "NES"
    },
    {
        "name": "Chrono Trigger",
        "price": "£6.99",
        "description": "A masterpiece RPG with time-traveling heroes, stunning pixel art, and a gripping story.",
        "image": "chrono.jpg",
        "impact": "5 – Larger cartridge and packaging; slightly higher manufacturing footprint.",
        "platform": "SNES"
    },
    {
        "name": "Castlevania: Symphony of the Night",
        "price": "£5.99",
        "description": "Explore Dracula’s castle in this legendary Metroidvania. Deep combat and haunting music await.",
        "image": "castlevania.jpg",
        "impact": "6 – CD production and jewel case packaging add to total emissions.",
        "platform": "PlayStation"
    },
    {
        "name": "Sonic the Hedgehog",
        "price": "£3.50",
        "description": "Blast through Green Hill Zone with blazing speed in this SEGA Genesis classic.",
        "image": "sonic.jpg",
        "impact": "4 – Cartridge-based and efficient console power usage.",
        "platform": "Genesis"
    },
    {
        "name": "Final Fantasy VII",
        "price": "£7.99",
        "description": "The turn-based RPG that defined a generation. Join Cloud and friends to stop Sephiroth’s apocalyptic plans.",
        "image": "ff7.jpg",
        "impact": "7 – Multiple discs, plastic cases, and high manufacturing energy cost.",
        "platform": "PlayStation"
    },
    {
        "name": "Donkey Kong Country",
        "price": "£4.49",
        "description": "Barrel through jungle levels with DK and Diddy in this beautifully rendered platformer.",
        "image": "dkc.jpg",
        "impact": "4 – Mid-size SNES cart with standard packaging.",
        "platform": "SNES"
    },
    {
        "name": "EarthBound",
        "price": "£5.49",
        "description": "A quirky RPG full of charm, humor, and aliens. Follow Ness on a journey to save the world.",
        "image": "earthbound.jpg",
        "impact": "6 – Came with an oversized box and guidebook, increasing paper and plastic use.",
        "platform": "SNES"
    },
    {
        "name": "Street Fighter II",
        "price": "£4.25",
        "description": "The definitive 2D fighter. Choose your warrior and battle to be the best in the world.",
        "image": "sf2.webp",
        "impact": "4 – Standard SNES release; modest cartridge and packaging impact.",
        "platform": "SNES"
    }
]

with app.app_context():
    db.create_all()

    for game in games:
        new_game = Game(
            name=game["name"],
            price=game["price"],
            description=game["description"],
            image=game["image"],
            impact=game["impact"],
            platform=game["platform"]
        )
        db.session.add(new_game)

    db.session.commit()
