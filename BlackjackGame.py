#CODECADEMY PORTFOLIO PROJECT
#PROJECT TITLE: Blackjack Game
#ASSUMPTIONS: 
#   Requires install of termcolor (in Terminal: "pip install termcolor")
#VERSION HISTORY: 
#   2023-09-10: Initial
#   2023-09-14: Minor fixes, including properly crediting player_bet (x2)
#   2023-09-17: Fixed issue with clearing of card_deck when shuffling (wasn't previously clearing correctly)
#PLANNED IMPROVEMENTS: 
#   1. Add color to terminal text for total rows to differentiate, improve readability
#   2. Support persistent players & balances (read/write to file)
#   3. Support multiplayer
#   4. Support "Split"
#   5. Print ASCII-art-style win/lose screen at completion
#   6. Handle floating-point math better with surrenders, maybe cast back to int if no decimal value

from time import sleep
from os import system
from termcolor import colored
import random

#This function contains high-level steps of game, consolidated into single function for readability
def main():
    #Clear terminal screen and print welcome message
    system('clear')
    print("""
        ======================  WELCOME  TO  ======================
        ______ _       ___  _____  _   __   ___  ___  _____  _   __ 
        | ___ \ |     / _ \/  __ \| | / /  |_  |/ _ \/  __ \| | / / 
        | |_/ / |    / /_\ \ /  \/| |/ /     | / /_\ \ /  \/| |/ /  
        | ___ \ |    |  _  | |    |    \     | |  _  | |    |    \  
        | |_/ / |____| | | | \__/\| |\  \/\__/ / | | | \__/\| |\  \ 
        \____/\_____/\_| |_/\____/\_| \_/\____/\_| |_/\____/\_| \_/ 
        
        ===========================================================
        
        """)
    print("For now, you'll be given $1000.00 to start with.")
    player_bank = 1000
    sleep (3) 

    #instantiate card deck for all rounds of play
    card_deck = CardDeck(1)

    #Begin play, continue as long as player says so or until bank reaches zero
    while player_bank>0:
        player_bank = play_round(player_bank, card_deck)
        system('clear')
        go_again = input("Would you like to play again? You have ${amt} in your bank. (Y/N) ".format(amt=player_bank))
        if go_again.upper() == "Y":continue
        else: break
    
    if player_bank < 0: final_player_bank = 0
    else: final_player_bank = player_bank
    print("\nYou ended the game with ${amt}. \n".format(amt=final_player_bank))

def play_round(player_bank, card_deck):
    system('clear')
    print("Let's play a round! \n")
    
    #Double check number of cards remaining in deck, and reshuffle if it's <17% (one-sixth) of original size
    if (len(card_deck.available_cards) / (card_deck.number_of_decks * 52)) < 0.17: 
        shufflemessage = "One moment - Shuffling the Deck"
        print(shufflemessage, end='\r')
        card_deck.shuffleDeck()
        i = 0
        while i < 3: 
            sleep(0.5)
            shufflemessage += " ."
            print(shufflemessage, end='\r')
            i += 1

    player_bet = 0
    #Ask how much player wants to bet, and scrub input for type and less-than available bank.
    while True:
        player_bet_dirty = input("\nHow much do you want to bet this round (out of ${bank})? $".format(bank=player_bank))
        try: player_bet = int(player_bet_dirty)
        except: 
            print("That wasn't an integer amount. Please try again.")
            sleep(2); continue
        if int(player_bet_dirty) > player_bank: 
            print("That amount was more than you have on hand. Please try again.")
            sleep(2); continue
        else: 
            player_bet = int(player_bet_dirty)
            break
    
    player_hand = PlayerHand() #Create object for player's hand
    dealer_hand = PlayerHand() #Create object for dealer's hand
    dealer_draw = True #Condition used to skip dealer portion of hand later if not needed
    player_hand.addCard(card_deck.drawCard())
    player_hand.addCard(card_deck.drawCard())
    dealer_hand.addCard(card_deck.drawCard())
    
    while True:
        system('clear')
        print(dealer_hand.printHand(True), "\n")
        print(player_hand.printHand(), "\n")
        print("""What do you want to do now? 
            1. Hit
            2. Stand
            3. Double Down
            4. Split
            5. Surrender""")
        match input("Enter the number of your choice: "):
            case "1": #Case for "Hit"
                player_hand.addCard(card_deck.drawCard())
                system('clear')
                print(player_hand.printHand())
                if player_hand.score > 21: 
                    print("Sorry, your hand went bust.")
                    dealer_draw = False
                    player_bank -= player_bet
                    break
                else: continue
            case "2": #Case for "Stand"
                break
            case "3": #Case for "Double Down"
                if player_bet * 2 > player_bank: 
                    print("Sorry, you don't have enough money to double-down on your bet.")
                    sleep(2)
                    continue
                else: 
                    player_bet += player_bet
                    print("Alright, double it is! Your bet is now ${amt} and you only get one more card.".format(amt=player_bet))
                    sleep(2)
                    system('clear')
                    player_hand.addCard(card_deck.drawCard())
                    print(player_hand.printHand())
                    if player_hand.score > 21: 
                        print("Sorry, your hand went bust.")
                        dealer_draw = False
                        player_bank -= player_bet
                    sleep(2)
                    break
            case "4": #Case for "Split"
                print("Sorry, I can't do that yet."); sleep(1)
                pass
            case "5": #Case for "Surrender"
                player_bank -= (player_bet / 2)
                print("Surrender it is. You've forfeit ${amt} in this round.".format(amt=(player_bet/2)))
                dealer_draw = False
                break
            case _: 
                print("Bad value entered, exiting program")
                exit()

    if dealer_draw:
        #Complete the dealer's draw on this round
        while dealer_hand.score < 17: 
            dealer_hand.addCard(card_deck.drawCard())
            system('clear')
            print(player_hand.printHand())
            print(dealer_hand.printHand(True))
            sleep(1)

        print("\n\nAND THE FINAL SCORE IS ... ")
        print("You have {a} points and the dealer has {b} points.".format(
            a = player_hand.score,
            b = dealer_hand.score))
        if dealer_hand.score > 21: 
            print("The dealer went bust - YOU WIN!")
            player_bank += player_bet * 2
        elif dealer_hand.score == player_hand.score: 
            print("You have the same score - this game was a PUSH.")
        elif dealer_hand.score > player_hand.score: 
            print("The dealer had more points - YOU LOST.")
            player_bank -= player_bet
        else: 
            print("You have more points! YOU WIN THIS ROUND!")
            player_bank += player_bet * 2

    sleep (3)

    player_hand.clearHand()   #get rid of all details of current hand
    return player_bank

class Card: 
    value = 0
    rank = ""
    rankint=0
    suit = ""
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        try: self.rankint = int(rank)
        except: pass
        if (self.rankint >= 2 and self.rankint <= 10): 
            self.value = self.rankint
        elif (rank in ["King", "Queen", "Jack"]): self.value = 10
        else: self.isAce = True; self.value = 1

class CardDeck: 
    available_cards = []
    card_options = []
    number_of_decks = 0
    
    def __init__(self,num_decks = 1): 
        self.number_of_decks = num_decks

        #Create list of available card options
        rank_options = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        suit_options = ["Spades", "Clubs", "Hearts", "Diamonds"]
        for rank in rank_options: 
            for suit in suit_options: 
                self.card_options.append(Card(rank,suit))

        self.shuffleDeck()

    def shuffleDeck(self):
        self.available_cards.clear() #Start by clearing any cards still in the deck
        
        #Create card deck based on number of standard card decks included in dealer's deck)        
        for i in range(0,int(self.number_of_decks)): 
            for option in self.card_options: self.available_cards.append(option)

    def drawCard(self): 
        #Return a random card from the cards still in the deck, and "pop" it out to the player's hand
        return self.available_cards.pop(random.randint(0,int(len(self.available_cards))-1))

class PlayerHand: 
    
    def __init__(self):
        self.score = 0
        self.cards = []
        self.hand_min_value = 0
        self.aces_high = 0

    def addCard(self,card):
        self.cards.append(card)
        if card.rank == "Ace":
            self.hasAce = True
            if self.score + 11 <= 21: 
                self.score += 11
                self.aces_high += 1
            else: 
                self.score += 1
        else: self.score += card.value

        if (self.score > 21) and (self.aces_high > 0): 
            self.score -= 10
            self.aces_high -= 1
    
#    def getScore(self):
#        finalscore = 0
#        number_of_aces = 0
#        for card in self.cards: 
#            if card.rank == "Ace": number_of_aces += 1
#            else: finalscore += card.value
#        return finalscore

    def clearHand(self):
        self.score = 0
        self.hand_min_value = 0
        self.cards.clear()

    def printHand(self,is_dealer=False):
        if is_dealer: message = "In the dealer's hand are: \n"
        else: message = "In your hand are: \n"
        for card in self.cards: 
            message += "   The {num} of {suit}".format(num=card.rank, suit=card.suit)
            message += "\n"
        message += "The score is currently {x}.".format(x=self.score)
        return message

class Player:
    pass

#This code used to execute the program by running main function
if __name__ == "__main__": 
    main()