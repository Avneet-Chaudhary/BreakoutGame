import turtle
import time

# Set up the screen
window = turtle.Screen()
window.title("Breakout Clone")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)

# Score and High Score
score = 0
high_score = 0

# Paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = -2

# Bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]
brick_rows = 5
brick_cols = 10
brick_width = 50
brick_height = 20
brick_start_x = -230
brick_start_y = 180

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(colors[row])
        brick.penup()
        x = brick_start_x + col * brick_width
        y = brick_start_y - row * brick_height
        brick.goto(x, y)
        bricks.append(brick)

# Score display
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: 0  High Score: 0",
                    align="center", font=("Courier", 18, "normal"))

# Paddle movement


def move_left():
    x = paddle.xcor()
    if x > -250:
        x -= 20
    paddle.setx(x)


def move_right():
    x = paddle.xcor()
    if x < 230:
        x += 20
    paddle.setx(x)


# Keyboard bindings
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")

# Ball speed (faster ball)
# Adjust this value to control the ball's speed (smaller values make it faster)
ball_speed = 0.001

# Function to handle ball-paddle collisions


def handle_paddle_collision():
    if (
        ball.ycor() < -240
        and paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60
        and ball.dy < 0
    ):
        ball.sety(-240)  # Bounce the ball back up
        ball.dy *= -1

# Function to handle ball-brick collisions and increase ball speed


def handle_brick_collision():
    # Declare score, high_score, and ball_speed as global to modify the global variables
    global score, high_score, ball_speed

    for brick in bricks:
        if ball.distance(brick) < 20:
            ball.dy *= -1
            brick.goto(1000, 1000)  # Move the brick out of the visible area
            bricks.remove(brick)   # Remove the brick from the list
            score += 10

            # Update the score display
            if score > high_score:
                high_score = score

            score_display.clear()
            score_display.write("Score: {}  High Score: {}".format(
                score, high_score), align="center", font=("Courier", 18, "normal"))

            # Increase ball speed
            if ball_speed > 0.005:  # Set a minimum speed to avoid excessively fast ball
                ball_speed -= 0.001
            break  # Break the loop to avoid hitting multiple bricks in one frame

# Function to handle game over


def game_over():
    global score, high_score, ball_speed

    ball.goto(0, 0)
    ball.dx = 0
    ball.dy = 0
    ball.color("black")

    # Clear the previous ball message
    ball.clear()

    ball.write("Game Over", align="center", font=("Courier", 24, "normal"))
    time.sleep(2)

    # Get the player's name for high score
    player_name = turtle.textinput("New High Score!", "Enter your name:")

    # Add the player's name and high score to a file
    with open("high_scores.txt", "a") as file:
        file.write(f"{player_name}: {high_score}\n")

    # Reset the bricks
    for brick in bricks:
        brick.goto(brick_start_x, brick_start_y)
    bricks.clear()

    # Reset the ball and paddle
    ball.goto(0, 0)
    ball.dx = 2
    ball.dy = -2
    paddle.goto(0, -250)

    # Re-create the bricks
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(colors[row])
            brick.penup()
            x = brick_start_x + col * brick_width
            y = brick_start_y - row * brick_height
            brick.goto(x, y)
            bricks.append(brick)

    # Reset the score and ball speed
    score = 0
    ball_speed = 0.001  # Reset the ball speed to the initial value
    score_display.clear()
    score_display.write("Score: {}  High Score: {}".format(
        score, high_score), align="center", font=("Courier", 18, "normal"))


# Main game loop
while True:
    window.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Check for collisions with the window borders
    if ball.xcor() > 290 or ball.xcor() < -290:
        ball.dx *= -1

    if ball.ycor() > 290:
        ball.dy *= -1

    # Check for collisions with the paddle
    handle_paddle_collision()

    # Check for collisions with the bricks and increase ball speed
    handle_brick_collision()

    # Check if all bricks are destroyed
    if len(bricks) == 0:
        ball.goto(0, 0)
        ball.dx = 0
        ball.dy = 0
        ball.color("black")
        ball.write("You Win!", align="center", font=("Courier", 24, "normal"))
        break

    # Game over condition: Ball goes below the paddle
    if ball.ycor() < -290:
        game_over()

    # Increase ball speed over time for added difficulty
    if ball.dx > 0:
        ball.dx += 0.001
    else:
        ball.dx -= 0.001

    if ball.dy > 0:
        ball.dy += 0.001
    else:
        ball.dy -= 0.001

    # Delay the game to control the ball's speed
    time.sleep(ball_speed)

# Keep the window open until the user closes it
