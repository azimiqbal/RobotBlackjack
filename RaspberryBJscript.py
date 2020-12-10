#!/usr/bin/env python3

import os, sys

#import serial
#arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
#arduinoSerialData.write('5')  https://www.meccanismocomplesso.org/en/controlling-arduino-by-raspberry-pi/

#import bluetooth
#server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#port = 1
#server_socket.bind(("",port))
#server_socket.listen(1)
#client_socket,address = server_socket.accept()
#print("Accepted connection from ",address)

#while True:
#    res = self.client_socket.recv(1024)
#    client_socket.send(res)
#    if res == 'q':
#        print ("Quit")
#        break
#    else:
#        print("Received:",res)

#client_socket.close()
#server_socket.close()

cardName = { 1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King' }
cardSuit = { 'c': 'Clubs', 'h': 'Hearts', 's': 'Spades', 'd': 'Diamonds' }
    
class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return(cardName[self.rank]+" Of "+cardSuit[self.suit])

    def getRank(self):
        return(self.rank)

    def getSuit(self):
        return(self.suit)

    def BJValue(self):
        if self.rank > 9 or self.rank == 1:
            return(10)
        else:
            return(self.rank)

    # Appends from openCV
    # deck.append(Card(rank,suit)) 
deck = []
suits = [ 'c','h','d','s' ]
score = { 'dealer': 0, 'player': 0 } # Stores total wins
hand    = { 'dealer': [],'player': [] }

for suit in suits:
    for rank in range(1,14):
        deck.append(Card(rank,suit))

def showHand(hand):
    for card in hand:
        print(card)

def showCount(hand):
    print("Count: "+str(handCount(hand)))

def handCount(hand):
    handCount=0
    for card in hand:
        handCount += card.BJValue()
    return(handCount)

def gameEnd(score):
    print("*Final Score* dealer: "+str(score['dealer'])+" You: "+str(score['player']))
    sys.exit(0)

keepPlaying = True

while keepPlaying:
    
    #Deal Cards
    
    hand['player'].append(deck.pop(0))
    hand['dealer'].append(deck.pop(0))
    
    playplayer = True
    bustedplayer = False

    while playplayer:
        os.system('cls')
        print("dealer: "+str(score['dealer'])+" You: "+str(score['player']))

        print('\ndealer Shows: '+ str(hand['dealer'][-1]))

        print('\nYour Hand:')

        showHand(hand['player'])

        showCount(hand['player'])
    
        inputCycle = True
        userInput = ''

        while inputCycle:
                        ## Player helper
            print()
            print(handCount(hand['dealer']))
            print(handCount(hand['player']))
            
            if handCount(hand['player'])<17 and handCount(hand['dealer'])<12 and handCount(hand['dealer'])>9:
                print('\nPlayer should hit. Case 1')
            elif handCount(hand['player'])>16 and handCount(hand['dealer'])<9:
                print('\nPlayer should stand. Case 2')
            elif handCount(hand['player'])>11 and handCount(hand['player'])<17 and handCount(hand['dealer'])>1 and handCount(hand['dealer'])<10:
                print('\nPlayer should stand. Case 3')
            elif handCount(hand['player'])>17:
                print('\nPlayer should stand. Case 4')
            elif handCount(hand['player'])<handCount(hand['dealer']):
                print('\nPlayer should hit. Case 5')
            elif handCount(hand['player'])<12:
                print('\nPlayer should hit. Case 6')
            else:
                print('\nNo cases met, player should fuck himself')

            userInput = input("(H)it, (S)tand, or (Q)uit: ").upper()
            if userInput == 'H' or 'S' or 'Q':
                inputCycle = False
        
        if userInput == 'H':
            hand['player'].append(deck.pop(0))
            if handCount(hand['player']) > 21:
                playplayer = False
                bustedplayer = True
        elif userInput == 'S':
            while handCount(hand['dealer'])<21 and handCount(hand['dealer'])<handCount(hand['player']):
                hand['dealer'].append(deck.pop(0))
            else:
                playdealer = False
            playplayer = False
        else:
            gameEnd(score)

    playdealer = True
    busteddealer = False

    while not bustedplayer and playdealer:
        print(handCount(hand['dealer']))
        playdealer = False
        if handCount(hand['dealer'])>21:
            playdealer = False
            busteddealer = True

    if bustedplayer:
        print('Player Busted')
        score['dealer'] += 1
    elif busteddealer:
        print('dealer Busted')
        score['player'] += 1
    elif handCount(hand['player']) > handCount(hand['dealer']):
        print('Player Wins')
        score['player'] += 1
    else:
        print('dealer Wins')
        score['dealer'] += 1
    
    print('\ndealer Hand:')
    showHand(hand['dealer'])
    showCount(hand['dealer'])

    print('\nPlayer Hand:')
    showHand(hand['player'])
    showCount(hand['player'])
    if input("\n(Q)uit or enter for next round").upper() == 'Q':
        gameEnd(score)

    del hand['dealer'][:]
    del hand['player'][:]