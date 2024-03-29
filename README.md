# Gobblet AI Game
# Description
In this project, we will explore the game-playing of Gobblet, Gobblet is an abstract game
played on a 4x4 grid with each of the two players having twelve pieces that can nest on
top of one another to create three stacks of four pieces.
Your goal in Gobblet is to place four of your pieces in a horizontal, vertical, or diagonal
row. Your pieces start nested off the board. On a turn, you either play one exposed
piece from your three off-the-board piles or move one piece on the board to any other
spot on the board where it fits. A larger piece can cover any smaller piece. A piece
being played from off the board may not cover an opponent's piece unless it's in a row
where your opponent has three of his color.
Your memory is tested as you try to remember which color one of your larger pieces is
covering before you move it. As soon as a player has four like-colored pieces in a row,
he wins — except in one case: If you lift your piece and reveal an opponent's piece that
finishes a four-in-a-row, you don't immediately lose; you can't return the piece to its
starting location, but if you can place it over one of the opponent's three other pieces in
that row, the game continues..

  ## Assumptions
   1. The game assumes that the RED pieces always start first.
   2. In the Human VS AI mode, the AI plays with the black pieces, and the human player plays with the red pieces.
  ## Features 
  The Game has three modes to choose from:
  - **Human VS Human**:
    This mode provides a multiplayer experience where two human players can play against each other. 
  - **Human VS AI**:
    In this mode, a human player can play against an AI. The difficulty level and algorithm used by the AI can be selected.
  - **AI VS AI**: 
     This mode allows users to observe the gameplay between two AI opponents. The difficulty level for each AI player can be adjusted.
  ## Algorithms Used 
  The game utilizes the following algorithms for AI decision-making:
  - **Minimax algorithm**: This algorithm explores all possible moves and evaluates the board state to make optimal decisions.
Here's an overview of the key functions in the Minimax algorithm:
      ```python
      def  __makeMove(self, currentBoard: Board, move: Move) -> Board
      ```
      > This function creates a deep copy of the current board and makes the given move on the copy. This allows the Minimax algorithm to evaluate the resulting board states without altering the original board.

      ```python
      def __evaluate(self, board: Board, player: AI, agent_turn) -> int
      ```

      > This function evaluates the desirability of a given board state from the perspective of a specific player. It computes an integer score that reflects the desirability of the state. The score is determined using the provided heuristic algorithm, which is accessed         through heuristic_v2 from the Evaluation class. This heuristic algorithm takes the board state, the minimizing player, and the maximizing player as input parameters.
       
     ```python
     def __minimax(self, currentBoard: Board, currentPlayer: AI, maxDepth: int, currentDepth: int) -> Tuple[int, Move]
     ```
     > This function is the core of the Minimax algorithm. It explores the game tree up to a certain depth and returns the best move for the current player along with its score. The score is calculated by the `__evaluate` function.

    In the Minimax algorithm, two players are typically referred to as the maximizing player and the minimizing player. The maximizing player tries to get the highest score possible, while the minimizing player tries to do the opposite and get the lowest score possible.

  - **Alpha-beta pruning**: is an optimization technique for the Minimax algorithm. It reduces the number of nodes that are evaluated by the Minimax algorithm in its search tree.
Here's an overview of the key functions in the Alpha-beta pruning:
     ```python
     def  __makeMove(self, currentBoard: Board, move: Move) -> Board
      ```
     > This function makes a move on the board. It takes the current board state and a move as input, and returns a new board state.

     ```python
     def __evaluate(self, board: Board, player: AI, agent_turn) -> int
      ```
      > This function evaluates the desirability of a given board state from the perspective of a specific player. It computes an integer score that reflects the desirability of the state. The score is determined using the provided heuristic algorithm, which is         accessed through heuristic_v2 from the Evaluation class. This heuristic algorithm takes the board state, the minimizing player, and the maximizing player as input parameters.

    ```python
    def get_action(self, currentBoard: Board, currentPlayer: AI, maxDepth: int) -> Tuple[int, Move]
       ```
       > This function determines the best action for the current player by utilizing the Alpha-beta pruning algorithm. It conducts a search in the game tree up to a specified maximum depth, employing Alpha-beta pruning to efficiently explore and evaluate different moves and their resulting states.

    ```python
    def alpha_beta_recursion(self, curr_depth, agent_turn, currentPlayer, currentBoard, alpha, beta, get_time_diff, max_time)
    ```
      > This is the main function that implements the Alpha-Beta Pruning algorithm. It recursively explores the game tree, pruning branches that are determined to have no influence on the final decision. The function maintains the alpha and beta values to optimize the search process.
       
 - **Alpha-beta pruning iterative deeping**: This algorithm further improves the alpha-beta pruning by performing iterative deepening, which allows for more efficient searching of the game tree.
Here's an overview of the key functions in the Alpha-beta pruning:

   ```python
   def __makeMove(self, currentBoard: Board, move: Move) -> Board
   ```
      > This function makes a move on the board. It takes the current board state and a move as input, and returns a new board state.

   ```python
   def __evaluate(self, board: Board, player: AI, agent_turn) -> int
   ```
   >  This function evaluates the desirability of a given board state from the perspective of a specific player. It computes an integer score that reflects the desirability of the state. The score is determined using the provided heuristic algorithm, which is accessed through heuristic_v2 from the Evaluation class. This heuristic algorithm takes the board state, the minimizing player, and the maximizing player as input parameters.
      
   ```python
   def __gen_time_diff(self)
   ```
   > This function generates a time difference function that can be used to measure the elapsed time.
      
   ```python
   def get_action_iterative(self, currentBoard: Board, currentPlayer: AI, maxDepth: int, maxTime: float)
   ```
   > This function determines the best action for the current player by employing the Iterative Deepening Alpha-Beta Pruning algorithm. It iteratively searches the game tree, gradually increasing the search depth from 1 to the specified maximum depth. The search is performed within the given maximum time constraint.
      
   ```python
   def alpha_beta_recursion(self, curr_depth, agent_turn, currentPlayer, currentBoard, alpha, beta, get_time_diff, max_time)
   ```
   > This is the main function that implements the Alpha-Beta Pruning algorithm. It recursively explores the game tree, pruning branches that are determined to have no influence on the final decision. The function maintains the alpha and beta values to optimize the search process.
    
  ## Difficulty levels
  The game supports two difficulty levels:
   - **Easy**: This level has a depth of 2 in the search tree, making it less challenging for players.
     
   - **Hard**: This level has a depth of 5 in the search tree, providing a greater challenge for players. At this level, the AI is expected to make more optimal moves and can be difficult to beat.
## Heuristics
### Description:
The function selects rows by which four can be placed in a row. These are all vertical, horizontal and both diagonals. For each type, its figures are checked separately, then they are evaluated accordingly and added to the total score of the board. The score of a row consists of its piece weight, which is represented by the size of the piece and the number of pieces of one player in that row. The sign of the score of one type determines whether it is a MAX player or for the MIN player. The MAX has a positive sign, MIN has negative. Thus, after the final calculated score, based on the sign, we can see which player, according to our estimation, should win this board.
### Evaluation Flow:

1. If there are 4 pieces for the MAX player in any direction, the game ends, and the score is the maximum positive value.

2. If there are 4 pieces for the MIN player in any direction, the game ends, and the score is the minimum negative value.

3. **Case I: Direction contains only pieces of the same color.**
    - Each empty field will have a score equal to 1.
    - If the cell is not empty, the score will be equal to Size of the piece * 10.
    - Size of pieces is one of these integers (1,2,3,4).
    - Finally, cumulate each cell by multiplication, and the sign of the final score is according to the color of MIN or MAX player.

4. **Case II: Direction has different pieces in color.**
    - If the direction has the same number of pieces, the score is 0; no advantages for one player over the other.
    - If the direction does not have the same number of pieces:
        - Check if the player with more pieces also has bigger pieces in the external stack than the other player's pieces in the same direction.
        - If yes, calculate the score as in Case I, considering the pieces of the other player as empty cells.
        - Otherwise, the score of the direction is 0.

### Example
<img src="https://github.com/Ahmed-Khaled24/Gobblet-Game/assets/88388782/4a5f28c7-382f-4a35-b574-b5f53f787b60" alt="image" width="600" height="600"/></br>
Black is maximizer and white is the minimizer. 
| Direction        | Black        | White       |
|------------------|--------------|-------------|
| Vertical 1       | 0            | 0           |
| Vertical 2       | 0            | 0           |
| Vertical 3       | 1 * 40 * 40 * 1 | 0           |
| Vertical 4       | 30 * 1 * 1 * 1 | 0           |
| Horizontal 1     | 40 * 30 * 1 * 1 | 0           |
| Horizontal 2     | 1 * 40 * 1 * 1 | 0           |
| Horizontal 3     | 0            | 0           |
| Horizontal 4     | 0            | -40 * 1 * 1 * 1 |
| Left Diagonal    | 40 * 40 * 1 * 1 | 0           |
| Right Diagonal   | 0            | 0           |

Total score = 40 * 40 + 30 + 40* 30 + 40 - 40 + 40*40 = 98100 

## Contributor

| Team Member  | ID | 
| :---         |     :---:  | 
| Youmna Mahmoud  | 1901008 | 
| Ahmed Elsayed  | 1900730  |
| Ahmed Khaled  | 1901275 |
| Omar Fahmy  | 1901299 |

# Technologies Used
- **Python**
- **Pygame**    


