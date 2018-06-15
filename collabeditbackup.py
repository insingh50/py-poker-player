from random import randint
import math
from itertools import combinations
from builtins import int

"""
Hand rankings:      Royal Flush
                    Straight Flush
                    Four of a Kind
                    Full House
                    Flush
                    Straight
                    Three of a Kind
                    Two Pairs
                    Pair
                    High Card
"""


inf = float("inf")
negInf = float("-inf")
chips = 0
bet = 0
table = []
FINGERS = []
ACTIONS = ["fold", "call","check", "raise"]
VALS = ["2", "3", "4", "5", "6", "7", "8", "9", "1", "J", "Q", "K", "A"]
SUITS = ["C", "D", "H", "S"]
otherPossibleHands = []

testHand = [8,9,10,11,12]

probabilities = {
'royal flush' : 0.00000154,
'straight flush' : 0.0000139,
'four of a kind' : 0.000240,
'full house' : 0.001441,
'flush' : 0.001965,
'straight' : 0.003925,
'three of a kind' : 0.021128,
'two pair' : 0.047539,
'one pair' : 0.422569,
'high card' : 0.501177
}

deck = []
for i in range(51):
    deck.append(i)
    
#print(deck)
# class ActionLawsuit is a single history event
class ActionLawsuit:
    def __init__(self, action, bet):
        self.action = action
        self.bet = bet

# class Player is the representation of players
class Player:
    def __init__(self, name, chips, history):
        self.name = name
        self.chips = chips
        self.history = history


# sets number of chips to the given value
def changeChips(c):
    global chips
    chips = c
# sets the current wager to the given value
def changeBet(c):
    global bet
    bet = c

# def action():
#     (action, bet), maxbet)

# takes a number 0-51 and returns the coinciding card
def card(c):
    s = ""
    v = "" 
    if (c < 13):
        s = SUITS[0]
    elif (c < 26):
        s = SUITS[1]
    elif (c < 39):
        s = SUITS[2]
    else:
        s = SUITS[3]
    h = (c % 13)
    v = VALS[h]
    card = v + s
    return card

# deletes the cards from the deck
def deleteCards(cards):
    global deck
    for c in cards:
        f = card(c)
        deck.remove(f)

#remove
deleteCards(table)
deleteCards(FINGERS)

otherPossibleHands = list(combinations(deck, 5))



# takes a two character string card and returns the pretty version
def prettyCard(c):
    suit = ""
    val = ""
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    if c[0] == "1":
        val = "10"
    elif c[0] == "J":
        val = "Jack"
    elif c[0] == "Q":
        val = "Queen"
    elif c[0] == "K":
        val = "King"
    elif c[0] == "A":
        val = "Ace"
    else:
        val = c[0]
    
    if c[1] == SUITS[0]:
        suit = "Clubs"
    elif c[1] == SUITS[1]:
        suit = "Diamonds"
    elif c[1] == SUITS[2]:
        suit = "Hearts"
    elif c[1] == SUITS[3]:
        suit = "Spades"
    return val + " of " + suit


# takes a number 0-51, prints and returns the pretty card
def pc(c):
    tmp = card(c)
    res = prettyCard(tmp)
#     print(res)
    return res


# Used to check the card and prettyCard methods
def checkCards():
    for i in range(52):
        #print("card number: " + str(i))
        res = card(i)
#         print(res)
#         print(prettyCard(res))
#checkCards()

    
#generates a random hand for testing  
def ranHand():
    hand = []
    while(len(hand) < 5):
        r = randint(0,51)
        if r not in hand:
            hand.append(r)
    return hand


"""
Note:
when checking rank of hand, check in descending order of hand rank
to avoid errors.
Example:    list [8,9,10,11,12]
            
            is considered both a flush and a straight flush,
            even though it is a royal flush
"""

# returns True and the suit if the hand is a flush
def flush(cards):
    suit = cards[0][1]
    count = 1
    for i in range(1,len(cards)):
        if cards[i][1] == suit:
            count += 1
    if count == 5:
        return True, suit
    return False, "X"


# returns True and the lowest value if the hand is a straight
def straight(cards):
    firstCard = cards[0][0]
    ind = VALS.index(firstCard) + 1
    for i in range(1,len(cards)):
        if cards[i][0] != VALS[ind]:
            return False, "X"
        ind += 1
    return True, firstCard
 
 
# returns True and the suit if the hand is a royal flush
def royalFlush(cards):
    bool, suit = flush(cards)
    if bool and cards[0][0] == "1":
        return True, suit
    return False, "X"


# returns True and the suit if the hand is a straight flush
def straightFlush(cards):
    bool, suit = flush(cards)
    bool2, val = straight(cards)
    if bool and bool2:
        return True, suit
    return False, "X"


# used to find number of repeated value cards
def multi(cards):
    unique = []
    uniqCount = []
    for i in range(len(cards)):
        if cards[i][0] not in unique:
            uniqCount.append(1)
            unique.append(cards[i][0])
        else:
            uniqCount[unique.index(cards[i][0])] += 1
    return countMult(unique, uniqCount)
    #print(unique)
    #print(uniqCount)

# used to find number of repeated value cards (using multi)
def countMult(unique, uniqCount):
    if 4 in uniqCount:
#         print("4 of a kind")
        return True, "4"
    elif (3 in uniqCount) and (2 in uniqCount):
#         print("full house")
        return True, "f"
    elif 3 in uniqCount:
#         print("3 of a kind")
        return True, "3"
    elif uniqCount.count(2) == 2:
#         print("two pair")
        return True, "2p"
    elif 2 in uniqCount:
#         print("pair")
        return True, "p"
    else:
        return False, "X"

# returns the two character card of the highest card in the hand
def highCard(cards):
    positions = []
    for i in range(len(cards)):
        positions.append(VALS.index(cards[i][0]))
    mx = max(positions)
    mxPos = positions.index(mx)
    return cards[mxPos]
    
#helper function for bestHand()
def combinationsCards(fingers, table):
    totalCards = []
    totalCards.extend(fingers)
    totalCards.extend(table)
    if len(fingers) + len(table) <=5:
        return totalCards
    else:
        print(len(totalCards))
        return list(combinations(totalCards, 5))
        
# returns best hand out of all possible hands
def bestHand(fingers, table):
    possibleHands = combinationsCards(fingers, table)
    ranks = []
    for hand in possibleHands:
        #if communityChest(fingers, hand):
        #    possibleHands.remove(hand)
        #else:
        #    ranks.append(ranker(list(hand))[0])
        ranks.append(ranker(list(hand))[0])
    res = list(possibleHands[ranks.index(max(ranks))])
    res.sort()
    return res, ranker(list(res))[1]

def communityChest(fingers, hand):
    if fingers[0] in hand: return False
    elif fingers[1] in hand: return False
    else: return True

# used to determine the ranking of the hand (not finished)
def ranker(hand):
    hand.sort()
    cards = []
    for i in range(len(hand)):
        cards.append(card(hand[i]))
    bool, str = multi(cards)
    b,s = royalFlush(cards)
    b2,s2 = straightFlush(cards)
    b3,s3 = flush(cards)
    b4,s4 = straight(cards)
    if b:
        return 10, "royal flush!"
    elif b2:
        return 9, "straight flush!"
    elif bool:
        if str == "4":
            return 8, "four of a kind!"
        elif str == "f":
            return 7, "full house!"
        elif str == "3":
            return 4, "three of a kind!"
        elif str == "2p":
            return 3, "two pair!"
        elif str == "p":
            return 2, "pair"
    elif b3:
        return 6, "flush!"
    elif b4:
        return 5, "straight!"
    else:
        return 1, "high card?"

# test
rankOfBestHand = ranker(testHand)[0]
for hand in otherPossibleHands:
    if ranker(list(hand))[0] < 10:
        otherPossibleHands.remove(hand)

print(otherPossibleHands)

#print(ranker([0,14,15,16,17]))
"""
# check hand printing methods
h = ranHand()
h.sort()
for i in range(len(h)):
    pc(h[i])
ranker(h)
# check flush
hand = [0,1,2,3,4]
cards = []
for i in range(len(hand)):
    cards.append(card(hand[i]))
b,s = flush(cards)
print(b)
print(s)
# check straight
hand = [13,14,15,16,17]
cards = []
for i in range(len(hand)):
    cards.append(card(hand[i]))
b,s = straight(cards)
print(b)
print(s)
# check royal flush
hand = [8,9,10,11,12]
cards = []
for i in range(len(hand)):
    cards.append(card(hand[i]))
b,s = royalFlush(cards)
print(b)
print(s)
# check straight flush
hand = [14,15,16,17,18]
cards = []
for i in range(len(hand)):
    cards.append(card(hand[i]))
b,s = straightFlush(cards)
print(b)
print(s)
# check multi
hand = [0,13,27,40,51]
cards = []
for i in range(len(hand)):
    cards.append(card(hand[i]))
multi(cards)
# b,s = multi(cards)
# print(b)
# print(s)
# check High Card
hand = [0,13,27,40,51]
cards = []
for i in range(len(hand)):
    cards.append(card(hand[i]))
# highCard(cards)
b = highCard(cards)
print(b)
"""
