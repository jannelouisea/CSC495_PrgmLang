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
            hasDraw2 = False
            for card in player.hand:
                if card.rank == '2':
                    hasDraw2 = True
            if (not hasDraw2):
                direction = player.env['direction']
                lptd2 = player.env['lptd2']
                currPlayer = player.env['currPlayer']
                endPlayer = player.env['numOfPlayers'] - 1

                if (lptd2 == -1):
                    canAct = True
                elif (direction == Direction.CLOCKWISE):
                    if(currPlayer == 0 and lptd2 != endPlayer):
                        canAct = True
                elif (direction == Direction.CRCLOCKWISE):
                    if(currPlayer == endPlayer and lptd2 != 0):
                        canAct = True
                else:
                    prevPlayer = currPlayer - (direction.value)
                    if(lptd2 != prevPlayer):
                        canAct = True
        return canAct


    def act(self, player):
        self.checkDeck(player)

        # First check how many Draw 2 cards are in the center
        drawCardCount = 0
        center = player.env['center']
        numOfPlayers = player.env['numOfPlayers']
        if numOfPlayers > 2:
            for i in range(center.numOfCards() - 1, -1, -1):
                card = center.cards[i]
                if card.rank == '2':
                    drawCardCount += 2
                else:
                    break
        else:
            drawCardCount = 2

        print("Your only option is to draw", drawCardCount, "card(s).")
        print("Automatically adding", drawCardCount, "card(s) to your hand.")
        for i in range(drawCardCount):
            player.addToHand(player.env['deck'].takeTop())
            self.checkDeck(player)

        player.env['lptd2'] = player.index
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
            if card.equalsRank(centerCard) or card.equalsSuit(centerCard) or card.rank == '2':
                canPlaceCard = True
                break
        return canPlaceCard

    def act(self, player):
        centerCard = player.env['center'].checkTopCard()
        possibleCards = list()
        for i in range(0, len(player.hand)):
            if player.hand[i].equalsRank(centerCard) or player.hand[i].equalsSuit(centerCard) or player.hand[i].rank == '2':
                possibleCards.append(i)

        print("Your hand: ")
        index = 0
        for card in player.hand:
            if index in possibleCards:
                print("{} - ({} {}) ** Can play this card **".format(index, card.rank, card.suit))
            else:
                print("{} - ({} {})".format(index, card.rank, card.suit))
            index += 1

        chosenCard = -1
        while(not(chosenCard in possibleCards)):
            chosenCard = int(input("Which card would you like to play?\n"))
            if not(chosenCard in possibleCards):
                print(f"You cannot play that card \nPossible card(s) to play {possibleCards}")

        player.env['center'].put(player.removeCardFromHand(chosenCard))

        centerCard = player.env['center'].checkTopCard()
        print("Player {} placed ({} {}) in Center".format(player.index + 1, centerCard.rank, centerCard.suit))

        numOfPlayers = player.env['numOfPlayers']
        if numOfPlayers == 2 and centerCard.rank != '2':
            player.env['lptd2'] = -1  # Resets the Draw 2 Logic

        player.env['currPlayer'] = super(PlaceCardRule, self).nextPlayer(player)

class DrawCard(BartokRuleNext):
    def __init__(self):
        self.name = BartokRule.DRAWCARD

    def canAct(self, player):
        return True

    def act(self, player):
        self.checkDeck(player)

        print("Your only option is to draw from the deck")
        print("Automatically adding one card to your hand.")
        player.addToHand(player.env['deck'].takeTop())
        player.env['currPlayer'] = super(DrawCard, self).nextPlayer(player)

    def checkDeck(self, player):
        if player.env['deck'].isEmpty():
            # Take extra cards from center and add it to the deck
            print("Deck is empty, adding extra cards from Center back to Deck")
            extraCardCount = player.env['center'].numOfCards() - 1
            for i in range(0,extraCardCount):
                player.env['deck'].put(player.env['center'].takeBottom(), False)
