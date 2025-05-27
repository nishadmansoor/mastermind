import turtle
import random
import time
from Marble import Marble
from Point import Point
from datetime import datetime

'''cursor_pen = turtle.Turtle()
cursor_pen.shape("arrow")
cursor_pen.color("cyan")
cursor_pen.penup()
cursor_pen.speed(0)
cursor_pen.setheading(0)'''

color_options = ["red", "blue", "green", "yellow", "purple", "black"]
color_buttons = []
current_guess = []
all_guesses = []
secret_code = []
player_name = ""

def setup_screen():
    screen = turtle.Screen()
    screen.title("Mastermind Game")
    screen.setup(width=850, height=700)
    screen.bgcolor("white")
    screen.tracer(0)
    return screen

def leadership_board():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(3)

    pen.penup()
    pen.goto(-330, 270)
    pen.pendown()
    for _ in range(2):
        pen.forward(420)
        pen.right(90)
        pen.forward(540)
        pen.right(90)

    pen.penup()
    pen.goto(190, 235)
    pen.pendown()
    pen.color("blue")
    pen.write("Leaders:", font=("Arial", 16, "bold"))

    pen.penup()
    pen.goto(185, 230)
    pen.pendown()
    pen.color("black")
    box_width = 200
    box_height = 120
    for _ in range(2):
        pen.forward(box_width)
        pen.right(90)
        pen.forward(box_height)
        pen.right(90)

    try:
        with open("leaderboard.txt", "r") as f:
            scores = f.readlines()

        pen.penup()
        pen.color("black")
        for i, line in enumerate(scores[:5]):
            pen.goto(200, 210 - i * 20)
            pen.write(line.strip(), font=("Arial", 12, "normal"))

    except FileNotFoundError:
        pass

def guess_board():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    start_y = 210
    for row in range(10):
        y = start_y - (row * 50)

        # guess rows
        x_start = -270
        for i in range(4):
            x = x_start + (i*50)
            pen.penup()
            pen.goto(x, y)
            pen.pendown()
            pen.circle(20)

        # answer pegs
        peg_start_x = -29
        peg_start_y = y + 10
        peg_space = 15
        for i in range(4):
            peg_x = peg_start_x + (i % 2) * peg_space
            peg_y = peg_start_y - (i // 2) * peg_space
            pen.penup()
            pen.goto(peg_x, peg_y)
            pen.dot(12, "black") # this is apparently the "outer ring"
            pen.dot(10, "white") # this is apparently the "inner fill"

'''def draw_cursor():
    global all_guesses
    cursor_pen.clear()
    row_y = 210 - (len(all_guesses) * 50)
    cursor_pen.goto(-320, row_y - 10)
    cursor_pen.showturtle()'''

def main_buttons():
    for button in color_buttons:
        try:
            button.pen.clear()
            button.pen.hideturtle()
            button.pen.goto(1000, 1000)  # move out of screen
            del button.pen
        except:
            pass
    color_buttons.clear()

    start_x = -275
    y = -300

    for i, color in enumerate(color_options):
        x = start_x + i * 50
        m = Marble(color=color, position=Point(x, y))
        m.draw()
        color_buttons.append(m)


def save_score(name, attempts):
    score = []
    try:
        with open("leaderboard.txt", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    n, guess_str = parts
                    guesses = int(guess_str.split()[0])
                    score.append((n,guesses))
    except FileNotFoundError:
        pass

    score.append((name, attempts))
    score.sort(key=lambda x: x[1])
    score = score[:5]

    with open("leaderboard.txt", "w") as f:
        for n,g in score:
            f.write(f"{n}: {g} guesses\n")

def count_bulls_and_cows(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(c), guess.count(c)) for c in set(guess)) - bulls
    return bulls, cows

def draw_feedback(bulls, cows, row_num):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    y = 210 - (row_num * 50)
    peg_start_x = -30
    peg_start_y = y + 10
    peg_space = 15

    results = ['black'] * bulls + ['red'] * cows
    random.shuffle(results) # position info is randomized, user cannot see which buttons are correct
    for i, color in enumerate(results[:4]):
        peg_x = peg_start_x + (i % 2) * peg_space
        peg_y = peg_start_y - (i // 2) * peg_space
        pen.goto(peg_x, peg_y)
        pen.dot(10, color)

def clear_guess_row():
    y = 230 - (len(all_guesses) * 50)
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    for i in range(4):
        x = -270 + i * 50
        pen.goto(x, y-20)
        pen.color("white")
        pen.begin_fill()
        pen.circle(20)
        pen.end_fill()

def click(x, y):
    global current_guess
    print(f"CLICK RECEIVED at ({x:.1f}, {y:.1f})")

    if len(current_guess) < 4:
        for button in color_buttons:
            if button.clicked_in_region(x, y) and button.color not in current_guess:
                current_guess.append(button.color)
                button.pen.clear()
                draw_guess()
                return

    if 'check_turtle' in globals() and globals()['check_turtle'].distance(x, y) < 45:
        handle_check(x, y)
        return
    if 'x_turtle' in globals() and globals()['x_turtle'].distance(x, y) < 45:
        handle_clear(x, y)
        return
    if 'quit_turtle' in globals() and globals()['quit_turtle'].distance(x, y) < 45:
        handle_quit(x, y)
        return


def draw_guess():
    clear_guess_row()
    y = 230 - (len(all_guesses) * 50)
    x_start = -270
    for i, color in enumerate(current_guess):
        pos = Point(x_start + i * 50, y)
        m = Marble(color=color, position=pos)
        m.draw()

def show_quit_message():
    global screen
    quit_popup = turtle.Turtle()
    quit_popup.speed(0)
    quit_popup.penup()
    quit_popup.hideturtle()
    screen.addshape("quitmsg.gif")
    quit_popup.shape("quitmsg.gif")
    quit_popup.goto(0, 0)
    #quit_popup.stamp()
    screen.update()
    time.sleep(3)

def handle_quit(x,y):
    show_quit_message()
    turtle.bye()

def handle_clear(x,y):
    current_guess.clear()
    clear_guess_row()
    draw_guess()
    main_buttons()
    
def handle_check(x, y):
    if len(current_guess) == 4:
        all_guesses.append(current_guess.copy())
        try:
            bulls, cows = count_bulls_and_cows(secret_code, current_guess.copy())
            draw_feedback(bulls, cows, len(all_guesses) - 1)

            if bulls == 4:
                save_score(player_name, len(all_guesses))

                screen.clear()
                screen.bgcolor("white")

                win_popup = turtle.Turtle()
                win_popup.speed(0)
                win_popup.penup()
                win_popup.hideturtle()

                screen.addshape("winner.gif")
                win_popup.shape("winner.gif")
                win_popup.goto(0, 0)
                win_popup.stamp()

                screen.update()
                time.sleep(4)
                turtle.bye()

            elif len(all_guesses) >= 10:
                screen.clear()
                screen.bgcolor("white")

                lose_popup = turtle.Turtle()
                lose_popup.speed(0)
                lose_popup.penup()
                lose_popup.hideturtle()

                screen.addshape("lose.gif")
                lose_popup.shape("lose.gif")
                lose_popup.goto(0, 50)
                lose_popup.stamp()

                # 💬 Show the secret code
                msg = f"The secret code was: {', '.join(secret_code)}"
                lose_popup.goto(0, -100)
                lose_popup.color("black")
                lose_popup.write(msg, align="center", font=("Arial", 14, "bold"))

                screen.update()
                time.sleep(4)
                turtle.bye()

        except Exception as e:
            with open("mastermind_errors.err", "a") as f:
                f.write(f"[{datetime.now()}] {type(e).__name__}: {e}\n")

        current_guess.clear()
        clear_guess_row()
        draw_guess()
        main_buttons()
        #draw_cursor()

def main():
    global screen, secret_code, player_name
    turtle.TurtleScreen._RUNNING = True
    turtle.clearscreen()
    screen = setup_screen()

    check_turtle = turtle.Turtle()
    x_turtle = turtle.Turtle()
    quit_turtle = turtle.Turtle()

    globals().update({
        "check_turtle": check_turtle,
        "x_turtle": x_turtle,
        "quit_turtle": quit_turtle,
    })
    player_name = turtle.textinput("Welcome to Mastermind!", "Enter your name: ")
    secret_code = random.sample(color_options, 4)
    print("Secret Code:", secret_code)
    leadership_board()
    main_buttons()
    guess_board()
    #draw_cursor()

    check_turtle.penup()
    check_turtle.hideturtle()
    screen.addshape("checkbutton.gif")
    check_turtle.shape("checkbutton.gif")
    check_turtle.goto(180,-300)
    check_turtle.showturtle()
    #check_turtle.onclick(handle_check)

    x_turtle.penup()
    x_turtle.hideturtle()
    screen.addshape("xbutton.gif")
    x_turtle.shape("xbutton.gif")
    x_turtle.goto(260,-300)
    x_turtle.showturtle()
    #x_turtle.onclick(handle_clear)

    quit_turtle.penup()
    quit_turtle.hideturtle()
    screen.addshape("quit_button.gif")
    quit_turtle.shape("quit_button.gif")
    quit_turtle.goto(340,-300)
    quit_turtle.showturtle()
    #quit_turtle.onclick(handle_quit)

    screen.onclick(None)
    screen.onscreenclick(click)
    screen.update()
    screen.mainloop()

if __name__ == "__main__":
    main()