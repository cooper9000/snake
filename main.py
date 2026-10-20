import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("#0a0a1a")
screen.setup(width=660, height=720)
screen.tracer(0)

# Game variables
snake_segments = []
direction = "right"
game_started = False
game_over_flag = False
score = 0
high_score = 0


# --- DRAW THE CHECKERBOARD ---

tile_drawer = turtle.Turtle()
tile_drawer.hideturtle()
tile_drawer.penup()
tile_drawer.speed(0)


def draw_tiles():
    tile_drawer.clear()

    # Draw 28 rows and 28 columns of tiles
    row = 0
    while row < 28:
        col = 0
        while col < 28:
            # Figure out where to put this tile
            x = -280 + col * 20
            y = 250 - row * 20

            # Pick a color for the checkerboard pattern
            if (row + col) % 2 == 0:
                tile_drawer.fillcolor("#1a1a2e")
            else:
                tile_drawer.fillcolor("#16213e")

            # Draw the tile
            tile_drawer.goto(x, y)
            tile_drawer.begin_fill()
            tile_drawer.forward(20)
            tile_drawer.left(90)
            tile_drawer.forward(20)
            tile_drawer.left(90)
            tile_drawer.forward(20)
            tile_drawer.left(90)
            tile_drawer.forward(20)
            tile_drawer.left(90)
            tile_drawer.end_fill()
            col = col + 1
        row = row + 1

    # Draw a glowing border (3 lines on top of each other)
    tile_drawer.goto(-280, -310)
    tile_drawer.pencolor("#0f3460")
    tile_drawer.pensize(7)
    tile_drawer.pendown()
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.penup()

    tile_drawer.goto(-280, -310)
    tile_drawer.pencolor("#1a5276")
    tile_drawer.pensize(4)
    tile_drawer.pendown()
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.penup()

    tile_drawer.goto(-280, -310)
    tile_drawer.pencolor("#2471a3")
    tile_drawer.pensize(2)
    tile_drawer.pendown()
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.forward(560)
    tile_drawer.left(90)
    tile_drawer.penup()


# --- FOOD ---

food = turtle.Turtle()
food.hideturtle()
food.penup()

food_drawer = turtle.Turtle()
food_drawer.hideturtle()
food_drawer.penup()


def draw_food():
    food_drawer.clear()
    fx = food.xcor()
    fy = food.ycor()

    # Draw layers from biggest to smallest for a glow effect
    food_drawer.goto(fx, fy)
    food_drawer.dot(24, "#4a0000")
    food_drawer.dot(18, "#8b0000")
    food_drawer.dot(14, "#ff3333")
    food_drawer.dot(8, "#ff6666")


def place_food():
    # Keep trying random spots until we find one not on the snake
    looking = True
    while looking:
        # Pick a random tile on the board
        col = random.randint(0, 27)
        row = random.randint(0, 27)
        x = -280 + col * 20 + 10
        y = 250 - row * 20 - 10

        # Check if any snake segment is at that spot
        on_snake = False
        for segment in snake_segments:
            if segment.distance(x, y) < 10:
                on_snake = True

        if not on_snake:
            food.goto(x, y)
            draw_food()
            looking = False


# --- HEADER / TITLE ---

title_deco = turtle.Turtle()
title_deco.hideturtle()
title_deco.penup()


def draw_header():
    title_deco.clear()
    title_deco.goto(0, 290)
    title_deco.color("#2471a3")
    title_deco.write("SNAKE", align="center",
                     font=("Courier", 28, "bold"))

    # A decorative line under the title
    title_deco.goto(-100, 285)
    title_deco.pencolor("#0f3460")
    title_deco.pensize(2)
    title_deco.pendown()
    title_deco.goto(100, 285)
    title_deco.penup()


# --- SCOREBOARD ---

scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()


def update_score():
    scoreboard.clear()

    # Score on the left
    scoreboard.goto(-270, 258)
    scoreboard.color("#5dade2")
    scoreboard.write("SCORE  " + str(score), align="left",
                     font=("Courier", 14, "bold"))

    # Best on the right
    scoreboard.goto(270, 258)
    scoreboard.color("#a569bd")
    scoreboard.write("BEST  " + str(high_score), align="right",
                     font=("Courier", 14, "bold"))


# --- MESSAGES ---

start_message = turtle.Turtle()
start_message.hideturtle()
start_message.penup()

game_message = turtle.Turtle()
game_message.hideturtle()
game_message.penup()

restart_message = turtle.Turtle()
restart_message.hideturtle()
restart_message.penup()

overlay = turtle.Turtle()
overlay.hideturtle()
overlay.penup()


def show_start_screen():
    start_message.goto(0, -10)
    start_message.color("#5dade2")
    start_message.write("PRESS SPACE TO START", align="center",
                        font=("Courier", 18, "bold"))

    start_message.goto(0, -45)
    start_message.color("#3d6d8f")
    start_message.write("WASD or Arrow Keys to move", align="center",
                        font=("Courier", 12, "normal"))


def draw_overlay():
    # Dim the board by covering it with dark dots
    overlay.clear()
    row = 0
    while row < 28:
        col = 0
        while col < 28:
            x = -280 + col * 20 + 10
            y = 250 - row * 20 - 10
            overlay.goto(x, y)
            overlay.dot(22, "#0a0a1a")
            col = col + 1
        row = row + 1


# --- SNAKE ---

snake_drawer = turtle.Turtle()
snake_drawer.hideturtle()
snake_drawer.penup()


def draw_snake():
    snake_drawer.clear()

    i = 0
    while i < len(snake_segments):
        sx = snake_segments[i].xcor()
        sy = snake_segments[i].ycor()

        if i == 0:
            # Draw the head
            snake_drawer.goto(sx, sy)
            snake_drawer.dot(22, "#1a4a1a")
            snake_drawer.dot(18, "#27ae60")
            snake_drawer.dot(12, "#2ecc71")

            # Draw eyes based on direction
            if direction == "right":
                snake_drawer.goto(sx + 4, sy + 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx + 4, sy - 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx + 5, sy + 4)
                snake_drawer.dot(2, "black")
                snake_drawer.goto(sx + 5, sy - 4)
                snake_drawer.dot(2, "black")
            if direction == "left":
                snake_drawer.goto(sx - 4, sy + 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx - 4, sy - 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx - 5, sy + 4)
                snake_drawer.dot(2, "black")
                snake_drawer.goto(sx - 5, sy - 4)
                snake_drawer.dot(2, "black")
            if direction == "up":
                snake_drawer.goto(sx + 4, sy + 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx - 4, sy + 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx + 4, sy + 5)
                snake_drawer.dot(2, "black")
                snake_drawer.goto(sx - 4, sy + 5)
                snake_drawer.dot(2, "black")
            if direction == "down":
                snake_drawer.goto(sx + 4, sy - 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx - 4, sy - 4)
                snake_drawer.dot(4, "white")
                snake_drawer.goto(sx + 4, sy - 5)
                snake_drawer.dot(2, "black")
                snake_drawer.goto(sx - 4, sy - 5)
                snake_drawer.dot(2, "black")
        else:
            # Draw body segments - alternating shades of green
            if i % 2 == 0:
                snake_drawer.goto(sx, sy)
                snake_drawer.dot(20, "#196f3d")
                snake_drawer.dot(16, "#27ae60")
            else:
                snake_drawer.goto(sx, sy)
                snake_drawer.dot(20, "#145a32")
                snake_drawer.dot(16, "#229954")

        i = i + 1


def make_snake():
    head = turtle.Turtle()
    head.hideturtle()
    head.penup()
    head.goto(0, 0)
    snake_segments.append(head)


# --- DIRECTION CONTROLS ---

def go_right():
    global direction
    if direction != "left":
        direction = "right"


def go_left():
    global direction
    if direction != "right":
        direction = "left"


def go_up():
    global direction
    if direction != "down":
        direction = "up"


def go_down():
    global direction
    if direction != "up":
        direction = "down"


# --- GAME OVER ---

def game_over():
    global game_started, game_over_flag, high_score

    game_started = False
    game_over_flag = True

    # Update high score if we beat it
    if score > high_score:
        high_score = score
        update_score()

    draw_overlay()

    game_message.goto(0, 30)
    game_message.color("#e74c3c")
    game_message.write("GAME OVER", align="center",
                       font=("Courier", 36, "bold"))

    game_message.goto(0, -5)
    game_message.color("#ec7063")
    game_message.write("Score: " + str(score), align="center",
                       font=("Courier", 16, "normal"))

    restart_message.goto(0, -40)
    restart_message.color("#f9e79f")
    restart_message.write("Press R to Restart", align="center",
                          font=("Courier", 14, "bold"))


# --- RESTART ---

def restart_game():
    global game_started, game_over_flag, direction, score

    if not game_over_flag:
        return

    # Clear everything
    game_message.clear()
    restart_message.clear()
    scoreboard.clear()
    overlay.clear()
    snake_drawer.clear()
    food_drawer.clear()

    # Hide and remove all snake segments
    for segment in snake_segments:
        segment.hideturtle()
    snake_segments.clear()

    # Reset variables
    direction = "right"
    score = 0
    game_started = False
    game_over_flag = False

    # Set up again
    draw_tiles()
    make_snake()
    place_food()
    update_score()
    show_start_screen()
    screen.update()


# --- START ---

def start_game():
    global game_started
    if not game_started and not game_over_flag:
        game_started = True
        start_message.clear()
        game_loop()


# --- GAME LOOP ---

def game_loop():
    global score

    if not game_started:
        return

    # Remember the tail position so we can grow there if we eat food
    old_tail_x = snake_segments[-1].xcor()
    old_tail_y = snake_segments[-1].ycor()

    # Move each body piece to where the one in front of it was
    i = len(snake_segments) - 1
    while i > 0:
        prev_x = snake_segments[i - 1].xcor()
        prev_y = snake_segments[i - 1].ycor()
        snake_segments[i].goto(prev_x, prev_y)
        i = i - 1

    # Move the head one tile in the current direction
    head = snake_segments[0]
    x = head.xcor()
    y = head.ycor()

    if direction == "right":
        x = x + 20
    if direction == "left":
        x = x - 20
    if direction == "up":
        y = y + 20
    if direction == "down":
        y = y - 20

    head.goto(x, y)

    # Check if we ate the food
    if head.distance(food) < 15:
        new_segment = turtle.Turtle()
        new_segment.hideturtle()
        new_segment.penup()
        new_segment.goto(old_tail_x, old_tail_y)
        snake_segments.append(new_segment)

        score = score + 1
        update_score()
        place_food()

    # Check if we hit a wall
    hit_wall = False
    if head.xcor() > 270:
        hit_wall = True
    if head.xcor() < -270:
        hit_wall = True
    if head.ycor() > 240:
        hit_wall = True
    if head.ycor() < -300:
        hit_wall = True

    if hit_wall:
        game_over()
    else:
        # Check if we hit ourselves
        i = 1
        while i < len(snake_segments):
            if head.distance(snake_segments[i]) < 10:
                game_over()
            i = i + 1

    draw_snake()
    draw_food()
    screen.update()

    if game_started:
        screen.ontimer(game_loop, 100)


# --- SET EVERYTHING UP ---

draw_tiles()
draw_header()
make_snake()
place_food()
update_score()
show_start_screen()

# Keyboard controls
screen.onkey(start_game, "space")
screen.onkey(go_right, "d")
screen.onkey(go_left, "a")
screen.onkey(go_up, "w")
screen.onkey(go_down, "s")
screen.onkey(go_right, "Right")
screen.onkey(go_left, "Left")
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(restart_game, "r")
screen.listen()

screen.update()
screen.mainloop()
