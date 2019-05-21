'''
Jason Xiong
Dino Game

Rules:
Each player takes one turn every round
Each turn, the player starts with 13 dice in the unused pile (6 green, 4 yellow, 3 red)
The green dice has 3 dinos, 2 leaves, 1 foot
The yellow dice has 2 dinos, 2 leaves, 2 feet
The red dice has 1 dino, 2 leaves, 3 feet
A player starts the turn by rolling three random dice
If a leaf is rolled, the dice is put back into the unused pile
If the dino or foot is rolled, the dice is put put into the used pile
The number of dinos and feet are tallied
If the player evers has three or more feet tallied for the turn, the turn ends and the player gains no points
The player now has the option to roll three more random dice
If the player refuses to roll or there are no dice remaining in the unused pile, the number of dinos tallied for the round are added to the players score
The player with the most points at the end of all the rounds wins
'''

import random

class Die:
    '''Die class'''

    def __init__(self,sides=6):
        '''Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides,int):
            self.numSides = sides
            self.sides = list(range(1,sides+1))
        else:  # use the list/tuple provided 
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+str(self.numSides)+'-sided die with '+\
               str(self.get_top())+' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self,value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value

### end Die class ###

class DinoDie(Die):
    '''implements the dice for Dino Hunt'''

    def __init__(self, color):
        self.color=color
        self.sides=[]
        while self.color not in ['green', 'yellow', 'red']:
            self.color=input('Choose a color of Dino die from green, yellow, or red: ')
        if self.color=='green':
            for a in range(3):
                self.sides.append('dino')
            for b in range(2):
                self.sides.append('leaf')
            for c in range(1):
                self.sides.append('foot')
        elif self.color=='yellow':
            for a in range(2):
                self.sides.append('dino')
            for b in range(2):
                self.sides.append('leaf')
            for c in range(2):
                self.sides.append('foot')
        elif self.color=='red':
            for a in range(1):
                self.sides.append('dino')
            for b in range(2):
                self.sides.append('leaf')
            for c in range(3):
                self.sides.append('foot')        
        self.numSides=6
        self.roll()
        
    def get_color(self):
        return self.color
    
    def __str__(self):
        return 'A ' +self.color+ ' color Dino die with a ' +self.get_top()+' on top.'
        
                
class DinoPlayer:
    '''implements a player of Dino Hunt'''
    def __init__(self, name):
        self.name=name
        self.points=0
        self.dice=[]
        for a in range(6):
            self.dice.append(DinoDie('green'))
        for b in range(4):
            self.dice.append(DinoDie('yellow'))
        for c in range(3):
            self.dice.append(DinoDie('red'))
        random.shuffle(self.dice)
    def __str__(self):
        return self.name+' has ' +str(self.points)+' points.'
    
    def get_points(self):
        return self.points
    
    def get_name(self):
        return self.name
    
    def take_turn(self):
        response='x'
        self.dice=[]
        for a in range(6):
            self.dice.append(DinoDie('green'))
        for b in range(4):
            self.dice.append(DinoDie('yellow'))
        for c in range(3):
            self.dice.append(DinoDie('red'))
        random.shuffle(self.dice)        
        dinoCount=0
        footCount=0
        random.shuffle(self.dice)
        print(' ')
        print(' ')
        print(self.name+", it's your turn.")
        remainingDice=len(self.dice)
        print('You have ' +str(remainingDice)+' dice remaining.')
        greenList=[die for die in self.dice if die.get_color()=='green']
        yellowList=[die for die in self.dice if die.get_color()=='yellow']
        redList=[die for die in self.dice if die.get_color()=='red']
        numGreen=len(greenList)
        numYellow=len(yellowList)
        numRed=len(redList)
        print(str(numGreen)+' green, '+str(numYellow)+' yellow, '+ str(numRed)+' red')        
        
        while True:
            if response=='n':
                break
            
            choices=[]
            input('Press enter to select dice and roll: ')
            if remainingDice>=3:
                for x in range(3):
                    randomDie=self.dice.pop()
                    choices.append(randomDie)        
                for die in choices:
                    die.roll()
                    print(die)
                    if die.get_top()=='dino':
                        dinoCount+=1
                    if die.get_top()=='foot':
                        footCount+=1
                    if die.get_top()=='leaf':
                        self.dice.append(die)
            else:
                for x in range(remainingDice):
                    randomDie=self.dice.pop()
                    choices.append(randomDie)        
                for die in choices:
                    die.roll()
                    print(die)
                    if die.get_top()=='dino':
                        dinoCount+=1
                    if die.get_top()=='foot':
                        footCount+=1
                    if die.get_top()=='leaf':
                        self.dice.append(die) 
            if footCount>=3:
                print('Too bad -- you got stomped!')
                print(' ')
                break
            elif remainingDice==0:
                print('you have no remaining dice')
                print('you earned '+ str(dinoCount)+ ' points this round')
                self.points+=dinoCount
                break
            elif footCount<=3 and remainingDice>0:
                print('This turn so far: ' +str(dinoCount) +' dinos '+ str(footCount)+' feet')
                remainingDice=len(self.dice)
                print('You have ' +str(remainingDice)+' dice remaining.')
                greenList=[die for die in self.dice if die.get_color()=='green']
                yellowList=[die for die in self.dice if die.get_color()=='yellow']
                redList=[die for die in self.dice if die.get_color()=='red']
                numGreen=len(greenList)
                numYellow=len(yellowList)
                numRed=len(redList)
                print(str(numGreen)+' green, '+str(numYellow)+' yellow, '+ str(numRed)+' red')
                response='x'
                while response not in 'yn':
                    response=input('Do you want to roll again? (y/n)')
                    if response.lower()=='n':
                        self.points+=dinoCount
                        print(' ')
                        print(' ')
                        
                    elif response.lower()=='y':
                        pass
 
        
def play_dino_hunt(numPlayers,numRounds):
    '''play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
      numPlayers is the number of players
      numRounds is the number of turns per player'''
    playerList=[]
    playerCount=1
    winList=[]
    maxScore=0
    winName=''
    roundCount=1
    for n in range(numPlayers):
        name=input('Player '+str(n+1)+', what is your name?')
        playerList.append(DinoPlayer(name))
    currentPlayerNum = random.randrange(numPlayers)
    for x in range(numRounds):
        print('ROUND ' +str(roundCount))
        roundCount+=1
        print(' ')
        print(' ')
        for player in playerList:
            for player in playerList:
                print(player.get_name()+' has ' +str(player.get_points())+' points.')
            playerList[currentPlayerNum].take_turn()          
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
    for player in playerList:
        if player.get_points()>maxScore:
            maxScore=player.get_points()
            winName=player.get_name()
            if len(winList)>0:
                winList=[]
                winList.append(player.get_name())
            else:
                winList.append(player.get_name())
        elif player.get_points()==maxScore:
            winList.append(player.get_name())            
    if len(winList)==1:          
        print('We have a winner!')
        print(winName+' has ' + str(maxScore)+' points.')
    elif len(winList)>1:
        print('We have a tie.')
        for winner in winList:
            print(winner.get_name()+' has ' + str(maxScore)+' points.') 
    
numPlayers=int(input("Please enter the number of players: "))
numRounds=int(input("Please enter the number of rounds: "))
play_dino_hunt(numPlayers,numRounds)    
    

