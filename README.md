
# ChessBot

This project will provide a Python bot that can play chess using _pyautogui_ and _cv2_. 

Before you can use the code properly, you need to do a following things, these are the following (in order):  
1. Clone or download the project  
2. Download a chess-game. I used _The Chess Lv. 100_ from the Microsoft store.  
Link: https://www.microsoft.com/en-us/p/the-chess-lv100/9wzdncrfj23z?activetab=pivot:overviewtab  
3. Change the images in the file (the _images_ directory). You need to do this part to make the code work since the image-recognition simply compares pixels,
and thus if your computer has a different resolution as mine (which captured the images), the code will not work correctly.  
	i. _B_ and _W_ stand for a black and white tile correspondingly  
	ii. _TWB_ stands for _Tower_ with a _White_ colour and a _Black_ background (tile), this protocol is used throughout all the images with the following 
	abbreviations: {B=Bishop}, {H=Horse}, {K=King}, {P=Pion}, {Q=Queen}, {T=Tower}. You need to capture images of all these pieces with their corresponding
	colour and background to make the code run properly.  
	iii. Capture the next elements:  
		* _init board_ - this image is used to map the starting-pixels of the board on your PC  
		* _promotion_ - the promotion-title, this is needed to give a pion that crosses the board a promotion to queen, tower, ... .  
		* _promotion queen_ - the queen-option within the _promotion_ window, this is the option the code will always choose, since it has the most overall value  
		* _title_ - the title of the game, the code scans for the title to know if it is still playing

If all the options above are done successfully, you can run the project. Go to 'Main' and run. You get three seconds to switch (manually) to the chess-game.
From then on, the bot will take over and play. A self-made board will be written inside the run-terminal. You can check if all the pictures were captured
successfully by going over each pion on the self-made board (inside the terminal) and compare this with the real chess board. Each step the bot will scan the
board completely to make sure that every pion is at the right position in the eyes of the bot.



## Computer or Human

It is both possible to let your bot play against a computer or a human component. By default the bot will play against the PC, but if you yourself wants to
play against the bot, you need to toggle the _human_ boolean inside the 'Main' class (a TODO will mark this position). The bot will always be player 1, so
if you want to play against the bot, you will be the player at the upper side, who will play second, after the bot performed it's action.



## Algorithm

The algorithm that is used to program the bot is the __minimax-algorithm__ (https://en.wikipedia.org/wiki/Minimax), further expended with __alpha-beta pruning__
(https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) to increase performance. The default depth of the search-tree is a depth of three. It is possible 
to change the depth inside the _Main Functions_ file (a TODO will mark this location). I have chosen to use a depth-tree of 3 because of the following reasons:  
* Three is an uneven number, which makes the algorithm more offensive  
* My machine is not that high-end, and thus a search-tree with a depth of five would make the algorithm to slow  

If a search-tree of five does not make the algorithm too slow on your machine, I would definitely recommend you to choose a depth of five.