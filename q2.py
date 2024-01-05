import copy
import heapq
import math
import random

archiveArray = []
possibleMoves = []
goals = 0
iteration_counter = 2000


def agent_update(array):
    agents = 0
    for y in range(len(array)):
        for x in range(len(array)):
            if array[y][x] == 2:
                agents += 1
    return agents


class Board:
    def __init__(self, array, parent=None):
        self.parent = parent
        self.array = array
        if parent:
            self.g = parent.g + 1
        else:
            self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


    def __eq__(self, other):
        for row in range(len(self.array)):
            for col in range(len(self.array)):
                if self.array[row][col] != other.array[row][col]:
                    return False
        return True


    def get_h(self):
        return self.h


    def getParent(self):
        return self.parent


    def getArray(self):
        return self.array


    def heuristics_calc(self):
        h = 0
        agentsCounter = 0
        agents = agent_update(self.array)
        global goals
        target = len(goals)
        diff = agents - len(goals)
        totalMinManhtan = []
        minStepToExitBord = []
        # calculate for each Agent the distance to each goal. save the minimual of all
        for y in range(len(self.array)):
            for x in range(len(self.array)):
                if self.array[y][x] == 2:
                    agentsCounter += 1
                    if diff > 0:
                        minStepToExitBord.append(len(self.array) - y)
                    mimMoveToGoal = 100  # some high number that could not be posible distance on the board
                    for goal in goals:
                        distance = abs(y - goal.y) + abs(x - goal.x)
                        if mimMoveToGoal > distance:
                            mimMoveToGoal = distance
                        if mimMoveToGoal == 0:
                            break
                    totalMinManhtan.append(mimMoveToGoal)
            if agentsCounter == agents:
                break
        heapq.heapify(totalMinManhtan)
        while target > 0:
            h += heapq.heappop(totalMinManhtan)
            target -= 1
        heapq.heapify(minStepToExitBord)
        while diff > 0:
            h += heapq.heappop(minStepToExitBord)
            diff -= 1
        return h


    def heuristicUpdate(self):
        self.h = self.heuristics_calc()
        self.f = self.g + self.h


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# check all possible move, if the move is valid and not already exist add the bord to possibleMoves
def explore(currentBoard):
    global iteration_counter
    global possibleMoves
    # gotToGoal = False
    for row in range(len(currentBoard.array)):
        # if gotToGoal is True:
        #     break
        for col in range(len(currentBoard.array)):
            if currentBoard.array[row][col] == 2:       # in current location there is an agent
                # move Up
                if row > 0 and currentBoard.array[row-1][col] == 0:
                    iteration_counter -= 1
                    newArray = copy.deepcopy(currentBoard.array)
                    newArray[row][col] = 0
                    newArray[row-1][col] = 2
                    if newArray not in archiveArray:
                        archiveArray.append(newArray)
                        newBoard = Board(newArray, currentBoard)
                        possibleMoves.append(newBoard)
                        newBoard.heuristicUpdate()
                        # if newBoard.get_h() == 0:
                        #     gotToGoal = True
                        #     break
                # move Down
                if row < len(currentBoard.array)-1 and currentBoard.array[row+1][col] == 0:
                    iteration_counter -= 1
                    newArray = copy.deepcopy(currentBoard.array)
                    newArray[row][col] = 0
                    newArray[row+1][col] = 2
                    if newArray not in archiveArray:
                        archiveArray.append(newArray)
                        newBoard = Board(newArray, currentBoard)
                        possibleMoves.append(newBoard)
                        newBoard.heuristicUpdate()
                        # if newBoard.get_h() == 0:
                        #     gotToGoal = True
                        #     break
                # move Left
                if col > 0 and currentBoard.array[row][col-1] == 0:
                    iteration_counter -= 1
                    newArray = copy.deepcopy(currentBoard.array)
                    newArray[row][col] = 0
                    newArray[row][col-1] = 2
                    if newArray not in archiveArray:
                        archiveArray.append(newArray)
                        newBoard = Board(newArray, currentBoard)
                        possibleMoves.append(newBoard)
                        newBoard.heuristicUpdate()
                        # if newBoard.get_h() == 0:
                        #     gotToGoal = True
                        #     break
                # move Right
                if col < len(currentBoard.array)-1 and currentBoard.array[row][col+1] == 0:
                    iteration_counter -= 1
                    newArray = copy.deepcopy(currentBoard.array)
                    newArray[row][col] = 0
                    newArray[row][col+1] = 2
                    if newArray not in archiveArray:
                        archiveArray.append(newArray)
                        newBoard = Board(newArray, currentBoard)
                        possibleMoves.append(newBoard)
                        newBoard.heuristicUpdate()
                        # if newBoard.get_h() == 0:
                        #     gotToGoal = True
                        #     break
                # move to get agent out of board
                agents = agent_update(currentBoard.getArray())
                if agents > len(goals) and row == len(currentBoard.array)-1:
                    iteration_counter -= 1
                    newArray = copy.deepcopy(currentBoard.array)
                    newArray[row][col] = 0
                    if newArray not in archiveArray:
                        archiveArray.append(newArray)
                        newBoard = Board(newArray, currentBoard)
                        possibleMoves.append(newBoard)
                        newBoard.heuristicUpdate()
                        # if newBoard.get_h() == 0:
                        #     gotToGoal = True
                        #     break


def print_bag():
    global bag
    bag.revers()
    for i in range(len(bag)):
        for j in range(len(i)):
            bag[i][j].array
            if i != 1:
                print("Board ", i, " (starting position):")
            elif i == len(bag):
                print("Board ", i, " (goal position):")
            else:
                if j == 0:
                    print("Board ", i,"a", " :")
                    print("   ", end=" ")
                elif j == 1:
                    print("Board ", i, "b", " :")
                    print("   ", end=" ")
                elif j == 2:
                    print("Board ", i, "c", " :")
                    print("   ", end=" ")
            for col in range(len(bag[i][j].array)):
                print(col + 1, end=" ")
            print()
            for row in range(len(bag[i][j].array)):
                print(row + 1, ":", end=" ")
                for col in range(len(bag[i][j].array)):
                    if bag[i][j].array[row][col] == 0:
                        print(" ", end=" ")
                    elif bag[i][j].array[row][col] == 1:
                        print('@', end=" ")
                    else:
                        print('*', end=" ")
                print()


# printing board
def printBoard(starting_board, detail_output):
    movesToPrint = []
    boardNumber = 1
    global bag
    global BoardTocheck
    while BoardTocheck.getParent():
        movesToPrint.append(BoardTocheck)
        BoardTocheck = BoardTocheck.parent
    movesToPrint.append(Board(starting_board))
    movesToPrint.reverse()
    # print moves from starting_board to goal_board
    while movesToPrint:
        boardPrint = movesToPrint.pop(0)
        ArrayToprint = boardPrint.getArray()
        if len(movesToPrint) == 0:
            print("Board ", boardNumber, " (goal position):")
        elif boardNumber == 1:
            print("Board ", boardNumber, " (starting position):")
        else:
            print("Board ", boardNumber, " :")
        print("   ", end=" ")
        for col in range(len(ArrayToprint)):
            print(col + 1, end=" ")
        print()
        for row in range(len(ArrayToprint)):
            print(row + 1, ":", end=" ")
            for col in range(len(ArrayToprint)):
                if ArrayToprint[row][col] == 0:
                    print(" ", end=" ")
                elif ArrayToprint[row][col] == 1:
                    print('@', end=" ")
                else:
                    print('*', end=" ")
            print()
        if detail_output and boardNumber != 1:
            print("Heuristic:", boardPrint.get_h())
        boardNumber += 1


def find_path(starting_board, goal_board, search_methos, detail_output):
    global goals
    global NoPathFound
    global possibleMoves
    global BoardTocheck

    goals = []
    NoPathFound = True
    for row in range(len(goal_board)):
        for col in range(len(goal_board)):
            if goal_board[row][col] == 2:
                goals.append(Goal(col, row))
    agents = agent_update(starting_board)
    if agents < len(goals):  # No way to get a solution when agents < goals
        if detail_output is False:
            print("No path found")
        quit()
    if search_methos == 1:
        a_star(starting_board)
    elif search_methos == 2:
        hill_climbing(starting_board, goal_board)
    elif search_methos == 3:
        simulated_annealing(starting_board, goal_board)
    elif search_methos == 4:
        local_beam(starting_board, goal_board, detail_output)
        # if detail_output is True:
        #     print_bag(bag)
    # elif search_methos == 5:
    #     genetic_algorithm(starting_board)
    if NoPathFound is False:
        # BoardTocheck is the goal board so process finished
        if BoardTocheck.get_h() == 0 and BoardTocheck.array == goal_board:
            printBoard(starting_board,detail_output)
    if detail_output is False and NoPathFound:
        print("No path found")


def a_star(starting_board):
    archiveArray.append(starting_board)
    currentBoard = Board(starting_board)
    explore(currentBoard)
    while len(possibleMoves) > 0 and iteration_counter > 0:
        heapq.heapify(possibleMoves)
        BoardTocheck = heapq.heappop(possibleMoves)
        # TODO check if agent update needed here
        agent_update(BoardTocheck.array)
        # BoardTocheck is the goal board so process finished
        if BoardTocheck.get_h() == 0 and BoardTocheck.array == starting_board:
            NoPathFound = False
            return
        explore(BoardTocheck)


def hill_climbing(starting_board, goal_board):
    reset_counter = 5
    flat_state = 3
    next_state = 0
    global NoPathFound
    global BoardTocheck
    if starting_board == goal_board:
        NoPathFound = False
        BoardTocheck = Board(starting_board)
        return
    else:
        current_state = Board(starting_board)
        current_state.heuristicUpdate()
        explore(current_state)
        initial_state = copy.deepcopy(possibleMoves)
        initial_state.sort(key=lambda board: board.h)
        while current_state.array != goal_board and reset_counter > 0 and iteration_counter > 0:
            if len(possibleMoves) < 1:
                break
            possibleMoves.sort(key=lambda board: board.h)
            next_state = possibleMoves.pop(0)
            if next_state.h > current_state.h:      # next_state will not improve the h function
                if len(initial_state) > 1:
                    initial_state.pop(0)
                    current_state = initial_state.pop(0)
                    reset_counter -= 1
                else:
                    reset_counter = 0
                    break
            elif next_state.h == current_state.h:   # flat state -> the h function stay the same
                current_state = next_state
                flat_state -= 1
            elif next_state.h < current_state.h:
                current_state = next_state
            archiveArray.clear()
            possibleMoves.clear()
            explore(current_state)
    if current_state.array == goal_board:
        NoPathFound = False
        BoardTocheck = current_state
        return


def cool_down(t):
    # TODO check how to fix temperature and probability
    t = 100 - t
    # t = math.exp(-t)
    return t


def simulated_annealing(starting_board, goal_board):
    global NoPathFound
    global BoardTocheck
    t = 1
    current_state = Board(starting_board)
    current_state.heuristicUpdate()
    explore(current_state)
    T = cool_down(t)
    while T > 0:
        random.shuffle(possibleMoves)
        next_state = possibleMoves.pop()
        possibleMoves.clear()
        archiveArray.clear()
        delta = current_state.h - next_state.h
        if delta > 0:
            current_state = next_state
            explore(current_state)
        else:
            # TODO delete the printing
            p = math.exp(delta/T)
            print("delate: " ,delta)
            print("T: ", T)
            print("p: " ,p)
            if p > random.random():
                current_state = next_state
            explore(current_state)
        t += 1
        T = cool_down(t)
        # TODO delete the printing
        print("t:", t)

    if T == 0:
        BoardTocheck = current_state
        if current_state.array == goal_board:
            NoPathFound = False
        return


def local_beam(starting_board, goal_board,detail_output):
    global NoPathFound
    global BoardTocheck
    global bag
    global possibleMoves
    bag = []            # list of neighbors that had considered in path
    k = 2               # the number of neighbors-1 each step
    next_state = []     # next list of neighbors that can lead to goal
    if starting_board == goal_board:
        BoardTocheck = Board(starting_board)
        NoPathFound = False
        return
    current_state = Board(starting_board)
    bag.append(current_state)
    current_state.heuristicUpdate()
    explore(current_state)
    possibleMoves.sort(key=lambda board: board.h)
    for i in range(k):                  # expend the K number of the best boards
        if len(possibleMoves) > 0:
            next_state.append(possibleMoves.pop(0))
    bag.append(next_state)
    while NoPathFound and len(next_state) > 0:
        possibleMoves.clear()           # TODO check if clear is needed here, if i keep memory of pased state it will be easier to solev
        archiveArray.clear()
        for state in next_state:
            if state.array == goal_board:
                BoardTocheck = state
                NoPathFound = False
                if detail_output is True:
                    print_bag()
                return
            else:
              explore(state)
        possibleMoves.sort(key=lambda board: board.h)
        next_state.sort(key=lambda board: board.h)
        for i in range(k):  # expend the K number of the best boards
            if len(possibleMoves) > 0 and possibleMoves[0].h < next_state[-1].h:
                if len(next_state) > 3:
                    next_state.pop(-1)
                next_state.append(possibleMoves.pop(0))
                next_state.sort(key=lambda board: board.h)
            if i == 2:
                bag.append(next_state)
            # else:
            #     next_state.clear()
    # if NoPathFound is False:
    #     # BoardTocheck is the goal board so process finished
    #     # if BoardTocheck.get_h() == 0 and BoardTocheck.array == goal_board:
    #     #     printBoard(starting_board, detail_output ,4)