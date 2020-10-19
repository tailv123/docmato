Practical Python: Tomato Quiz
============================

UX
----
This application was developed with an educational end use in mind. 

__User Stories__

User stories were developed to guide game play and desired functions.

* As a site visitor I expect to have a access to instruction before deciding to sign in and play. 
* As a site visitor I expect to be able to view the leaderboard without having to sign in.
* As a player I should be able to enter my username before starting the game.
* As a player I expect that only valid username entries will be accepted.
* As a player I expect that I will be informed of if the username entered has already been used and if so what is the users playing status.
* As a player I should be informed if my answer was right or wrong before moving on to the next image. 
* As a player I should expect to have two attempts at answering each question, scoring higher marks for submitting a correct answer on the first attempt.
* As a player I should see my progress at each question in the quiz, with the question number, attempt and current score clearly shown.

Features
-----------------

__Existing Features__
* The home page greats the user with a brief intro, provides a text box to sign in, as well as links to the leaderboard and game instructions
* Players.json file stores the game data for all players as a list of dictionaries. In the format of:  
        
          [{"cur_score": 0,  
            "attempt": 2,   
            "name": "name1"  
            "cur_question": 5,  
            "high_score": 60,  
            "game_num": 2}]

* If the player signs in with a username already used it will load up the players data on record.
* The username must be of the form "^[a-zA-Z0-9]+$". This requirement is set in the html code.
* Once the player enters a username a brief welcome message is displayed, informing the player of their current game status. This allows the user to enter in a different username if they are a new player, before playing the game.
* Each questions data is stored in a tree_lib.json as a list of dictionaries. in the format of:
       
         [{"question": 1,  
         "tree_image": "/static/img/arbutus.jpg",  
         "tree_name": "arbutus"}]

* As the game progresses the question number is incremented by one and the relevant image and tree_name/answer are retrieved using the question number.
* The player is presented with the image of a tree, a brief request to enter the tree name, along with an input box for the answer and submit button.
* The answer may not contain any spaces and must be of form "^[a-zA-Z0-9]+$". This requirement is set in the html code.
* The player can keep track of their game with the progress states displayed on screen, current question, attempt number and current score are displayed. The attempt number is hidden in smaller screen resolutions.
* Once the player submits an answer the answer is processed, there data is updated in the players.json file and a feedback message is displayed on the screen.
* If the player answers correctly a green tick and  congratulatory message is displayed and 'Next Question' button is made visible.
* If the player answers incorrectly on their first attempt at the question, a red x with a message stating that their answer was incorrect and they have another attempt, is displayed,
* If the player answers incorrectly on their second attempt at the question, a red x with a message stating the correct answer is displayed, along with the 'Next Question' button.
* The player gets 10 points for every question answer correctly on their first attempt and 5 points for answered correctly on their second attempt.
* Once the 10th question has been submitted the player is presented with a Game Over screen, displayed their final score and a a game feedback message. 
* The feedback message compares the players current score to their high score on record as well as to the leaderboard and displays an appropriate message.
* The a 5 ranked leaderboard is also displayed. The leaderboard data is stored in leaderboard.json. To be included in the leaderboard the player must score higher than their high score on record and higher than the lowest score on the leaderboard.
* If the player scores the same as their high score it does not make any changes, but if the score is the same as the lowest score on the leaderboard it knocks out the older player.
* From the Game Over screen the player can play the game again without having to reenter the username.

__Features Left to Implement__
* Develop code so that the images are not shown in the same sequence during each game. Some use of the random function, should be used.
* Include more trees, make the game longer.
* Display a hint for the second attempt at a question.
* Have a section giving detailed information on each of the tree species. 
* On the Game Over screen show all the pictures, displaying which ones were answered correctly and which ones were wrong. Use a list to save if the user got each question wrong of right.

Testing
-----------------------


__Automated Testing__

Throughout the development of this project a 'Test After - Automated Testing' approach was taken. After deciding what was needed, the function was written, manually tested 
while developing. Once a basic function was built, an automated test was written in test_quiz.py using unittest testing framework for each of the possible conditions.
As functions became more complex and interacted with other functions, these automated tests insured that the functions all maintained their required functionality. 
The tests are written quite explicitly, to ensure it is clear as to what each test is testing. This resulted in a very long repetitive testing code, but made troubleshooting simpler.

In run.py there are 10 functions that do not render html templates. 8 of these have automated tests written in test_quiz.py. The other 2 use text book code to read and write to .json files.
As the .json files would be constantly changing, these were manually tested. For all template rendering functions manual testing was performed.

__Visual Testing__

The dev tool within Google Chrome was used to test that the pages were displaying correctly (alignment, spacing, position etc) across different screen widths.


|                                    | Galaxy S5 | Pixel 2 | Pixel 2XL | iPhone 5/SE |	iPhone 6/7/8  | iPhone 6/7/8 + | iPhone X | iPad  | iPad Pro   | Responsive 1366 x 768 | Responsive 1680 x 1050 |  
| ---------------------------------- | --------- | ------- | --------- | ----------- | -------------- | -------------- | -------- | ------| ---------- | --------------------- | ---------------------- |
| index.html (sign-in)               | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| index.html (play game)             | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| leaderboard.html                   | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| instructions.html                  | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (ask question)           | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (wrong, go again)        | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (wrong, next question)   | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| quiz.html (correct, next question) | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 
| game_over.html                     | OK        | OK      | OK        | OK          | OK             | OK             | OK       | OK    | OK         | OK                    | OK                     | 



__Manual Testing__

The following test were performed manually. Care was taken that all relevant messages were correctly displayed.
During initial testing it was noted that if the user refreshed the page during game play that questions could be skipped, 
and even increment the users score without entering an answer. The function was changed in run.py to correct this bug.


|                                   | Chrome (Desktop) | Edge (Desktop) | Chrome (Mobile) | Samsung Internet (Mobile)|
| ----------------------------      | ---------------- | -------------- | --------------- | ------------------------ |
| __index.html__                                                                                                     |                                                                                
| Sign in Btn (blank name)          | OK               | OK             | OK              | OK                       |
| Sign in Btn (new name)            | OK               | OK             | OK              | OK                       |
| Sign in Btn (old name)            | OK               | OK             | OK              | OK                       |
| Play Game Btn                     | OK               | OK             | OK              | OK                       |
| Refresh (reloads index.html with blank input box) | OK | OK           | OK              | OK                       |
| __quiz.html__                                                                                                      |                                                                                
| Submit Btn (blank answer)         | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 1, correct)   | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 1, incorrect) | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 2, incorrect) | OK               | OK             | OK              | OK                       |
| Submit Btn (attempt 2, correct)   | OK               | OK             | OK              | OK                       |
| Next Question Btn                 | OK               | OK             | OK              | OK                       |
| players.json updating             | OK               | OK             | OK              | OK                       |
| Refresh before submit (reloads quiz.html with same question) | OK |OK | OK              | OK                       |
| Refresh after submit (warning that form data will be re-entered, submitted answer will continue to be submitted for the next question) | OK | OK  | OK| OK|
| __game_over.html__                                                                                                 |                                                                                
| leaderboard.json up to date       | OK               | OK             | OK              | OK                       |
| players.json up to date           | OK               | OK             | OK              | OK                       |
| Play Again Btn                    | OK               | OK             | OK              | OK                       |
| Refresh (loads quiz.html with new game)| OK          | OK             | OK              | OK                       |
| __instructions.html__                                                                                              |                                                                                
| Sign in Btn                       | OK               | OK             | OK              | OK                       |
| Refresh (reloads instructions.html| OK               | OK             | OK              | OK                       |

Multiplayer parallel play was tested by signing in with the two usernames in different browsers (Chrome & Edge) and answering questions at the same time.
Players.json updated correctly without the seperate games conflicting.
It was also tested if the same username was playing on two different browsers at the same time. The player would be unaware except that questions would be skipped as they are already been answered by the other browser.




__Hosting__

A Procfile is required by Heroku to know what language to launch the application as. 
In Heroku the config variables were set:

IP: 0.0.0.0  
Port: 5000




