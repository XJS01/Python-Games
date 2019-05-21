"""
Jason Xiong
Uno Game
"""

import random

class UnoCard:
    '''represents an Uno card
    attributes:
      rank: int from 0 to 9 and reverse, skip, and draw two
      color: string'''

    def __init__(self,rank,color):
        '''UnoCard(rank,color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color

    def __str__(self):
        '''str(Unocard) -> str'''
        return(str(self.color)+' '+str(self.rank))
    def get_rank(self):
        return self.rank #returns rank of the card
    def get_color(self):
        return self.color
    def is_match(self,other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        return (self.color == other.color) or (self.rank == other.rank) or (self.color=='special')
    def change_color(self, color):
        self.color=color

class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''

    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for a in range(4):
            self.deck.append(UnoCard('wild', 'special'))
            self.deck.append(UnoCard('wild draw four', 'unique'))
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0,color))  # one 0 of each color
            for i in range(2):
                self.deck.append(UnoCard('reverse', color))
                self.deck.append(UnoCard('draw two', color))
                self.deck.append(UnoCard('skip', color))
                for n in range(1,10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n,color))
        random.shuffle(self.deck)  # shuffle the deck

    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+str(len(self.deck))+' cards remaining.'

    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0

    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self,pile):
        '''UnoDeck.reset_deck(pile)
        resets the deck from the pile'''
        self.deck = pile.reset_pile() # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck

class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self,deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has '+str(self.pile[-1])+' on top.'

    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self,card):
        '''UnoPile.add_card(card)
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck
    
    def len_of_pile(self):
        return len(self.pile) #returns the length of the pile

class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''

    def __init__(self,name,deck):
        '''UnoPlayer(name,deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name)+' has '+str(len(self.hand))+' cards.'

    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self,deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self,card,pile):
        '''UnoPlayer.play_card(card,pile)
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self,deck,pile):
        '''UnoPlayer.take_turn(deck,pile)
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        # print player info
        print(self.name+", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        uniqueCheck=[]
        uniqueCheck=[card for card in self.hand if card.get_rank()=='wild draw four']
        if all(match.get_color() != topcard.get_color() for match in matches) and len(uniqueCheck)>0:
            for t in range(len(uniqueCheck)):
                matches.append(uniqueCheck[t])
        if len(matches) > 0:  # can play
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index+1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice-1],pile)        

        else:
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard) or newcard.get_rank()=='unique': # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
            else:   # still can't play
                print("Sorry, you still can't play.")
            input("Press enter to continue.")

def play_uno(numPlayers):
    '''play_uno(numPlayers)
    plays a game of Uno with numPlayers'''
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    # set up the players
    playerList = []
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        name = input('Player #'+str(n+1)+', enter your name: ')
        playerList.append(UnoPlayer(name,deck))
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numPlayers)
    # play the game
    while True:
        # take a turn
        a=pile.top_card()
        if a.get_rank()=='skip' and pile.len_of_pile()>1:#check for special cards
            print('your turn has been skipped')
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers #skip the next player
        elif a.get_rank()=='wild' and pile.len_of_pile()>1:
            z='color'
            while z not in ['red', 'blue', 'green', 'yellow']: 
                z=input('Enter the color you want: ')
                a.change_color(z)
            print('the color has been changed to ' + z)
        elif a.get_rank()=='wild draw four' and pile.len_of_pile()>1:
            z='color'
            while z not in ['red', 'blue', 'green', 'yellow']: 
                z=input('Enter the color you want: ')
                a.change_color(z)
            for w in range(4):
                playerList[currentPlayerNum].draw_card(deck)
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers    
            print('you drew 4 cards and your turn was skipped')
            print('the color has been changed to ' + z)        
        elif a.get_rank() =='draw two' and pile.len_of_pile()>1:
            playerList[currentPlayerNum].draw_card(deck)#draw cards
            playerList[currentPlayerNum].draw_card(deck)
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers#skip a turn
            print('you drew two cards and your turn was skipped')
        elif a.get_rank() =='reverse' and pile.len_of_pile()>1:
            playerList.reverse()#flip the list
            currentPlayerNum=(len(playerList)-currentPlayerNum+1)% numPlayers#get new starting position
            print('player order was reversed')
                # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        playerList[currentPlayerNum].take_turn(deck,pile)
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name()+" wins!")
            print("Thanks for playing!")
            break
        # go to the next player
        currentPlayerNum = (currentPlayerNum + 1) % numPlayers
numPlayers=int(input("Enter the number of players: ")
play_uno(numPlayers)
