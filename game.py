import pygame
import pygame_gui
from random import *
import sys
import psycopg2

# Database configuration
DB_NAME = 'defaultdb'
DB_USER = 'admin'
DB_PASSWORD = "nzzh3o4nu7b82Mo0u3Sp2A97"
DB_HOST = "typically-powerful-falcon-iad.a1.pgedge.io"
DB_PORT = "5432"

# Function to connect to the database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to database successfully!")
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        sys.exit(1)

# Function to create 'scores' table in the database
def create_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                player_name VARCHAR(100) NOT NULL,
                score INTEGER NOT NULL
            );
        """)
        conn.commit()
        print("Table 'scores' created successfully!")
    except psycopg2.Error as e:
        print("Error creating table:", e)
        conn.rollback()
        sys.exit(1)
    finally:
        cur.close()

# Function to get player's name using Pygame GUI
def get_user_name(screen, manager):
    global player_name
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                player_name = event.text
                return player_name
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        screen.fill(BLACK)
        manager.draw_ui(screen)
        pygame.display.update()

# Function to set up the game grid
def setup(level):
    global conn
    number_count = (level // 3) + 5
    shuffle_grid(number_count)
    create_table(conn)

# Function to shuffle numbers in the grid
def shuffle_grid(number_count):
    rows = 5
    columns = 9
    cell_size = 130
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20
    grid = [[0 for col in range(columns)] for row in range(rows)]
    number = 1
    while number <= number_count:
        row_idx = randrange(0, rows)
        col_idx = randrange(0, columns)
        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)
            number_buttons.append(button)
    print(grid)

# Function to display start screen
def display_start_screen(screen, curr_level):
    start_button = pygame.Rect(0, 0, 120, 120)
    start_button.center = (120, screen.get_height() - 120)
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)
    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)
    screen.blit(msg, msg_rect)
    pygame.display.update()

# Function to display the game screen
def display_game_screen():
    global hidden
    for idx, rect in enumerate(number_buttons, start=1):
        if hidden:
            pygame.draw.rect(screen, WHITE, rect)
        else:
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

# Function to check buttons clicked by the user
def check_buttons(pos):
    global start
    if start:
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True

# Function to check if the correct number button is clicked
def check_number_buttons(pos):
    global start, hidden, curr_level
    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]:
                print("Correct")  
                del number_buttons[0]
                if not hidden:
                    hidden = True
            else:
                game_over(conn)
            break
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

# Function to handle game over event
def game_over(conn):
    global running, player_name, curr_level
    msg = game_font.render(f"{player_name}'s score - {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/5))
    save_score(conn, player_name, curr_level)
    screen.fill(BLACK)
    screen.blit(msg, msg_rect)
    display_leaderboard(conn)
    pygame.display.update()
    conn.close()
    running = False

# Function to save player's score to the database
def save_score(conn, player_name, score):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO scores (player_name, score) VALUES (%s, %s)", (player_name, score))
        conn.commit()
    except psycopg2.Error as e:
        print("Error saving score:", e)
        conn.rollback()
        sys.exit(1)
    finally:
        cur.close()

# Function to display leaderboard
def display_leaderboard(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 10")
        leaderboard = cur.fetchall()
        y_offset = 50
        for i, (leader_name, leader_score) in enumerate(leaderboard, start=1):
            msg = ranking_font.render(f"{i}. {leader_name}: {leader_score}", True, WHITE)
            msg_rect = msg.get_rect(center=(screen_width/2, screen_height/4 + y_offset))
            screen.blit(msg, msg_rect)
            y_offset += 50
    except psycopg2.Error as e:
        print("Error displaying leaderboard:", e)
        conn.rollback()
        sys.exit(1)
    finally:
        cur.close()

# Initialize Pygame
pygame.init()
player_name = ""
clock = pygame.time.Clock()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")
game_font = pygame.font.Font(None, 120)
ranking_font = pygame.font.Font(None, 70)
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
number_buttons = []
curr_level = 1
display_time = None
start_ticks = None

conn = connect_to_database()

# Start Game
start = False
hidden = False

setup(curr_level)

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text Input in PyGame | BaralTech")

manager = pygame_gui.UIManager((1600, 900))

text_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((350, 275), (600, 50)), manager=manager, object_id='#main_text_entry')

UI_REFRESH_RATE = clock.tick(60) / 1000

running = True  # Flag to check if the game is running
name_entered = False  # Flag to track if the user has entered their name
show_name_input = True  # Flag to control rendering of the name input field

# Game Loop
while running:
    click_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close Window
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:  # When user clicks mouse
            click_pos = pygame.mouse.get_pos()
            print(click_pos)
        # Process events for the text input
        manager.process_events(event)

    screen.fill(BLACK)

    if not start:
        if not name_entered and show_name_input:
            user_name = get_user_name(screen, manager)
            if user_name:
                name_entered = True
                show_name_input = False
        else:
            display_start_screen(screen, curr_level)  # Show the start screen after getting user name
    else:
        display_game_screen()

    if click_pos:
        check_buttons(click_pos)

    # Check game over condition
    if len(number_buttons) == 0:  # If all buttons are clicked
        game_over(conn)

    # Update the GUI manager
    manager.update(UI_REFRESH_RATE)

    # Draw UI elements based on game state
    if show_name_input:
        manager.draw_ui(screen)

    # Display Update
    pygame.display.update()

pygame.time.delay(10000)

# After the game loop ends, close the database connection
conn.close()
pygame.quit()
