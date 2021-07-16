def getInstructions():
    text = ["You have been arrested for a crime, as has your partner.",
            "You are both being interrogated.",
            "You can either stay silent and try to cooperate with your partner, or defect and betray them to the detectives.",
            "",
            "If you both cooperate-- you each serve a year in prison.",
            "If you cooperate and your partner defects-- you serve three years and they serve none (and vice-versa.)",
            "If you both betray each other-- you each serve two years.",
            "",
            "Thus our dilemma."]
    return text

def getEntropyText():
    text = ["In order to normalize results, we are going to need to introduce a source of entropy.",
            "It's easiest to calculate this with a whole number percentage.",
            "Please enter a positive integer (1-100): "]

    return text

def getMaxGamesText():
    text = ["There are optimal strategies when the number of games is known (namely, always defect.)",
            "This is boring.",
            "However, if neither player has this information beforehand-- various strategies open up.",
            "What is the maximum number of games you want to play?",
            "Please enter a positive integer (1-256): "]

    return text
