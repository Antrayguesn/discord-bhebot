# Blind test bot!

from bhebot.singleton import Singleton

class Game(metaclass = Singleton):
    isPlaying = False
    players = {}
    currentSong = ""
    currentAuthor = ""
    playersGoodSong = []
    playersGoodAuthor= []
    botChanel = None

    def start(self) :
        self.isPlaying = True

    def stop(self) :
        self.isPlaying = False

    def restart(self) :
        self.currentSong = ""
        self.currentAuthor = ""
        self.players = {}

    def addPlayer(self, player) :
        self.players[player] = 0

    def getScores(self):
        strToSend = ""
        for player in self.players :
            strToSend += "{} à {} points\n".format(player.mention, self.players[player])
        return strToSend


    def incrementScore(self, player: str) :
        self.players[player] += 1

    def setCurrentSong(self, currentSong: str, currentAuthor: str) :
        self.currentSong = currentSong
        self.currentAuthor = currentAuthor

    def processReponse(message: str) :
        playerSong = messageCopied.content.split("-")[0].strip() if "-" in messageCopied.content else messageCopied.content.strip()
        playerAuthor = messageCopied.content.split("-")[1].strip() if "-" in messageCopied.content else messageCopied.content.strip()

        if messageCopied.author in self.playersGoodSong and messageCopied.author in self.playersGoodAuthor :
            return

        wrongKey = WrongKey()
        strToSend = ""

        if messageCopied.author not in self.playersGoodSong:
            intNbErrorSong, falseTrueErrorSong = wrongKey.findError(self.currentSong, playerSong)

            if intNbErrorSong < 0 :
                strToSend += ""

            elif intNbErrorSong == 0:
                self.playersGoodSong.append(messageCopied.author)
                strToSend += "{0} est trop fort (+1 pour la chanson)\n"
                self.incrementScore(messageCopied.author)

            elif (intNbErrorSong == falseTrueErrorSong) and falseTrueErrorSong <= 3:
                self.playersGoodSong.append(messageCopied.author)
                strToSend += "Ok {0}, mais écris mieux la prochaine fois (+1 pour la chanson)\n"
                self.incrementScore(messageCopied.author)

        if messageCopied.author not in self.playersGoodAuthor :
            intNbErrorAuthor, falseTrueErrorAuhtor = wrongKey.findError(self.currentAuthor, playerAuthor)

            if intNbErrorAuthor == 0:
                self.playersGoodAuthor.append(messageCopied.author)
                strToSend += "{0} est trop fort (+1 pour l\'auteur)\n"
                self.incrementScore(messageCopied.author)

            elif intNbErrorAuthor > 0 and (intNbErrorAuthor == falseTrueErrorAuhtor) and falseTrueErrorAuhtor <= 3:
                self.playersGoodAuthor.append(messageCopied.author)
                strToSend += "Ok {0}, mais écris mieux la prochaine fois (+1 pour l\'auteur)\n"
                self.incrementScore(messageCopied.author)

        if strToSend == "":
            strToSend += 'bhèèèèè {0}\n'

