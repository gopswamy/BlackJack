# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = [] 
        

    def __str__(self):
        s = "Hand contains"
        for c in self.cards:
            s += " " + str(c)
        return s        

    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        hand_value = 0
        ace = False
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace = True
        
        if (ace == True) and (hand_value + 10 <= 21):            
            hand_value += 10
        return hand_value
       
    def draw(self, canvas, pos):
        for c in self.cards:
            c.draw(canvas,pos)
            pos[0] +=100
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cardlist = []
        for suit in SUITS:
            for rank in RANKS:
                self.cardlist.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.cardlist)
        return self.cardlist

    def deal_card(self):
        return self.cardlist.pop()
    
    def __str__(self):
        c= " "
        for i in range(len(self.cardlist)):
            c +=  str(self.cardlist[i]) + " "
        return "Deck contains" + str(c)
        



#define event handlers for buttons
def deal():
    global outcome, in_play,player,dealer,game_deck,score
    if in_play == True:
        score -= 1
    game_deck = Deck()
    game_deck.shuffle()  
#    print game_deck
    player = Hand()   
    dealer = Hand()    
    player.add_card(game_deck.deal_card())
    player.add_card(game_deck.deal_card())
    dealer.add_card(game_deck.deal_card())
    dealer.add_card(game_deck.deal_card())
#    print "Player " + str(player)
#    print player.get_value()
#    print "Dealer " + str(dealer)
#    print dealer.get_value()
    outcome = "Hit or Stand?"
#    print outcome
    # your code goes here
    
    in_play = True

def hit():
    global in_play
    global outcome
    global score
    if in_play == True:        
        if player.get_value() <= 21 :             
            player.add_card(game_deck.deal_card())
#            print "Player " + str(player)
#            print player.get_value()
            outcome = "Hit or Stand?"
            if player.get_value() > 21:
                outcome = "Player is busted" 
                in_play = False
                score -= 1                
#        print outcome
#        print score  
def stand():
    global in_play
    global outcome
    global score
    if player.get_value() > 21:
        outcome = "Busted"
#        print outcome
    else:
        while dealer.get_value() < 17:
            dealer.add_card(game_deck.deal_card())
#            print "Dealer " + str(dealer)
#            print dealer.get_value()
        if dealer.get_value() >21:
                outcome =  "Dealer has busted"
                in_play = False
                score += 1
        elif player.get_value() < dealer.get_value():
                outcome =  "Dealer wins"
                in_play = False
                score -= 1
        elif  player.get_value() == dealer.get_value():
                outcome =  "Hands are equal. Dealer wins"
                in_play = False
                score -= 1
        else:
                outcome =  "Player wins"
                in_play = False
                score += 1
            
         
       
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    global outcome,in_play
    player.draw(canvas, [100, 400])
    dealer.draw(canvas, [100, 100])
    canvas.draw_text("Blackjack", (50, 50), 36, 'White')
    canvas.draw_text("Dealer", (90, 90), 24, 'black')
    canvas.draw_text("Player", (90, 390), 24, 'black')
    canvas.draw_text("Score:", (400, 50), 36, 'White')
    canvas.draw_text(str(score), (500, 50), 36, 'White')
    if in_play == True:
        canvas.draw_text(outcome, (300, 300), 24, 'black')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (100+CARD_CENTER[0], 100+CARD_CENTER[1]), CARD_SIZE)
    elif in_play == False:
        canvas.draw_text("New Deal?", (300, 300), 24, 'black')
        canvas.draw_text(outcome, (300, 90), 24, 'black')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
