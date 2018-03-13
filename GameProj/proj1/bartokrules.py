from thing import Thing
from rule import Rule
import random
from enums import BartokRule, Direction

class BartokRules(Thing):
    def __init__(self):
        # Place Rules below in order of priority
        self.rules = [Draw2Rule(), PlaceCardRule(), DrawCard()]

class BartokRuleNext(Rule):
    def nextPlayer(self, player):
        numOfPlayers = player.env['numOfPlayers']
        direction = player.env['direction'].value
        currPlayer = player.env['currPlayer']
        nextPlayer = currPlayer + direction
        if nextPlayer == numOfPlayers:
            nextPlayer = 0
        elif nextPlayer == -1:
            nextPlayer = numOfPlayers - 1
        return nextPlayer

class Draw2Rule(BartokRuleNext):
    def __init__(self):
        self.name = BartokRule.DRAW2

    def canAct(self, player):
        canAct = False
        centerCard = player.env['center'].checkTopCard()
        if (centerCard.rank == '2'):

            direction = player.env['direction']
            lpdt2 = player.env['lpdt2']
            currPlayer = player.env['currPlayer']
            endPlayer = player.env['numOfPlayers'] - 1

            if (lpdt2 == -1):
                canAct = True
            elif (direction == Direction.CLOCKWISE):
                if(currPlayer == 0 and lpdt2 != endPlayer):
                    canAct = True
            elif (direction == Direction.CRCLOCKWISE):
                if(currPlayer == endPlayer and lpdt2 != 0):
                    canAct = True
            else:
                prevPlayer = currPlayer - (direction.value)
                if(lpdt2 != prevPlayer):
                    canAct = True
        return canAct


    def act(self, player):
        self.checkDeck(player)

        # First check how many Draw 2 cards are in the center
        drawCardCount = 0
        center = player.env['center']
        for i in range(center.numOfCards() - 1, -1, -1):
            card = center.cards[i]
            if card.rank == '2':
                drawCardCount += 2
            else:
                break

        print("Player", player.index, "draws", drawCardCount, "Card(s) from Deck")
        for i in range(drawCardCount):
            player.addToHand(player.env['deck'].takeTop())
            self.checkDeck(player)

        # For simulation purposes
        centerCard = player.env['center'].checkTopCard()
        possibleCards = list()
        for i in range(0, len(player.hand)):
            if player.hand[i].equalsRank(centerCard) or player.hand[i].equalsSuit(centerCard):
                possibleCards.append(i)
        chosenCard = possibleCards.pop(random.randint(0, len(possibleCards) - 1))

        player.env['center'].put(player.removeCardFromHand(chosenCard))

        centerCard = player.env['center'].checkTopCard()
        print("Player {} placed ({} {}) in Center".format(player.index, centerCard.rank, centerCard.suit))
        # For simulation purposes

        player.env['currPlayer'] = super(Draw2Rule, self).nextPlayer(player)

    def checkDeck(self, player):
        if player.env['deck'].isEmpty():
            # Take extra cards from center and add it to the deck
            print("Deck is empty, adding extra cards from Center back to Deck")
            extraCardCount = player.env['center'].numOfCards() - 1
            for i in range(0,extraCardCount):
                player.env['deck'].put(player.env['center'].takeBottom(), False)

class PlaceCardRule(BartokRuleNext):
    def __init__(self):
        self.name = BartokRule.PLACECARD

    def canAct(self, player):
        centerCard = player.env['center'].checkTopCard()
        canPlaceCard = False
        for card in player.hand:
            if card.equalsRank(centerCard) or card.equalsSuit(centerCard):
                canPlaceCard = True
                break
        return canPlaceCard

    def act(self, player):
        centerCard = player.env['center'].checkTopCard()
        possibleCards = list()
        for i in range(0, len(player.hand)):
            if player.hand[i].equalsRank(centerCard) or player.hand[i].equalsSuit(centerCard):
                possibleCards.append(player.hand[i])
       # chosenCard = possibleCards.pop(random.randint(0, len(possibleCards) - 1))
        print("Your full hand: ")
        player.reflect()
        print()
        print("Your possible cards for this turn: ", possibleCards)


        chosenCard = 10
        while( chosenCard > len(possibleCards)):
            chosenCard = int(input("Which card would you like to play?"))
        print()

        player.env['center'].put(player.removeCardFromHand(chosenCard))

        centerCard = player.env['center'].checkTopCard()
        print("Player {} placed ({} {}) in Center".format(player.index, centerCard.rank, centerCard.suit))
        player.env['currPlayer'] = super(PlaceCardRule, self).nextPlayer(player)

class DrawCard(BartokRuleNext):
    def __init__(self):
        self.name = BartokRule.DRAWCARD

    def canAct(self, player):
        return True

    def act(self, player):
        self.checkDeck(player)

        print("Player", player.index, "draws 1 Card from Deck")
        player.addToHand(player.env['deck'].takeTop())
        player.env['currPlayer'] = super(DrawCard, self).nextPlayer(player)

    def checkDeck(self, player):
        if player.env['deck'].isEmpty():
            # Take extra cards from center and add it to the deck
            print("Deck is empty, adding extra cards from Center back to Deck")
            extraCardCount = player.env['center'].numOfCards() - 1
            for i in range(0,extraCardCount):
                player.env['deck'].put(player.env['center'].takeBottom(), False)
