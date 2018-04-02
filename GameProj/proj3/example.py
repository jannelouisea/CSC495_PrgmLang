centerCard = player.env['center'].checkTopCard()
possibleCards = list()	# Holds a list of card indexes not the actual cards
for i in range(0, len(player.hand)):
    if (... equals suit or rank):
        possibleCards.append(i)

print('Your hand')
index = 0
for card in player.hand
    if index in possibleCards:
        print("{} - ({} {}) ** Can play this card **".format(index, card.rank, card.suit))
    else:
        print("{} - ({} {})".format(index, card.rank, card.suit))
    index += 1

chosenCard = -1
while(not(chosenCard in possibleCards)):
    chosenCard = int(input("Which card would you like to play?\n> "))
    if not(chosenCard in possibleCards):
        print("You cannot play that card\nPossible cards to play {}".format(possibleCards))

player.env['center'].put(player.removeCardFromHand(chosenCard))
... other stuff

