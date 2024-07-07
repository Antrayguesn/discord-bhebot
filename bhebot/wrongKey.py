import re
from bhebot.singleton import Singleton

keyboardLeter = {
"a":["&","z","q"],
"z":["é","a","e","s"],
"e":["\"","r","d","z"],
"r":["\'","t","f","e"],
"t":["(","y","r","g"],
"y":["-","u","h","t"],
"u":["è","i","j","y"],
"i":["_","o","k","u"],
"o":["ç","p","l","i"],
"p":["o","à","^","m"],
"q":["a","s","w"],
"s":["q","x","z","d"],
"d":["e","c","f","s"],
"f":["r","v","d","g"],
"g":["h","f","t","b"],
"h":["y","j","g","n"],
"j":["u","k","h",","],
"k":["i",";","l","j"],
"l":["m","k","o",":"],
"m":["l","ù","p","!"],
"w":["x","q"],
"x":["w","s","c"],
"c":["x","d","v"],
"v":["c","b","f"],
"b":["v","g","n"],
"n":["b","h",","],
}

class WrongKey(metaclass = Singleton) :
    keyboardASCCI = {}
    def __init__(self) :
        self.__strToAscci()

    def substract(self, a, b):
        result = []
        for i in range(len(a)) :
            result.append(abs(a[i] - b[i]))
        return result

    def nbError(self, list) :
      return len(list) - list.count(0)

    def indexWrong(self, list):
        return [i for i in range(len(list)) if list[i] > 0 ]

    def formatCompare(self, str) :
        formatStr = str.lower()
        formatStr = re.sub(r"[éèê]", "e", formatStr)
        formatStr = re.sub(r"[àâ]", "a", formatStr)
        formatStr = re.sub(r"[ô]", "o", formatStr)
        formatStr = re.sub(r"[î]", "i", formatStr)
        formatStr = re.sub(r"[ùû]", "u", formatStr)
        formatStr = re.sub(r"[ç]", "c", formatStr)
        return formatStr.encode()

    def __strToAscci(self) :
        global keyboardLeter
        for leter in keyboardLeter :
            for near in keyboardLeter[leter] :
                try :
                    self.keyboardASCCI[ord(leter)].append(ord(near))
                except KeyError  :
                    self.keyboardASCCI[ord(leter)] = []
                    self.keyboardASCCI[ord(leter)].append(ord(near))

    def findError(self, trueStr, compareStr) :


        if (len(trueStr) != len(compareStr)) :
            return (-1, -1)


        ascciStr = list(bytes(self.formatCompare(trueStr)))
        wrongAscciStr = list(bytes(self.formatCompare(compareStr)))

        diffStr = self.substract(ascciStr, wrongAscciStr)
        intNbError = self.nbError(diffStr)

        falseTrueError = 0

        wrongIndexes = self.indexWrong(diffStr)
        for j in wrongIndexes :
            if wrongAscciStr[j] in self.keyboardASCCI[ascciStr[j]] :
                falseTrueError += 1

        return (intNbError, falseTrueError)
