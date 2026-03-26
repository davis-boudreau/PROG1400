import turtle
import random

# Define Variables
score_a = 0
score_b = 0
max_move_speed = 15  # Set a fixed maximum move speed

# Setup the drawing pallet
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Define Paddle A Class to use the methods
paddle_a = turtle.Turtle()
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.speed(10)
paddle_a.shapesize(stretch_wid=5,stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350,0)

# Define Paddle B Class to use the methods
paddle_b = turtle.Turtle()
#Methods
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.speed(0)
paddle_b.shapesize(stretch_wid=5,stretch_len=1)
paddle_b.penup()
paddle_b.goto(350,0)

# Define the ball Class to use the methods
ball = turtle.Turtle()
#Methods
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0,0)
# Define the ball movement
ball.dx = 0.05
ball.dy = 0.05

# Define the scoreboard class to use methods
score_board = turtle.Turtle()
# Methods
score_board.speed(0)
score_board.shape("square")
score_board.color("white")
score_board.penup()
score_board.hideturtle()
score_board.goto(0,260)
score_board.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", 
          font=("Courier", 24, "normal"))

# Define a function to move the paddle up
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

# Define a function to move the paddle down
def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

# Define a function to move the paddle up
def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

# Define a function to move the paddle down
def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "Up")
wn.onkeypress(paddle_a_down, "Down")
#wn.onkeypress(paddle_b_up, "w")
#wn.onkeypress(paddle_b_down, "s")
# Main
playing = True
while playing:
    wn.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    if ball.xcor() >= -240:
        distance_to_ball = abs(paddle_b.xcor() - ball.xcor())
        # Calculate the move speed as a proportion of the distance to the ball, but capped at max_move_speed
        move_speed = min(max_move_speed, distance_to_ball * 0.05)

        # Decide if there's an error
        error_occurred = random.randint(1, 100) <= 10

        if ball.dx > 0 or error_occurred:  # Move the paddle when the ball is moving towards it OR if there's an error
            if distance_to_ball > 50:  # Only move if the paddle is more than 50 units away from the ball
                if error_occurred:
                    # Randomly move up or down irrespective of the ball's position
                    if random.randint(0, 1) == 0:
                        paddle_b.sety(paddle_b.ycor() + move_speed)
                    else:
                        paddle_b.sety(paddle_b.ycor() - move_speed)
                else:
                    if paddle_b.ycor() < ball.ycor():
                        paddle_b.sety(paddle_b.ycor() + move_speed)
                    elif paddle_b.ycor() > ball.ycor():
                        paddle_b.sety(paddle_b.ycor() - move_speed)
        else:
            paddle_b.setposition(paddle_b_latest_vect['x'],paddle_b_latest_vect['y'])
        # AI End

    # Check Top and Bottom Borders
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy = ball.dy * -1
    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy = ball.dy * -1
    # Check Left and Rights Borders
    if ball.xcor() > 390:
        score_a = score_a + 1
        score_board.clear()
        score_board.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", 
          font=("Courier", 24, "normal"))
        ball.goto(0,0)
    elif ball.xcor() < -390:
        score_b = score_b + 1
        score_board.clear()
        score_board.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", 
          font=("Courier", 24, "normal"))
        ball.goto(0,0)
    
    # Paddle and Ball Collision
    if ball.xcor() < -340 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50:
        ball.dx = ball.dx * - 1
    elif ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
        ball.dx = ball.dx * - 1
        paddle_b_latest_vect = {'x':paddle_b.xcor(),'y':paddle_b.ycor()}
wn.bye()



    


