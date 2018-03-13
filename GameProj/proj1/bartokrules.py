from thing import Thing
from rule import Rule
import random
from enums import BartokRuleEnum, Direction

class BartokRules(Thing):
    def __init__(self):
        # Place Rules below in order of priority
        self.rules = [Draw2Rule(), PlaceCardRule(), DrawCardRule()]

class BartokRule(Rule):
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

    def resetDraw2Effect(self, player):
        player.env['mustDraw2'] = False
        player.env['draw2Effect'] = 0

    def checkDeck(self, player):
        if player.env['deck'].isEmpty():
            # Take extra cards from center and add it to the deck
            print("Deck is empty, adding extra cards from Center back to Deck")
            extraCardCount = player.env['center'].numOfCards() - 1
            for i in range(0,extraCardCount):
                player.env['deck'].put(player.env['center'].takeBottom(), False)


class Draw2Rule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.DRAW2

    def canAct(self, player):
        canAct = False
        hasDraw2 = False
        for card in player.hand:
            if card.rank == '2':
                hasDraw2 = True
        if player.env['mustDraw2'] and not(hasDraw2):       # mustDraw2 is only True when a player has started
            canAct = True                                   # the Draw 2 effect or added to the effect
        return canAct                                       # mustDraw2 is set back to false when a player has drawn the
                                                            # the cards

    def act(self, player):
        super(Draw2Rule, self).checkDeck(player)

        drawCount = player.env['draw2Effect'] * 2
        print("Your only option is to draw", drawCount, "card(s).")
        print("Automatically adding", drawCount, "card(s) to your hand.")
        for i in range(drawCount):
            newCard = player.env['deck'].takeTop()
            player.addToHand(newCard)
            print("({}, {})".format(newCard.rank, newCard.suit))
            super(Draw2Rule, self).checkDeck(player)

        super(Draw2Rule, self).resetDraw2Effect(player)
        player.env['currPlayer'] = super(Draw2Rule, self).nextPlayer(player)


class PlaceCardRule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.PLACECARD

    def canAct(self, player):
        centerCard = player.env['center'].checkTopCard()
        canPlaceCard = False
        for card in player.hand:
            if card.equalsRank(centerCard) or card.equalsSuit(centerCard) or card.rank == '2':
                canPlaceCard = True
                break
        return canPlaceCard

    def act(self, player):

        def letUserPlaceCard(player, possibleCards):
            print("Your Hand")
            print("INDEX - (CARD RANK, CARD SUIT)")
            index = 0
            for card in player.hand:
                if index in possibleCards:
                    print("{} - ({}, {}) ** Can play this card **".format(index, card.rank, card.suit))
                else:
                    print("{} - ({}, {})".format(index, card.rank, card.suit))
                index += 1

            chosenCard = -1
            while(not(chosenCard in possibleCards)):
                try:
                    chosenCard = int(input("Enter the INDEX of the card you would like to place.\n> "))
                except(ValueError):
                    print("Invalid input. Input must be an integer.")
                    chosenCard = -1
                if not(chosenCard in possibleCards):
                    print(f"You cannot place that card \nPossible card indexes to play {possibleCards}")

            player.env['center'].put(player.removeCardFromHand(chosenCard))
            centerCard = player.env['center'].checkTopCard()
            print("Player {} placed ({}, {}) in Center".format(player.index + 1, centerCard.rank, centerCard.suit))
            return centerCard


        # This is true only when another player has started the Draw 2 effect
        # and the current player has the option to add to that effect
        if (player.env['mustDraw2']):
            choice = -1
            while(choice != 0 or choice != 1):
                try:
                    choice = int(input("Draw 2 effect started. Add Draw 2 card to increase Draw 2 effect?\n0 - No\n1 - Yes\n> "))
                except(ValueError):
                    print("Invalid input. Input must be an integer.")
                    choice = -1
                # Player chose No
                if (choice == 0):
                    print("Wow, you're a pretty nice person. The next player should buy you a drink.")
                    super(PlaceCardRule, self).checkDeck(player)

                    drawCount = player.env['draw2Effect'] * 2
                    for i in range(drawCount):
                        player.addToHand(player.env['deck'].takeTop())
                        super(PlaceCardRule, self).checkDeck(player)

                    print(f"{drawCount} cards added to you hand")
                    super(PlaceCardRule, self).resetDraw2Effect(player)
                    break
                # Player chose Yes
                elif(choice == 1):
                    possibleCards = list()
                    for i in range(0, len(player.hand)):
                        if player.hand[i].rank == '2': possibleCards.append(i)
                    letUserPlaceCard(player, possibleCards)
                    player.env['draw2Effect'] += 1
                    break
                else:
                    print("Invalid input. Either input 0 for No or 1 for Yes")
        else:
            centerCard = player.env['center'].checkTopCard()
            possibleCards = list()
            for i in range(0, len(player.hand)):
                if player.hand[i].equalsRank(centerCard) or player.hand[i].equalsSuit(centerCard) or player.hand[i].rank == '2':
                    possibleCards.append(i)
            centerCard = letUserPlaceCard(player, possibleCards)
            if centerCard.rank == '2':
                player.env['mustDraw2'] = True
                player.env['draw2Effect'] += 1
            else:
                super(PlaceCardRule, self).resetDraw2Effect(player)

        player.env['currPlayer'] = super(PlaceCardRule, self).nextPlayer(player)


class DrawCardRule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.DRAWCARD

    def canAct(self, player):
        return True

    def act(self, player):
        super(DrawCardRule, self).checkDeck(player)

        print("Your only option is to draw from the deck")
        print("Automatically adding one card to your hand.")
        newCard = player.env['deck'].takeTop()
        player.addToHand(newCard)
        print("({}, {})".format(newCard.rank, newCard.suit))
        player.env['currPlayer'] = super(DrawCardRule, self).nextPlayer(player)
