# coinline.py

class State:
    def __init__(self, coins, pScore=0, aiScore=0, turn='player'): 
        self.coins = coins
        self.pScore = pScore
        self.aiScore = aiScore
        self.turn = turn


"""
Returns which player (either you or AI) who has the next turn.

In the initial game state, you (i.e. 'player') gets to pick first. 
Subsequently, the players alternate with each additional move.

If there no coins left, any return value is acceptable.
"""
def player(state):
    return state.turn


"""
Returns the set of all possible actions available on the line of coins.

The actions function should return a list of all the possible actions that can be taken given a state.

Each action should be represented as a tuple (i, j) where i corresponds to the side of the line ('L', 'R')
and j corresponds to the number of coins to be picked (1, 2).

Possible moves depend on the numner of coins left.

Any return value is acceptable if there are no coins left.
"""
def actions(state):
    possible_actions = []
    coins_left = len(state.coins)

    if coins_left == 0:
        return possible_actions

    # Choose from Left side
    if coins_left >= 1:
        possible_actions.append(('L', 1))
    if coins_left >= 2:
        possible_actions.append(('L', 2))

    # Choose from right side
    if coins_left >= 1:
        possible_actions.append(('R', 1))
    if coins_left >= 2:
        possible_actions.append(('R', 2))

    return possible_actions

"""
Returns the line of coins that results from taking action (i, j), without modifying the 
original coins' lineup.

If `action` is not a valid action for the board, you  should raise an exception.

The returned state should be the line of coins and scores that would result from taking the 
original input state, and letting the player whose turn it is pick the coin(s) indicated by the 
input action.

Importantly, the original state should be left unmodified. This means that simply updating the 
input state itself is not a correct implementation of this function. You’ll likely want to make a 
deep copy of the state first before making any changes.
"""
def succ(state, action):

    if action not in actions(state):
        raise ValueError(f"Invalid action: {action} for current state")


    new_coins = state.coins.copy()
    new_pScore = state.pScore
    new_aiScore = state.aiScore

    side, num_coins = action

    # Calculating score for the move
    score = 0
    if side == 'L':
        for i in range(num_coins):
            score += new_coins.pop(0)  # Remove from left
    else:  # side == 'R'
        for i in range(num_coins):
            score += new_coins.pop()  # Remove from right

    # Update the score based on whose turn it is
    if state.turn == 'player':
        new_pScore += score
        new_turn = 'ai'
    else:
        new_aiScore += score
        new_turn = 'player'

    return State(new_coins, new_pScore, new_aiScore, new_turn)


"""
Returns True if game is over, False otherwise.

If the game is over when there are no coins left.

Otherwise, the function should return False if the game is still in progress.
"""
def terminal(state):
    return len(state.coins) == 0

"""
Returns the scores of the two players.

You may assume utility will only be called on a state if terminal(state) is True.
"""
def utility(state):
    if not terminal(state):
        raise ValueError("Utility will only be called on terminal states")
    return (state.pScore, state.aiScore)


"""
Returns the winner of the game, if there is one.

- If the player has won the game, the function should return 'player'.
- If your AI program has won the game, the function should return AI.
- If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the
  function should return None.
"""
def winner(state):
    if not terminal(state):
        return None

    if state.pScore > state.aiScore:
        return 'player'
    elif state.aiScore > state.pScore:
        return 'ai'
    else:
        return None


"""
Returns the best achivable value and the optimal action for the current player.

The move returned should be the optimal action (i, j) that is one of the allowable 
actions given a line of coins.

If multiple moves are equally optimal, any of those moves is acceptable.

If the board is a terminal board, the minimax function should return None.
"""

#Using memoization here for efficiency and avoiding unnecessary calculation
memo = {}
def minimax(state, is_maximizing):
    state_key = (tuple(state.coins), state.turn)

    if state_key in memo:
        return memo[state_key]

    if terminal(state):
        return (state.aiScore - state.pScore), None

    possible_actions = actions(state)
    best_action = None

    if is_maximizing:
        best_value = -float('inf')
        for action in possible_actions:
            value, _ = minimax(succ(state, action), False)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = float('inf')
        for action in possible_actions:

            value, _ = minimax(succ(state, action), True)
            if value < best_value:
                best_value = value
                best_action = action

    memo[state_key] = (best_value, best_action)
    return best_value, best_action

    