'''
    This program is a version of the game solitaire
    It recieves game moves from the user, checks the validity of the moves and executes the moves if they valid
    There is error checking built in if the user mistypes or the moves is not valid, so the program does not crash
    It then displays the game board with the updated move and prompts the user for another move
    When user has placed all the cards in their appropriate foundation, the winner banner appears and the program stops
'''

import cards

YAY_BANNER = """
__   __             __        ___                       _ _ _ 
\ \ / /_ _ _   _    \ \      / (_)_ __  _ __   ___ _ __| | | |
 \ V / _` | | | |    \ \ /\ / /| | '_ \| '_ \ / _ \ '__| | | |
  | | (_| | |_| |_    \ V  V / | | | | | | | |  __/ |  |_|_|_|
  |_|\__,_|\__, ( )    \_/\_/  |_|_| |_|_| |_|\___|_|  (_|_|_)
           |___/|/                                            

"""

RULES = """
    *------------------------------------------------------*
    *-------------* Thumb and Pouch Solitaire *------------*
    *------------------------------------------------------*
    Foundation: Columns are numbered 1, 2, ..., 4; built 
                up by rank and by suit from Ace to King. 
                You can't move any card from foundation,   
                you can just put in.

    Tableau:    Columns are numbered 1, 2, 3, ..., 7; built 
                down by rank only, but cards can't be laid on 
                one another if they are from the same suit. 
                You can move one or more faced-up cards from 
                one tableau to another. An empty spot can be 
                filled with any card(s) from any tableau or 
                the top card from the waste.
     
     To win, all cards must be in the Foundation.
"""

MENU = """
Game commands:
    TF x y     Move card from Tableau column x to Foundation y.
    TT x y n   Move pile of length n >= 1 from Tableau column x 
                to Tableau column y.
    WF x       Move the top card from the waste to Foundation x                
    WT x       Move the top card from the waste to Tableau column x        
    SW         Draw one card from Stock to Waste
    R          Restart the game with a re-shuffle.
    H          Display this menu of choices
    Q          Quit the game
"""

def valid_fnd_move(src_card, dest_card):
    """
        Function that checks to make sure a card meets the requirements to be moved to a foundation
    """      
    if src_card.suit() == dest_card.suit():
        if dest_card.rank() == (src_card.rank() - 1):
            return True
        else:
            raise RuntimeError('Error: invalid command because the card rank')
    else:
        raise RuntimeError('Error: invalid command because the card suit')

        
def valid_tab_move(src_card, dest_card):
    """
        Function that checks to make sure a card meets the requirements to be moved to a tableau
    """          
    if src_card.suit() != dest_card.suit():
        if dest_card.rank() == (src_card.rank() + 1):
            return True
        else:
            raise RuntimeError('Error: invalid command because the card rank')
    else:
        raise RuntimeError('Error: invalid command because the card suit')
        
        
def tableau_to_foundation(tab, fnd):
    """
        function that moves a card from a tableau to a foundation and flips the top card of the tableau if necessary
    """  
    if len(tab) == 1:
        card = tab.pop()
        fnd.append(card)
    else:
        card = tab.pop()
        fnd.append(card)
        bottom_card = tab[-1]
        if not bottom_card.is_face_up():
            card1 = tab.pop()
            card1.flip_card()
            tab.append(card1)
            

def tableau_to_tableau(tab1, tab2, n):
    """
        function that moves a given number of cards from a tableau to another tableau and flips the top card of the tableau if necessary
    """ 
    if len(tab1) == n:
        cards = tab1[-n:]
        del tab1[-n:]
        for i in cards:
            tab2.append(i)
    else:
        cards = tab1[-n:]
        del tab1[-n:]
        for i in cards:
            tab2.append(i)
        bottom_card = tab1[-1]
        if not bottom_card.is_face_up():            
            card = tab1.pop()
            card.flip_card()
            tab1.append(card)
        
def waste_to_foundation(waste, fnd, stock):
    """
        function that moves a card from the waste to the foundation
    """   
    if len(waste) == 0:
        raise RuntimeError('Error: invalid command, waste is empty')
    card = waste.pop()
    fnd.append(card)
        
def waste_to_tableau(waste, tab, stock):
    """
        function that moves a card from the waste to the tableau
    """    
    if len(waste) == 0:
        raise RuntimeError('Error: invalid command, waste is empty')
    card = waste.pop()
    tab.append(card)

                            
def stock_to_waste(stock, waste):
    """
        Moves the card from the stock pile and places it on the top of the waste pile
    """   
    if len(stock) > 0:
        card = stock.deal()
        waste.append(card)
    else:
        raise RuntimeError('Error: invalid command, stock is empty')
                            
def is_winner(foundation):
    """
        if the 4 foundations have 13 cards each the winner banner is displayed
    """    
    if len(foundation[0]) == 13:
        if len(foundation[1]) == 13:
            if len(foundation[2]) == 13:
                if len(foundation[3]) == 13:
                    return True

def setup_game():
    """
        The game setup function, it has 4 foundation piles, 7 tableau piles, 
        1 stock and 1 waste pile. All of them are currently empty. This 
        function populates the tableau and the stock pile from a standard 
        card deck. 

        7 Tableau: There will be one card in the first pile, two cards in the 
        second, three in the third, and so on. The top card in each pile is 
        dealt face up, all others are face down. Total 28 cards.

        Stock: All the cards left on the deck (52 - 28 = 24 cards) will go 
        into the stock pile. 

        Waste: Initially, the top card from the stock will be moved into the 
        waste for play. Therefore, the waste will have 1 card and the stock 
        will be left with 23 cards at the initial set-up.

        This function will return a tuple: (foundation, tableau, stock, waste)
    """
    # you must use this deck for the entire game.
    # the stock works best as a 'deck' so initialize it as a 'deck'
    stock = cards.Deck()
    stock.shuffle()
    # the game piles are here, you must use these.
    foundation = [[], [], [], []]           # list of 4 lists
    tableau = [[], [], [], [], [], [], []]  # list of 7 lists
    waste = []                              # one list

    count = 0
    for d in range(7):
        tab = tableau[count:]
        count1 = 0
        for i in tab:
            if count1 == 0:
                i.append(stock.deal())
                count1 += 1
            else:
                card = stock.deal()
                card.flip_card()
                i.append(card)
        count += 1
    waste.append(stock.deal())


    return foundation, tableau, stock, waste

def display_game(foundation, tableau, stock, waste):
    """
        function that displays the game table
    """        
    print('='*20,'FOUNDATIONS','='*20)
    print('f1',' '*5,'f2',' '*5,'f3',' '*5,'f4')
    #prints the foundations, checks to make sure just the top card of the foundation is showing
    if len(foundation[0]) > 0:
            if len(foundation[1]) > 0:
                if len(foundation[2]) > 0:
                    if len(foundation[3]) > 0:
                        print(foundation[0][-1],' '*5,foundation[1][-1],' '*5,foundation[2][-1],' '*5,foundation[3][-1])
                    else:
                        print(foundation[0][-1],' '*5,foundation[1][-1],' '*5,foundation[2][-1],' '*5,foundation[3])
                else:
                    print(foundation[0][-1],' '*5,foundation[1][-1],' '*5,foundation[2],' '*5,foundation[3])
            else:
                print(foundation[0][-1],' '*5,foundation[1],' '*5,foundation[2],' '*5,foundation[3])
    else:
        print(foundation[0],' '*5,foundation[1],' '*5,foundation[2],' '*5,foundation[3])
    print('='*22,'TABLEAU','='*22)
    print('{:8}{:8}{:8}{:8}{:8}{:8}{:8}'.format('t1','t2','t3','t4','t5','t6','t7'))
    #checks the length of each tableau to find the longest one
    max_len = max(len(x) for x in tableau)
    #loops through each card in the tableau and formats the tableau in the correct manner
    for i in range(max_len):
        for j in range(7):
            if len(tableau[j])> i:
                print('{:8s}'.format(tableau[j][i].__repr__()), end='')
            else:
                print('{:8s}'.format(''), end='')
        print()    
    
    print('='*20,'STOCK/WASTE','='*20)
    print('Stock', '#', '(', len(stock), ')', '--->', waste)



print(RULES)
fnd, tab, stock, waste = setup_game()
display_game(fnd, tab, stock, waste)
print(MENU)
command = input("prompt :> ")
while command.lower() != 'q':
    try:
        if command.lower() == 'h':
            print(MENU)
        elif command.lower() == 'r':
            print(RULES)
            fnd, tab, stock, waste = setup_game()
            display_game(fnd, tab, stock, waste)
            print(MENU)
        elif command.lower() == 'sw':
            move = stock_to_waste(stock, waste)
        #executes the move when wt is entered
        #error checking is added to prevent the program from crashing if an invalid command is given
        elif command[:2].lower() == 'wt':
            i = command.split()
            if len(i) == 2:
                ta_tab = i[1]
                if ta_tab in '1234567':
                    i_tab = int(ta_tab)
                    waste_to_tab_count = (i_tab - 1)
                    #executes the move if the destination is empty
                    if len(tab[waste_to_tab_count]) == 0:                    
                        waste_to_tab = waste_to_tableau(waste, tab[waste_to_tab_count], stock)
                    elif len(tab[waste_to_tab_count]) == 0:
                                if waste[-1].rank() == 1:
                                    waste_to_tab = waste_to_tableau(waste, tab[waste_to_tab_count], stock)
                    #sends the user's move to check for the validity of the move
                    elif valid_tab_move(waste[-1], tab[waste_to_tab_count][-1]):
                        waste_to_tab = waste_to_tableau(waste, tab[waste_to_tab_count], stock)
                    else:
                        raise RuntimeError('Error: invalid command, incorrect tableau number')
                else:
                    raise RuntimeError('Error: invalid command, incorrect tableau row')
            else:
                raise RuntimeError('Error: invalid command, incorrect input')
        #executes the move when wf is entered
        #error checking is added to prevent the program from crashing if an invalid command is given
        elif command[:2].lower() == 'wf':
            i = command.split()
            if len(i) == 2:
                f_fnd = i[1]
                if f_fnd in '1234':
                    i_fnd = int(f_fnd)
                    waste_to_fnd_count = (i_fnd - 1)
                    #executes the move if the destination is empty
                    if len(fnd[waste_to_fnd_count]) == 0:
                        if waste[-1].rank() == 1:
                            waste_to_foundation(waste, fnd[waste_to_fnd_count], stock)
                        else:
                            raise RuntimeError('Error: invalid command, not an ace')
                    #sends the user's move to check for the validity of the move
                    elif valid_fnd_move(waste[-1], fnd[waste_to_fnd_count][-1]):
                        waste_to_foundation(waste, fnd[waste_to_fnd_count], stock)
                else:
                    raise RuntimeError('Error: invalid command, incorrect foundation number')
            else:
                raise RuntimeError('Error: invalid command, incorrect input')
        #executes the move when tt is entered
        #error checking is added to prevent the program from crashing if an invalid command is given
        elif command[:2].lower() == 'tf':
            i = command.split()
            if len(i) == 3:
                i_tab = i[1]
                i_fnd = i[2]
                if i_tab in '1234567':
                    if i_fnd in '1234':
                        tab_to_fnd_count = (int(i_tab) - 1)
                        fnd_from_tab_count = (int(i_fnd) - 1)
                        #executes the move if the destination is empty
                        if len(fnd[fnd_from_tab_count]) == 0:
                            if len(tab[tab_to_fnd_count]) > 0:
                                if tab[tab_to_fnd_count][-1].rank() == 1:
                                    tab_to_fnd = tableau_to_foundation(tab[tab_to_fnd_count], fnd[fnd_from_tab_count])
                                else:
                                    raise RuntimeError('Error: invalid command, not an ace')
                            else:
                                raise RuntimeError('Error: invalid command, incorrect tableau number')
                        #sends the user's move to check for the validity of the move        
                        elif valid_fnd_move(tab[tab_to_fnd_count][-1], fnd[fnd_from_tab_count][-1]):
                            tab_to_fnd = tableau_to_foundation(tab[tab_to_fnd_count], fnd[fnd_from_tab_count])
                    else:
                        raise RuntimeError('Error: invalid command, incorrect foundation number')
                else:
                    raise RuntimeError('Error: invalid command, incorrect tableau number')
            else:
                raise RuntimeError('Error: invalid command, incorrect input')        
        #executes the move when tt is entered
        #error checking is added to prevent the program from crashing if an invalid command is given
        elif command[:2].lower() == 'tt':
            i = command.split()
            if len(i) == 4:
                tab_tab1 = i[1]
                tab_tab2 = i[2]
                card_num = i[3]
                if tab_tab1 in '1234567' and tab_tab2 in '1234567' and card_num.isdigit():
                    tab_to_tab_count1 = (int(tab_tab1) - 1)
                    tab_to_tab_count2 = (int(tab_tab2) - 1)
                    num_of_cards = (int(card_num))
                    if num_of_cards <= len(tab[tab_to_tab_count1]):
                        if len(tab[tab_to_tab_count1]) > 0:
                            #executes the move if the destination is empty
                            if len(tab[tab_to_tab_count2]) == 0:
                                tab_to_tab = tableau_to_tableau(tab[tab_to_tab_count1], tab[tab_to_tab_count2], num_of_cards)
                            #sends the user's move to check for the validity of the move
                            elif valid_tab_move(tab[tab_to_tab_count1][-num_of_cards], tab[tab_to_tab_count2][-1]):
                                tab_to_tab = tableau_to_tableau(tab[tab_to_tab_count1], tab[tab_to_tab_count2], num_of_cards)
                        else:
                            raise RuntimeError('Error: invalid command, incorrect tableau number')       
                    else:
                        raise RuntimeError('Error: invalid command, incorrect number of cards')
                else:
                    raise RuntimeError('Error: invalid command, incorrect tableau row')
            else:
                raise RuntimeError('Error: invalid command, incorrect input')
                            
        else:
            raise RuntimeError('Error: not a valid command')

    except RuntimeError as error_message:  # any RuntimeError you raise lands here
        print("{:s}\nTry again.".format(str(error_message)))  
        print()
    #displays the winner banner if the user wins
    if is_winner(fnd):
        print(YAY_BANNER)
        break
    display_game(fnd, tab, stock, waste)                
    command = input("prompt :> ")

