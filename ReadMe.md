- Title: Memory Test game
- Description: 
This game will challenge a player’s memory and cognitive skills.
Developing a memory game using Python as a programming language.
Implementing a user-friendly GUI for gameplay.
This game will have features like randomized number placement, varying difficulty levels, and performance tracking.
Conduct user testing to evaluate the game’s effectiveness and usability.
Maintains a record of the scores and rank of the player in the database.


Technical Aspects
Programming Language: Python
GUI Framework: pygame_gui
Database: Postgres
Library: Pygame, psycopg2, sys, pygame_gui
User Interface Design: This will include the menus, buttons, and sets that will be utilized to manage game data and store player’s progress.


INSTALLATION
- Dependencies: pygame,pygame_gui,psycopg2.

Steps to set up the project:
- command to install: pip install pygame,pygame_gui,psycopg2
- to run the code give command python3 game.py

- Examples: added the screenshots of the game
- Configuration: there are no special instructions for the user just follow the above mentioned steps to play the game.

- List of Features: Our project focuses on providing a fun time for the user to play the game and side by side check their memory skills.

- Guidelines: task distribution is as follows:
   * Sachin - Worked on Database
   * Jiseok - worked on the functionality of pygame
   * Yashasvini - worked on the functionality of python in overall code
- Code Style: We majorly used Python as programming language, and used postgress as a database.

- Authors: 
   - Jiseok Shim (122758170) 
   - Sachin Brahman (141237230)
   - Yashasvini BHanuraj (164581217)

- Acknowledgments: We as a group decided to prepare this game. We got inspired from the chimpenze game. Link for which is -      https://humanbenchmark.com/tests/chimp

- License Information: MIT license

- FAQ:

Q: How do I start the game?
A: To start the game, simply click on the circular button located at the bottom left corner of the screen.

Q: How do I input my name to play the game?
A: Your name input will be prompted on the screen. Type your name into the text field and press Enter to proceed.

Q: What happens if I click on the wrong number during gameplay?
A: If you click on the wrong number, the game will end, and your score will be displayed along with the leaderboard.

- Troubleshooting:

Issue: Unable to connect to the database.
Solution: Ensure that the database credentials (DB_USER, DB_PASSWORD, etc.) are correctly configured in the script and that the database server is running.

Issue: Game freezes or crashes unexpectedly.
Solution: Check for any errors displayed in the console. Ensure that all dependencies, including Pygame and psycopg2, are installed correctly. Debug any syntax errors or logical issues in the code.

Issue: Name input field does not appear.
Solution: Verify that Pygame GUI elements are properly initialized and rendered. Check for any errors related to UI element creation and management.

- Roadmap:

Implement additional levels with increased difficulty.
Add sound effects and background music to enhance the gaming experience.
Introduce power-ups or special features to make gameplay more engaging.
Implement multiplayer functionality to allow players to compete against each other.
Improve UI/UX design for better visual appeal and user interaction.
Changelog:

Version 1.0:
Initial release of the game with basic features, including name input, gameplay mechanics, and database integration.
Version 1.1:
Added leaderboard functionality to display top scores.
Implemented error handling for database connections and queries.
Version 1.2:
Optimized code for better performance and readability.
Fixed minor bugs and glitches reported by users.
Version 1.3:
Introduced Pygame GUI for improved user interface and interactivity.
Enhanced game visuals and added animation effects.
Version 1.4:
Implemented dynamic level scaling based on player performance.
Added troubleshooting tips and FAQ section to the documentation.
Version 1.5 (Planned):
Integration with online leaderboard service for global score tracking.
Refinement of game mechanics based on user feedback.
Compatibility updates for cross-platform support.
