import turtle

# Define Variables
score_a = 0
score_b = 0

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
ball.shape("circle")
ball.pensize("105")
ball.color("white")
ball.penup()
ball.goto(0,0)
# Define the ball movement
ball.dx = 0.2
ball.dy = 0.2

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
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
# Main
playing = True
while playing:
    wn.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

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
        if ball.ycor() <= -290 + -10 or ball.ycor() >= 290 + 10:
            ball.dy = ball.ycor() * - 1
        else:
            ball.dx = ball.dx * - 1
    elif ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
        if ball.ycor() <= -290 + -10 or ball.ycor() >= 290 + 10:
            ball.dy = ball.ycor() * - 1
        else:
            ball.dx = ball.dx * - 1




    


