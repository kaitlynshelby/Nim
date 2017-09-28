# Kaitlyn Sorum
# TCSS 142
# Charles Bryan
# 12/11/2015
# Programming Project 2 - Nim Game

# Extra Features: Players can choose a different character to use
# in place of the 'O' stone. Players can also choose if they want to
# enable hints.

import random

def main():
    play_again = 'y'
    while play_again.lower() == 'y':
        player1, player2 = get_players()
        stone = choose_stone()
        hint = get_hint_choice()
        stone_list, num_piles, game_over = generate_start_board(stone, hint)
        while stone_list != game_over:
            get_move(player1, num_piles, stone_list, game_over, hint)
            if stone_list != game_over:
                get_move(player2, num_piles, stone_list, game_over, hint)
        play_again = input \
            ("Do you want to play again? Enter y for yes, anything for no: ")
        
# pre : none
# post: player1 and player2 are the names of the players
def get_players():
    player1 = input('Player 1, enter your name: ')
    player2 = input('Player 2, enter your name: ')
    return player1, player2

# pre : none
# post: returns player's choice of stone
def choose_stone(): 
    print("{} = 1\t{} = 2\t{} = 3\t{} = 4\t{} = 5".format('O', chr(9829),\
                    chr(9786), chr(9774), chr(9924)))
    choice = input("Choose a stone to play with: ")
    # if choice is not valid, default stone ('O') will be used 
    if choice == '2':
        stone = chr(9829)
    elif choice == '3':
        stone = chr(9786)
    elif choice == '4':
        stone = chr(9774)
    elif choice == '5':
        stone = chr(9924)
    else:
        stone = 'O'
    return stone

# pre : none
# post: returns player input for whether or not to enable hints
def get_hint_choice():
    choice = input("Would you like to enable hints? Enter y for yes, anything for no: ")
    return choice

# pre : stone is the stone type chosen by the player
# pre : hint is a string indicating whether or not hints are enabled
# post: stone_list is a list of strings representing the stones in each pile
#       (ex: ["OO", "OOO", "O"])
# post: num_piles is the randomly generated number of piles
# post: game_over is a list of empty strings representing the state the board
#       should be in when the game is over
def generate_start_board(stone, hint):
    num_piles = random.randint(2, 5)
    stone_list = []
    game_over = []
    for num in range(num_piles):
        stone_list.append(stone * random.randint(1, 8))
        #   game_over should be a list of empty strings the same length as
        #   stone_list. stone_list should be a list of empty strings when
        #   the game is over, so game_over can be used for comparison
        game_over.append('')  
    generate_updated_board(num_piles, stone_list, game_over, hint)
    return stone_list, num_piles, game_over

# pre : name is the name of the player whose turn it is
# pre : num_piles is the number of piles
# pre : stone_list is the list representing the stones in each pile
# pre : hint is string indicating whether or not hints are enabled
# pre : game_over is a list the same size as stone_list of empty strings
# post: none
def get_move(name, num_piles, stone_list, game_over, hint):
    stones = input('{}, how many stones to remove? '.format(name))
    pile = input('Pick a pile to remove from: ')
    while not str(pile).isdigit() or int(pile)-1 not in range(num_piles):
        pile, stones = input_error(name)
    while not str(stones).isdigit() or int(stones)-1 not in range\
          (len(stone_list[int(pile)-1])):
        pile, stones = input_error(name)
    stones = int(stones)
    pile = int(pile)
    stone_list[pile-1] = stone_list[pile-1][:(-stones)]
    generate_updated_board(num_piles, stone_list, game_over, hint)
    if stone_list == game_over: 
        print('{} is the winner of this round!'.format(name))

# pre : name is the name of a player
# post: pile is the validated pile number to remove from
# post: stones is the validated number of stones to remove
def input_error(name):
    print('Hmm. You entered an invalid value. Try again {}.'.format(name))
    stones = input('{}, how many stones to remove? '.format(name))
    pile = input('Pick a pile to remove from: ')
    return pile, stones

# pre : num_piles is the number of piles
# pre : stone_list is the list representing the stones in each pile
# pre : game_over is a list the same size as stone_list of empty strings
# pre : hint is a string indicating whether or not hints are enabled
# post: none
def generate_updated_board(num_piles, stone_list, game_over, hint):
    print("Let's look at the board now.")
    print("-"*30)
    for num in range(num_piles):
        print('Pile {}: {}'.format(num+1, stone_list[num]))
    print("-"*30)
    # should not give hint if the game is over
    if stone_list != game_over and hint.lower() == 'y':
        give_hint(stone_list)

#pre : stone_list is the list representing the stones in each pile
#post: none
def give_hint(stone_list):
    board_nimsum = get_nimsum(stone_list) 
    # if board_nimsum is not zero, calculate how many stones to remove from
    # "bad pile"
    # if board_nimsum is zero, no need to call find_bad_pile, just remove all
    # stones from first pile containing stones
    if board_nimsum != 0:
        remove_idx = find_bad_pile(stone_list)
        stone_copy = stone_list[:]
        del stone_copy[remove_idx]
        nimsum = get_nimsum(stone_copy)
        remove_num = len(stone_list[remove_idx])-nimsum
        print("Hint: nimsum is {}.".format(board_nimsum))
        print("Pick {} stones from pile {}.".format(remove_num, remove_idx + 1))
    else:
        idx = 0
        for item in stone_list:
            # need to find first pile containing stones
            # break out of loop once pile is found
            if item != '':
                print("Hint: nimsum is 0.")
                print("Pick {} stones from pile {}.".format(len(item), idx + 1))
                break
            idx += 1
    

#pre : a_list is a list of stones in each pile involved in the calculation
#post: nimsum is the nimsum of all the lengths of the items in a_list
def get_nimsum(a_list):
    nimsum = 0
    for item in a_list:
        nimsum ^= len(item)
    return nimsum

# pre : stone_list is the list of stones in each pile
# post: returns index of the first occurence of 1 in xor_list
# post: returns list of binary values of stone_list lengths as strings
def get_xor(stone_list):
    xor_list = [0, 0, 0, 0]
    bin_list = []
    for item in stone_list:
        binary = "{:0>4}".format(bin(len(item))[2:])
        bin_list.append(binary)
        i = 0
        for digit in binary:
            xor_list[i] ^= int(digit)
            i += 1
    # if there is a 1 in xor_list, nimsum is not 0, and the index of the first 1 in xor_list
    # is the index to look for 1s at in binary representations of the lengths of
    # stone_list items
    if 1 in xor_list:
        return xor_list.index(1), bin_list
    # return -1 if there are no 1s in xor_list
    else:
        return -1, bin_list

# pre : stone_list is the list of stones in each pile
# post: returns index of pile to remove from
def find_bad_pile(stone_list):
    # x is the index to look for 1s at in each item in bin_list
    # bin_list is a list of binary numbers representing the length
    # of each item in stone_list
    x, bin_list = get_xor(stone_list)
    # if x is not -1, return i (i is the index number the "bad pile"
    # is located at (bin_list is parallel to stone_list))
    if x != -1:
        for i in range(len(bin_list)):
            if bin_list[i][x] == '1':
                return i
    # return -1 to indicate there are no piles contributing a 1 to nimsum
    else:
        return -1
        
            


main()
