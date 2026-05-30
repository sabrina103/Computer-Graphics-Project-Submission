import turtle

# --- Game State ---
board = [" " for _ in range(9)]
current_player = "X"
starting_player = "X"  # Keeps track of who starts the round
game_active = True

# --- Setup Screen ---
screen = turtle.Screen()
screen.title("Tic-Tac-Toe")
screen.setup(width=600, height=600)
screen.bgcolor("#f0f0f0")
screen.tracer(0)  # Turns off animation for instant drawing

# --- Drawer Turtles ---
grid_drawer = turtle.Turtle()
grid_drawer.hideturtle()
grid_drawer.pensize(5)

piece_drawer = turtle.Turtle()
piece_drawer.hideturtle()
piece_drawer.pensize(7)

status_drawer = turtle.Turtle()
status_drawer.hideturtle()
status_drawer.penup()

# --- Functions ---

def draw_grid():
    """Draws the shifted 3x3 grid lines and UI elements."""
    grid_drawer.clear()
    grid_drawer.color("#333333")
    
    # Vertical lines (kept between Y: 150 and -300)
    for x in [-75, 75]:
        grid_drawer.penup()
        grid_drawer.goto(x, 150)
        grid_drawer.pendown()
        grid_drawer.goto(x, -300)
        
    # Horizontal lines
    for y in [-150, 0]:
        grid_drawer.penup()
        grid_drawer.goto(-225, y)
        grid_drawer.pendown()
        grid_drawer.goto(225, y)
        
    # Draw Reset Button safely in the top right area
    grid_drawer.penup()
    grid_drawer.goto(120, 240)
    grid_drawer.color("#d9534f")
    grid_drawer.begin_fill()
    for _ in range(2):
        grid_drawer.forward(100)
        grid_drawer.right(90)
        grid_drawer.forward(45)
        grid_drawer.right(90)
    grid_drawer.end_fill()
    
    grid_drawer.color("white")
    grid_drawer.goto(170, 208)
    grid_drawer.write("RESET", align="center", font=("Arial", 12, "bold"))
    
    update_status()
    screen.update()

def update_status(message=None):
    """Updates the turn/win message safely in the top left corner."""
    status_drawer.clear()
    status_drawer.goto(-220, 210)
    status_drawer.color("#333333")
    
    if message:
        status_drawer.write(message, font=("Arial", 14, "bold"))
    else:
        status_drawer.write("Player Turn: {}".format(current_player), font=("Arial", 14, "bold"))
    screen.update()

def draw_x(x, y):
    """Draws an X centered at (x, y)."""
    piece_drawer.color("#007acc")
    piece_drawer.penup()
    piece_drawer.goto(x - 30, y + 30)
    piece_drawer.pendown()
    piece_drawer.goto(x + 30, y - 30)
    piece_drawer.penup()
    piece_drawer.goto(x + 30, y + 30)
    piece_drawer.pendown()
    piece_drawer.goto(x - 30, y - 30)

def draw_o(x, y):
    """Draws an O centered at (x, y)."""
    piece_drawer.color("#e67e22")
    piece_drawer.penup()
    piece_drawer.goto(x, y - 30)
    piece_drawer.pendown()
    piece_drawer.circle(30)

def check_win():
    """Checks if there is a winner on the board."""
    win_coords = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
        [0, 4, 8], [2, 4, 6]             # Diagonal
    ]
    for coord in win_coords:
        if board[coord[0]] == board[coord[1]] == board[coord[2]] != " ":
            return board[coord[0]]
    return None

def check_tie():
    """Checks if the board is full with no winner."""
    return " " not in board

def reset_game():
    """Resets the board state and alternates who starts the new round."""
    global board, current_player, starting_player, game_active
    board = [" " for _ in range(9)]
    piece_drawer.clear()
    
    if starting_player == "X":
        starting_player = "O"
    else:
        starting_player = "X"
        
    current_player = starting_player
    game_active = True
    draw_grid()

def handle_click(x, y):
    """Handles click coordinates adapted specifically for the shifted grid."""
    global current_player, game_active

    # Check if Reset button is clicked (New UI position bounds)
    if 120 <= x <= 220 and 195 <= y <= 240:
        reset_game()
        return

    if not game_active:
        return

    # Check if click falls within the valid shifted 3x3 play grid bounds
    if -225 <= x <= 225 and -300 <= y <= 150:
        # Determine column (0, 1, 2)
        col = int((x + 225) // 150)
        # Determine row (0, 1, 2) from top to bottom
        row = int((150 - y) // 150)
        
        if 0 <= col <= 2 and 0 <= row <= 2:
            index = row * 3 + col
            
            if board[index] == " ":
                board[index] = current_player
                
                # Dynamic centers for the updated board sizes
                center_x = -150 + (col * 150)
                center_y = 75 - (row * 150)
                
                if current_player == "X":
                    draw_x(center_x, center_y)
                    winner = check_win()
                    if winner:
                        update_status("Player {} Wins! Click RESET.".format(winner))
                        game_active = False
                    elif check_tie():
                        update_status("It's a Tie! Click RESET.")
                        game_active = False
                    else:
                        current_player = "O"
                        update_status()
                else:
                    draw_o(center_x, center_y)
                    winner = check_win()
                    if winner:
                        update_status("Player {} Wins! Click RESET.".format(winner))
                        game_active = False
                    elif check_tie():
                        update_status("It's a Tie! Click RESET.")
                        game_active = False
                    else:
                        current_player = "X"
                        update_status()
                        
                screen.update()

# --- Initialize Game ---
draw_grid()

screen.onclick(handle_click)
screen.mainloop()