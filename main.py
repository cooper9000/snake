import turtle

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.screensize(300, 300)

# Make the snake
snake = turtle.Turtle()
snake.shape("square")
snake.color("white")
snake.penup()

# Main function for user input with keyboard
def movement_controls():

    def right():
        snake.setheading(0)
        snake.forward(50)

    def left():
        snake.setheading(180)
        snake.forward(50)

    def up():
        snake.setheading(90)
        snake.forward(50)

    def down():
        snake.setheading(270)
        snake.forward(50)

    # Keyboard controls
    screen.onkey(right, "d")
    screen.onkey(left, "a")
    screen.onkey(up, "w")
    screen.onkey(down, "s")

    screen.listen()


movement_controls()

# Start the window
screen.mainloop()
