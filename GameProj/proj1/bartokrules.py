from thing import Thing
from rule import Rule
import random
from enums import BartokRule

class BartokRules(Thing):
    def __init__(self):
        # Place Rules below in order of priority
        self.rules = [PlaceDraw2Rule(), Draw2Rule(), PlaceCardRule(), DrawCard()]

class PlaceDraw2Rule(Rule):
    def __init__(self):
        self.name = BartokRule.PLACEDRAW2

    def canAct(self, player):
        centerCard = player.env['center'].checkTopCard()
        hasDraw2 = False
        for card in player.hand:
            if card.rank == '2':
                hasDraw2 = True
        return centerCard.rank == '2' and hasDraw2

    def act(self, player):
        draw2Idx = 0
        for i in range(0, len(player.hand)):
            if player.hand[i].rank == '2':
                draw2Idx = i
                break
        player.env['center'].put(player.removeCardFromHand(draw2Idx))
        player.env['currPlayer'] = self.nextPlayer(player)


class Draw2Rule(Rule):
    def __init__(self):
        self.name = BartokRule.DRAW2

    def canAct(self, player):
        centerCard = player.env['center'].checkTopCard()
        return centerCard.rank == '2'

    def act(self, player):
        # First check the number of cards left in the deck
        if player.env['deck'].isEmpty():
            # Take extra cards from center and add it to the deck
            extraCardCount = player.env['center'].numOfCards() - 1
            for i in range(0,extraCardCount):
                player.env['deck'].put(player.end['center'].takeBottom(), False)

        player.addToHand(player.env['deck'].takeTop())
        player.addToHand(player.env['deck'].takeTop())
        player.env['currPlayer'] = self.nextPlayer(player)

class PlaceCardRule(Rule):
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
                possibleCards.append(i)
        chosenCard = possibleCards.pop(random.randint(0, len(possibleCards) - 1))

        player.env['center'].put(player.removeCardFromHand(chosenCard))
        player.env['currPlayer'] = self.nextPlayer(player)

class DrawCard(Rule):
    def __init__(self):
        self.name = BartokRule.DRAWCARD

    def canAct(self, player):
        return True

    def act(self, player):
        # First check the number of cards left in the deck
        if player.env['deck'].isEmpty():
            # Take extra cards from center and add it to the deck
            extraCardCount = player.env['center'].numOfCards() - 1
            for i in range(0,extraCardCount):
                player.env['deck'].put(player.end['center'].takeBottom(), False)

        player.addToHand(player.env['deck'].takeTop())
        player.env['currPlayer'] = self.nextPlayer(player)
