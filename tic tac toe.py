def print_board():
    print(board[0] + "|" + board[1] + "|" + board[2])
    print("-+-+-")
    print(board[3] + "|" + board[4] + "|" + board[5])
    print("-+-+-")
    print(board[6] + "|" + board[7] + "|" + board[8])


def checker(turn,loc):

    if (len(board[loc-1].strip()) == 0):
        board[loc-1]=turn
        print("Move saved")
        print_board()
    else:
        print("The location is full, Enter another location")
        loc = int(input())
        checker(turn,loc)
    return


def win(turn):
    for x in lst:
        if(board[x[0]]==board[x[1]]==board[x[2]]==turn):
            return True
    return False


def main():
    count = 0
    winner = ""
    turn = "X"
    print("Welcome to tic tac toe game")
    print("The board with locations looks like this : ")
    print("1|2|3")
    print("-+-+-")
    print("4|5|6")
    print("-+-+-")
    print("7|8|9")

    print("Kindly please enter your names ")
    print("Player 1 : ")
    name1 = input()
    print("Player 2 : ")
    name2 = input()
    print("The game starts with " + name1)
    while ((count <= 9) | (len(winner) == 0)):
        if (count % 2 == 0):
            print("Enter the location from 1-9 where you would like to insert X")
            Name = name1
            turn = "X"
            loc = int(input())
            checker(turn, loc)
        else:
            print("Enter the location from 1-9 where you would like to insert O")
            Name = name2
            turn = "O"
            loc = int(input())
            checker(turn, loc)

        if (count >= 4):
            if (win(turn)):
                print("Congratulations! " + Name + " wins the game")
                return
        count += 1
    print("It's a Tie")
    return

lst = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]

board = {
    8 : " ", 7 : " ", 6 : " ", 5 : " ",4 : " ", 3 : " ", 2 : " ", 1 : " ", 0 : " "
}

__name__ = '__main__'

if __name__ == '__main__':
    main()


