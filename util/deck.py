'''
TODO:

Change prints to errors

Add jokers to deck 
handle character creation draw(including jokers)

Eliminate lowest two for character creation(may be moved)
'''

import itertools, random
import sys
from collections import deque
from typing import Tuple

class DeckOfCards:
	_cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
	
	def __init__(self):
		self._deck = deque(itertools.product(_cards,['Spades','Hearts'
			,'Clubs','Diamonds']))
		self._convertdic = {'Spades': '4','Hearts':'3','Diamonds': '2'
		, 'Clubs':'1','2':'4','3':'6','4':'6','5':'6','6':'6','7':'6','8':'6'
		,'9':'8','10':'8','J':'8','Q':'10','K':'10','A':'12','JK':'12'}

#
#Shuffles current deck list using random.shuffle() method
#
	def shuffle(self) -> 'None':
		random.shuffle(self._deck)
#
#Draw card and place at the end of the deck
#
	def drawcard(self) -> Tuple[str,str]:
		x = self._deck.popleft()
		self._deck.append(x)
		return(x)
#
#draw a card then immediately shuffle
#
	def drawandshuffle(self) -> Tuple[str,str]:
		x = self._deck[0]
		self.shuffle()
		return(x)
#
#Draw <num> number of cards and returns a list of the cards drawn
#
	def drawmultiple(self, num: 'int'):
		if num<1 or num>52:
			print("out of range error")
			return
		l = []
		for i in range(0,num):
			l.append(self.drawcard())
		return l
#
#Draws a card then prints the card in its dice format
#e.g.  8 of spades will print 4d6, A of Spades prints 4d12
#
	def dicedraw(self):
		return self.cardtodice(self.drawcard())

#
#Prints dice representation of card, requries card tuple passed 
#shouldnt be called externally(???????)
#
	def cardtodice(self,card):
		print(self._convertdic.get(card[1])+"d"+self._convertdic.get(card[0]))

#
#generator function for yielding cards
#probably not needed since its at most 52 cards
#possibly deleted later
#
	def gencards(self,num):
		for i in range(0,num):
			yield self._deck[i]
#
#Prints the conversion dictionary for taking a card and getting its dice 
#representation
#
	def __printdic(self) -> 'None':
		print(self._convertdic)
#
#Prints card number and suit
#
	def __printcard(self,card) -> 'None':
		print(str(x[0])+" of "+str(x[1]))
#
#Prints the whole deck of tuple cards
#
	def printdeck(self) -> 'None':
		print(self._deck)
#
#Joker check function used for creating a character
#worked on later
#
	def jokercheck(self,card)-> bool:
		if card[0]=='JK':
			return True
		return False

	def convertlisttodice(self,cardlist):
		dicelist = []
		for x in cardlist:
			dicelist.append((self._convertdic.get(x[1]),self._convertdic.get(x[0])))
		return dicelist