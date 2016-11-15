#data structure for rooms
rooms = {
    "DeathRoom": {
        "description": "There's a bigass dragon in here! He crushes you to death.",
        "exits": None,
        "items": ["Gold Chest", "Scales"]
    },
    "CaveWest": {
        "description": "The cave is damp and cold. You hear a faint dripping sound that seems to echo for miles.",
        "exits": { "east": "CaveEast",
            "north": "DungeonLeft"
            },
        "items": ["Flask", "Boulder", "Sword"]
    },
    "CaveEast": {
        "description": "This cave is warm and full of dust. You can feel trembles and sounds through the wall, perhaps some danger is around the corner.",
        "exits": { "west": "CaveWest",
            "east" : "DeathRoom"
            },
        "items": ["Sack", "Potion"]
    },
    "DungeonLeft": {
        "description": "It feels sort of wierd in here, too quite perhaps. Better to have a quick look and move on. ",
        "exits": { "up": "StarLand",
            "south": "CaveWest",
            "east" : "EmptyRoom"
            },
        "items": ["Locked Crate"]
    },
    "DungeonRight": {
        "description": "Take a look around, someone forgot his most valuable possesions around here a long time ago. Enjoy! ",
        "exits": { "west": "EmptyRoom",
            "south": "DeathRoom",
            "up" : "PromiseHill"
            },
        "items": ["Book", "Vase", "Coins"]
    },
    "EmptyRoom": {
        "description": "You realize the minute you entered the room, that this was a total waste of time. There is literally nothing in here!",
        "exits": { "up": "WizardCove",
            "south": "CaveEast"
            },
        "items": []
    },
    "ForrestCorner": {
        "description": "Beatiful nature spot to relax for a bit. You feel at ease around here, enjoy and take your time.",
        "exits": {"down": "CaveWest",
            "east" : "CenterWorld"
            },
        "items": ["Stone", "Bones"]
    },
    "CenterWorld": {
        "description": "Busy and confusing in here. Everything is moving all over the place, you feel overwhelmed yet intrigued with this room.",
        "exits": { "west": "ForrestCorner",
            "east" : "MazeCorner"
            },
        "items": ["Scrolls", "Sacrificial Stone", "Ancient artifact"]
    },
    "MazeCorner": {
        "description": "You just went into a big maze, might take a while to get back.",
        "exits": { "west" : "CenterWorld"
            },
        "items": ["Traveler's Tent"]
    },
    "StarLand": {
        "description": "This room feels like looking straight to the sun, everything is bright and shiny. You feel like there must be something worthy around here.",
        "exits": { "south": "ForrestCorner",
            "down" : "DungeonLeft"
            },
        "items": ["Magic ring", "Broken Wand"]
    },
    "WizardCove": {
        "description": "You've hit the magic land, home of the wisdom and eldest minds. Coming in here already make you feel that much prepared for what comes next. They also have the best knowledge and items around.",
        "exits": { "west": "StarLand",
            "south": "CenterWorld",
            "down" : "EmptyRoom"
            },
        "items": ["Wand", "Crystals", "Revival potion"]
    },
    "PromiseHills": {
        "description": "You have entered the land of promise, the mountains don't give you a great view, but you know there is a great adventure after every turn coming up. ",
        "exits": { "west": "WizardCove",
            "down": "DungeonRight"
            },
        "items": ["Mirror of promise", "Energy booster"]
    }
}
