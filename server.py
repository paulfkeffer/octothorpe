from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from random import randrange

class ReadWriteContent(Protocol):

    loggedIn = False

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print('New connection to server')

    def dataReceived(self, data):
        value = data.decode("utf-8")
        if type(value) is str:
            if value.startswith('login'):
                if self.loggedIn == True:
                    self.transport.write(bytes("400:Already logged in\r\n", "utf-8"))
                else:
                    self.sendMap()
                    knownPlayer = False
                    if len(value) < 9:
                        self.transport.write(bytes("400:Expected a name and got nothing\r\n", "utf-8"))
                    else:
                        for key,value in self.factory.listPlayers.items():
                            if value[0] == str(data[6:-2], "utf-8"):
                                self.factory.listPlayers[self] = self.factory.listPlayers.pop(key)
                                knownPlayer = True
                                self.factory.listPlayers[self][4] = True
                                break
                        if knownPlayer == False:
                            self.factory.listPlayers[self] = [str(data[6:-2], 'utf-8'),1,1,0,True]
                        self.loggedIn = True
                        welcome = bytes('200:Welcome to Octothorpe # The Game\r\n', "utf-8")
                        self.transport.write(welcome)
                        for value in self.factory.listPlayers.values():
                            if value[4] is True:
                                toSend2 = bytes(f"101:{value[0]}, {value[1]}, {value[2]}, {value[3]}\r\n", "utf-8")
                                self.transport.write(toSend2)
                        self.sendPlayerLocation()
                        self.checkTreasure()
            elif value.startswith('move'):
                if self.loggedIn == False:
                    self.transport.write(bytes("400:You must login first\r\n", "utf-8"))
                else:
                    self.move(str(data[5:-2], "utf-8"))
            elif value.startswith('map'):
                if self.loggedIn == False:
                    self.transport.write(bytes("400:You must login first\r\n", "utf-8"))
                else:
                    self.sendMap()
            elif value.startswith('quit'):
                self.transport.write(bytes("200:Goodbye!\r\n", "utf-8"))
                self.transport.loseConnection()
            else:
                self.transport.write(bytes("400:Invalid command\r\n", "utf-8"))
        else:
            self.transport.write(bytes("400:Input not understood\r\n", "utf-8"))

    def checkTreasure(self):
        for key,value in self.factory.listObjects.items():
            playerData = self.factory.listPlayers[self]
            if playerData[1] == value[0] and playerData[2] == value[1]:
                toSend3 = bytes(f"102:{key} You found treasure #{key} worth {value[2]} points!\r\n", "utf-8")
                playerData[3] = playerData[3]+value[2]
                self.transport.write(toSend3)
                self.sendTreasureUpdate(value, key, self.factory.listPlayers[self][0])
                self.factory.listObjects.pop(key)
                break

    def sendTreasureUpdate(self, value, key, playerName):
        for player,data in self.factory.listPlayers.items():
            if player is not self and data[4] is True:
                toSend = bytes(f"103:{playerName} found treasure #{key} worth {value[2]} points!\r\n", "utf-8\r\n")
                player.transport.write(toSend)

    def sendPlayerLocation(self):
        playerData = self.factory.listPlayers[self]
        for player,data in self.factory.listPlayers.items():
            if player is not self and data[4] is True:
                toSend = bytes(f"101:{playerData[0]}, {playerData[1]}, {playerData[2]}, {playerData[3]}\r\n", "utf-8")
                player.transport.write(toSend)

    def sendMap(self):
        self.transport.write(bytes("200:Ok\r\n", "utf-8"))
        self.transport.write(bytes("104:20, 20\r\n", "utf-8"))
        self.transport.write(bytes("104:####################\r\n", "utf-8"))
        for x in range(0, 18):
            self.transport.write(bytes("104:#                  #\r\n", "utf-8"))
        self.transport.write(bytes("104:####################\r\n", "utf-8"))

    def move(self, direction):
        self.transport.write(bytes(f"200:move {direction}\r\n", "utf-8"))
        playerData = self.factory.listPlayers[self]
        moved = False
        if direction == 'north':
            if playerData[1] == self.factory.gridYSize-1:
                self.transport.write(bytes("400:Invalid Move\r\n", "utf-8"))
            else:
                playerData[1] = playerData[1]+1
                moved = True
        elif direction == 'south':
            if playerData[1] == 1:
                self.transport.write(bytes("400:Invalid Move\r\n", "utf-8"))
            else:
                playerData[1] = playerData[1]-1
                moved = True
        elif direction == 'west':
            if playerData[2] == 1:
                self.transport.write(bytes("400:Invalid Move\r\n", "utf-8"))
            else:
                playerData[2] = playerData[2]-1
                moved = True
        elif direction == 'east':
            if playerData[2] == self.factory.gridXSize-1:
                self.transport.write(bytes("400:Invalid Move\r\n", "utf-8"))
            else:
                playerData[2] = playerData[2]+1
                moved = True
        else:
            self.transport.write(bytes("400:bad request\r\n", "utf-8"))
        if moved == True:
            self.checkTreasure()
            self.sendPlayerLocation()
            toSend = bytes(f"101:{playerData[0]}, {playerData[1]}, {playerData[2]}, {playerData[3]}\r\n", "utf-8")
            self.transport.write(toSend)

    def connectionLost(self, reason):
        if self.loggedIn == True:
            self.factory.listPlayers[self][4] = False
            for player in self.factory.listPlayers.keys():
                player.transport.write(bytes(f"101:Player {self.factory.listPlayers[self][0]} has disconnected\r\n", "utf-8"))

class ReadWriteContentFactory(Factory):
    listPlayers = {}
    listObjects = {}
    gridXSize = 20
    gridYSize = 20

    def __init__(self):
        numberDone = 1
        while numberDone < 21:
            self.listObjects[numberDone] = [randrange(21), randrange(21), randrange(1,6)]
            numberDone = numberDone+1
        print(self.listObjects)

    def buildProtocol(self, addr):
        return ReadWriteContent(self)

reactor.listenTCP(8000, ReadWriteContentFactory())
reactor.run()
