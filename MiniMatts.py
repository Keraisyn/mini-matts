"""
|  \/  | (_)         (_)   |  \/  |         | |   | |
| \  / |  _   _ __    _    | \  / |   __ _  | |_  | |_   ___
| |\/| | | | | '_ \  | |   | |\/| |  / _` | | __| | __| / __|
| |  | | | | | | | | | |   | |  | | | (_| | | |_  | |_  \__ \
|_|  |_| |_| |_| |_| |_|   |_|  |_|  \__,_|  \__|  \__| |___/
"""

#############################################################
# Course: ICS 3UI
# Teacher: Mr. Schattman
# Assignment: Artificial Intelligence Team Coding Assignment
# Authors: Matthews Ma, Harry Kim, Michelle Ma
#############################################################


def getMove(myScore, mySnowballs, myDucksUsed, myMovesSoFar,
            oppScore, oppSnowballs, oppDucksUsed, oppMovesSoFar):
    """Returns the best move given a game state."""

    state = [myScore, mySnowballs, myDucksUsed, myMovesSoFar,
            oppScore, oppSnowballs, oppDucksUsed, oppMovesSoFar]

    # Checks for patterns
    patternMove = detectPattern(state)
    if patternMove:
        return patternMove

    move = miniMax(state, "miniMax", 1, 7, "")

    return move["move"]


def detectPattern(state):
    """Detects Throw, Reload patterns and counters them."""
    oppMovesSoFar = state[7]
    myDucksUsed = state[2]
    mySnowballs = state[1]

    if len(oppMovesSoFar) >= 4:
        if oppMovesSoFar[-4:] == ["THROW", "RELOAD", "THROW", "RELOAD"]:
            if myDucksUsed < 5:
                return "DUCK"
            elif mySnowballs >= 1:
                return "THROW"
            else:
                return "RELOAD"
        elif oppMovesSoFar[-4:] == ["RELOAD", "THROW", "RELOAD", "THROW"]:
            if mySnowballs > 0:
                return "THROW"
            else:
                return "RELOAD"
    else:
        return None


# Implemented with reference to:
# https://medium.freecodecamp.org/how-to-make-your-tic-tac-toe-game-unbeatable-by-using-the-minimax-algorithm-9d690bad4b37
def miniMax(state, player, depth, maxDepth, miniMaxMove):
    """Finds the best move using the minimax algorithm."""

    availableMoves = getAvailableMoves(state, player)

    stateValue = evalState(state)

    if depth == maxDepth:
        return {"score": stateValue}

    if stateValue in [1000, -1000]:
        # A terminal state has been reached
        return {"score": stateValue}

    moves = []  # A list of all possible moves and their scores

    # Play each available move
    for i in availableMoves:
        move = {}
        move["move"] = i

        if player == "miniMax":
            newState = getNewState(state, player, i, "")
        else:
            newState = getNewState(state, player, miniMaxMove, i)

        # Find the score of the move
        if player == "miniMax":
            # Do not advance depth so the opponent can make a move
            result = miniMax(newState, "opponent", depth, maxDepth, i)
            move["score"] = result["score"]
        else:
            result = miniMax(newState, "miniMax", depth + 1, maxDepth, miniMaxMove)
            move["score"] = result["score"]

        # Append the move to the moves array
        moves.append(move)

    # Pick the move with the minimum or maximum score
    if player == "miniMax":
        # If it is miniMax's turn, choose the move with the highest score
        bestScore = -10000

        for i in moves:
            if i["score"] > bestScore:
                bestScore = i["score"]
                bestMove = i
    else:
        # If it is the opponent's turn, choose the move with the lowest score
        bestScore = 10000

        for i in moves:
            if i["score"] < bestScore:
                bestScore = i["score"]
                bestMove = i

    return bestMove


def getAvailableMoves(state, player):
    """Finds possible moves according to the rules."""

    moves = ["THROW", "DUCK", "RELOAD"]

    if player == "miniMax":
        if state[1] == 0:
            # No snowballs left
            moves.remove("THROW")

        if state[2] == 5:
            # No ducks left
            moves.remove("DUCK")

        if state[1] == 10:
            # Max snowballs reached
            moves.remove("RELOAD")
    else:
        if state[5] == 0:
            # No snowballs left
            moves.remove("THROW")

        if state[6] == 5:
            # No ducks left
            moves.remove("DUCK")

        if state[5] == 10:
            # Max snowballs reached
            moves.remove("RELOAD")

    return moves


def getNewState(state, player, miniMaxMove, opponentMove):
    """Calculates the new state according the move."""

    newState = state.copy()
    
    if player == "miniMax":
        if miniMaxMove == "THROW":
            # Remove 1 from my snowballs
            newState[1] -= 1
        elif miniMaxMove == "DUCK":
            # Add 1 from my ducks used
            newState[2] += 1
        elif miniMaxMove == "RELOAD":
            # Add 1 to my snowballs
            newState[1] += 1
    else:
        # The opponent's move is calculated second, so minimax's move must be factored in
        if opponentMove == "THROW":
            # Remove 1 from opponent snowballs
            newState[5] -= 1

            if miniMaxMove == "RELOAD":
                # MiniMax does not defend itself
                newState[4] += 1
        elif opponentMove == "DUCK":
            # Add 1 to opponent ducks
            newState[6] += 1
        elif opponentMove == "RELOAD":
            # Add 1 to opponent snowballs
            newState[5] += 1

            if miniMaxMove == "THROW":
                # Opponent does not defend itself
                newState[0] += 1
            
    return newState


def evalState(state):
    """Evaluates a game state."""

    if state[4] == 3: #We lose. Extremely Undesirable
        return -1000

    elif state[0] == 3: #Victory! Desirable.
        return 1000
    
    elif len(state[3]) >= 30: #Broke the Round Limit.
        if state[0] > state[4]:
            # Return slightly less than 1000 so miniMax() doesn't exit immediately when on round 30
            return 999
        elif state[0] < state[4]:
            return -999
        else:
            return 0
    else:
        pointValue = 20
        snowballValue = 5
        duckValue = 7

        myDucksLeft = 5 - state[2]
        oppDucksLeft = 5 - state[6]

        pointsDifference = state[0] - state[4]
        ballsDifference = state[1] - state[5]
        ducksDifference = myDucksLeft - oppDucksLeft
        movesSoFar = len(state[3])

        if movesSoFar <= 10: #Normal Mode
            pointAdvantage = pointsDifference * pointValue
            snowballAdvantage = ballsDifference * snowballValue
            duckAdvantage = ducksDifference * duckValue

        elif movesSoFar > 10 and movesSoFar <= 20: #Slightly More Offensive/Defensive...

            if state[0] > state[4]: #We're winning!
                pointAdvantage = pointsDifference * pointValue
                snowballAdvantage = ballsDifference * snowballValue * 1.1
                duckAdvantage = ducksDifference * duckValue

            else: #We're losing!
                pointAdvantage = pointsDifference * pointValue
                snowballAdvantage = ballsDifference * snowballValue * 0.9
                duckAdvantage = ducksDifference * duckValue


        elif movesSoFar > 20 and movesSoFar <= 25: #Getting more Offensive/Defensive...

            if state[0] > state[4]: #We're winning!
                pointAdvantage = pointsDifference * pointValue 
                snowballAdvantage = ballsDifference * snowballValue * 1.25
                duckAdvantage = ducksDifference * duckValue


            else: #We're losing
                pointAdvantage = pointsDifference * pointValue
                snowballAdvantage = ballsDifference * snowballValue * 0.75 
                duckAdvantage = ducksDifference * duckValue

        else: #Getting extremely Defensive/Offensive... 25 moves gone, 5 moves to go!
            if state[0] > state[4]: #We're winning!
                if state[2] > 2:
                    pointAdvantage = pointsDifference * pointValue
                    snowballAdvantage = ballsDifference * snowballValue * 1.5
                    duckAdvantage = ducksDifference * duckValue

                else:
                    pointAdvantage = pointsDifference * pointValue
                    snowballAdvantage = ballsDifference * snowballValue 
                    duckAdvantage = ducksDifference * duckValue

            else: #We're losing!
                 #go ham on the throws!
                    pointAdvantage = pointsDifference * pointValue
                    snowballAdvantage = ballsDifference * snowballValue * 2
                    duckAdvantage = ducksDifference * duckValue

        return pointAdvantage + snowballAdvantage + duckAdvantage 
