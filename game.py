import rooms
import users


class Player(object):
    def __init__(self):
        pass

    def readDesc(self, user):
        return users.users[user]['description']

    def getInventory(self, user):
        return users.users[user]['inventory']

    def addItem(self, user, item):
        users.users[user]['inventory'].append(item)

    def dropItem(self, user, item):
        itemIndex = users.users[user]['inventory'].index(item)
        users.users[user]['inventory'].pop(itemIndex)

    def getCurLoc(self, user):
        return users.users[user]['location']

class Navigation(object):
    def __init__(self):
        pass

    def getCurLoc(self, user):
        return rooms.rooms[Player().getCurLoc(user)]
        # return self.location

    def moveLoc(self, user, direction):
        dest = self.getCurLoc(user)['exits'][direction]
        users.users[user]['location'] = dest
        # self.location = dest

    def readDesc(self, user):
        return rooms.rooms[self.getCurLoc()]['description']

    def readExits(self, user):
        return rooms.rooms[self.getCurLoc()]['exits']

    def readItems(self, user):
        return rooms.rooms[self.getCurLoc()]['items']
