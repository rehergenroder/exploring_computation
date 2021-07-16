import quantumrandom

class player:
    def __init__(self, playerNumber, n, strat):
        self.id = playerNumber
        self.strat = strat
        self.randArr = quantumrandom.get_data(array_length = n)
        self.entropyArr = quantumrandom.get_data(array_length = n)
        self.choice = -1
        self.years = 0
        self.minYears = 0
        self.entropyInvoked = 0

    def __str__(self):
        return "Player " + str(self.id) + " "

    def makeChoice(self, playerChoices, opponentChoices, numPlayed, entropy):
        ### RANDOM ###
        if self.strat == "Random":
            self.choice = self.randArr[numPlayed] % 2
        ### Tit for TAT ###
        elif self.strat == "Tit for Tat":
            if len(opponentChoices) == 0:
                self.choice = 0
            elif opponentChoices[-1] == 1:
                self.choice = 1
            else:
                self.choice = 0
        ### Tit for Two Tat###
        elif self.strat == "Tit for Two Tat":
            if len(opponentChoices) < 2:
                self.choice = 0;
            elif opponentChoices[-1] == 1 and opponentChoices[-2] == 1:
                self.choice = 1
            else:
                self.choice = 0
        ### GRIM ###
        elif self.strat == "GRIM":
            if 1 in opponentChoices:
                self.choice = 1
            else:
                self.choice = 0
        ### PAVLOV ###
        elif self.strat == "Pavlov":
            if len(opponentChoices) == 0:
                self.choice = 0
            elif opponentChoices[-1] != playerChoices[-1]:
                self.choice = (self.choice + 1) % 2

        ### ENTROPY ###
        if self.randArr[numPlayed] % ( 100 // entropy) == 0:
            self.choice = self.entropyArr[numPlayed] % 2
            self.entropyInvoked += 1
