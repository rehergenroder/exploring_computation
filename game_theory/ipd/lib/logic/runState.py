import quantumrandom

class runState():
    def __init__(self, e, n):
        self.gameLength = int(quantumrandom.randint(1, n))
        self.currentGame = 0
        self.p1_moves = []
        self.p2_moves = []
        self.entropy = e

    def __str__(self):
        return "Run State:\nn = " + str(self.gameLength)

    def updateGame(self, p1, p2):
        self.currentGame += 1
        self.p1_moves.append(p1.choice)
        self.p2_moves.append(p2.choice)

        if(p1.choice == 0 and p2.choice == 0):
            p1.years += 1
            p2.years += 1
        elif(p1.choice == 0 and p2.choice == 1):
            p1.years += 3
            p1.minYears += 2
        elif(p1.choice == 1 and p2.choice == 0):
            p2.years += 3
            p2.minYears += 2
        else:
            p1.years += 2
            p1.minYears += 2
            p2.years += 2
            p2.minYears += 2
        
    def getMoves(self, p1, p2):
        text = []
        buff = ""
        for x in self.p1_moves:
            buff += str(x)
        text.append(buff)
        buff = ""
        for x in self.p2_moves:
            buff += str(x)
        text.append(buff)
        buff = "Player 1 served " + str(p1.years) + ". They could have served " + str(p1.minYears) + " with perfect knowledge. Entropy = " + str(p1.entropyInvoked)
        text.append(buff)
        buff = "Player 2 served " + str(p2.years) + ". They could have served " + str(p2.minYears) + " with perfect knowledge. Entropy = " + str(p2.entropyInvoked)
        text.append(buff)
        return text
