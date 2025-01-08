import tkinter
import random

ROWS = 25 
COLUMNS = 25
TILESIZE = 25

#game window 
WINDOW_WIDTH = COLUMNS * TILESIZE
WINDOW_HEIGHT = ROWS * TILESIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

window = tkinter.Tk()
window.title("snake")
window.resizable(False, False)


canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, highlightthickness=0)
canvas.pack()
window.update()

#center window 
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

windowX = int((screen_width/2) - (window_width/2))
windowY = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{windowX}+{windowY}")

#initialise game
snake = Tile(5 * TILESIZE, 5 * TILESIZE)             #single tile is snakes head 
food = Tile(10 * TILESIZE, 10 * TILESIZE)            
velocityX = 0
velocityY = 0
snake_body = []                                       #multiple tile objects 
game_over = False 
score = 0

def change_direction(e):                             #e = event 
    global velocityX, velocityY, game_over

    if(game_over):
        return

    if(e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1

    elif(e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif(e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif(e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, game_over, food, snake_body, score

    if(game_over):
        return

    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collission 
    if(snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLUMNS - 1) * TILESIZE   #i might be wrong on columns 
        food.y = random.randint(0, ROWS - 1) * TILESIZE   #i might be wrong on columns 
        score += 1

    #update body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if(i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILESIZE
    snake.y += velocityY * TILESIZE



def draw():
    global snake

    #move
    move()

    canvas.delete("all")

    #draw food 
    canvas.create_rectangle(food.x, food.y, food.x + TILESIZE, food.y + TILESIZE, fill="red")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILESIZE, snake.y + TILESIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILESIZE, tile.y + TILESIZE, fill="lime green")

    window.after(100, draw)  #refreshes every 100ms 

    if(game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")


draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
