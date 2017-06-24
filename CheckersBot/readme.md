# Checkers Bot

### Basic Information

The Checkers bot is an interactive bot where Twitter users can play checkers against an AI enemy. The project was developed mainly to help me get used to working with Twitter's API, as well as playing around with artificial intellegence algorithms (minimax, alpha-beta pruning, etc.)

### Using It

Starting off, the black pieces are controlled by AI, and the white pieces are controlled by players. The players make the first turn.

To play, respond to the tweet that has the game board with the piece to be moved, and where the piece should move. The program will take all from when the board tweet was posted until 3 hours after (if there weren't any responses, it'll just take the first response that comes in). The move that was tweeted the most will be utilized. If it's illegal, then the 2nd most tweeted move will be used, and so on. After that, the AI will move a piece, and control goes back to the player.

### Things To Work On

The data structures for the minimax algorithm are a mess, and it's leading to unsustainable code. I need to completely rewrite the data structure for the minimax algorithm.

Also, I need to find a way to access replied to specific tweets. Twitter's API doesn't have that feature, so I'll have to write it in myself.
