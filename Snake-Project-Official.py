import turtle
import random #**for food

class Snake:
    #The snake moves by jumping one square at a time.
    def __init__(self, home, size):
        #home is the starting location (by default is 0, 0)
        #size is the size of the square in each cell of the snake
        #The snake location is stored as a list of tuples, where each tuple
        #is the position of a segment of the snake
        self.snake_location = [home]
        self.home = home
        self.size = size
        self.num_moves = 0
        
        for i in range(1,2): # makes the snake longer in the start
            self.snake_location.append((self.home[0] + self.size * i, self.home[1]))
        
    def draw_segment(self, point):
        #Draws a square equal to the size of the snake, where the location
        #given is the bottom left corner of the square
        #point is a tuple with (x,y) coordinates.
        turtle.goto(point)
        turtle.begin_fill()
        turtle.pendown()
        for i in range(4):
            turtle.forward(self.size)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()

    
    def draw(self):
        #Draws each of the segments, and then draws the head with red colour
        turtle.color("red")
        self.draw_segment(self.snake_location[0])
        turtle.color("black")
        for segment in (self.snake_location[1:]):
            self.draw_segment(segment)
            
    def move(self, direction, location_tuple):
        #move the snake in the direction given by adding a new
        #head position to the list of locations, and removing
        #the end of the snake.  The snake grows automatically every 10
        #moves.  That is, every 10 moves, the tail of the snake is not
        #removed.
        #for cutting the tail and not cutting the tail
        new_headX = self.snake_location[0][0]
        new_headY = self.snake_location[0][1]
        if direction == "left":
            new_headX -= self.size

        if direction == "right":
            new_headX += self.size

        if direction == "up":
            new_headY += self.size

        if direction == "down":
            new_headY -= self.size

        self.snake_location = [(new_headX, new_headY)] + self.snake_location

##                   ## Makes the Snake Grow Automatically ##
##        self.num_moves += 1
##        if self.num_moves % 10 != 0: #multiples of 10
##            self.snake_location.pop(-1)
##
        if not self.hit_target(location_tuple):
            self.snake_location.pop()

    def enemy_move(self, target_location):
        target_locationX = target_location[0]
        target_locationY = target_location[1]
        
        snakehead_locationX = self.snake_location[0][0]
        snakehead_locationY = self.snake_location[0][1]
        
        if snakehead_locationX < target_locationX:
            self.move('right', target_location)
            return
        if snakehead_locationY < target_locationY:
            self.move('up', target_location)
            return
        if snakehead_locationY > target_locationY:
            self.move('down', target_location)
            return
        if snakehead_locationX > target_locationX:
            self.move('left', target_location)
            return
    
    def hit_self(self):
        #check if the head of the snake has hit one of its own segments
        #try check locations except head, if equal to other locations return == True
        for segment in self.snake_location[1:]:
            if segment == self.snake_location[0]:
                return True

        return False
            

    def hit_bounds(self, bounds): #left, top, right, bottom bounding box
        #check if the snake has hit the bounds given
        head = self.snake_location[0]
        if head[0] <= bounds["left"] * self.size or head[0] > bounds["right"] * self.size:
            return True

        if head[1] < bounds["bottom"]* self.size:
            return True

        if head[1] >= bounds["top"]* self.size:
            return True
        
    def hit_target(self, location_tuple):
        
        if self.snake_location[0] == location_tuple:
            return True
        else:
            return False
        
    def hit_enemy(self, enemy_location):
        if self.snake_location[0] in enemy_location:
            return True
        else:
            return False

class Target:
    def __init__(self, bound, size, snake):
        self.left_bound = -300
        self.right_bound = 280
        self.up_bound = 280
        self.down_bound = -300
        self.size = size
        self.snake = snake
        self.location_tuple = self.random_location()

    def random_location(self):
        self.random_X = random.randrange(self.left_bound + self.size, self.right_bound, self.size)
        self.random_Y = random.randrange(self.down_bound, self.up_bound, self.size)
        return(self.random_X, self.random_Y)
        
    def draw_target(self):
        turtle.goto(self.location_tuple)
        turtle.begin_fill()
        turtle.pendown()
        for i in range(4):
            turtle.forward(self.size)
            turtle.left(90)
        turtle.fillcolor("blue")
        turtle.end_fill()
        turtle.penup()



class SnakeGame:
    def __init__(self):
        #set up the window for the game, the methods that are called when keys are pressed, and
        #the method that is called each new game turn
        self.framework = GameFramework(800, 800, 'COMPSCI Python Project')
        self.framework.add_key_action(self.move_right, 'Right')
        self.framework.add_key_action(self.move_up, 'Up')
        self.framework.add_key_action(self.move_down, 'Down')
        self.framework.add_key_action(self.move_left, 'Left')
        self.framework.add_key_action(self.setup_game, ' ') #Pressing space will restart the game
        self.framework.add_tick_action(self.next_turn, 100) #Delay (speed) is 100.  Smaller is faster.

    #set of methods to keep track of which key was most recently pressed
    def move_right(self):
        self.last_key = 'Right'

    def move_left(self):
        self.last_key = 'Left'

    def move_down(self):
        self.last_key = 'Down'

    def move_up(self):
        self.last_key = 'Up'
        
    def setup_game(self):
        #initializes starting variables and begins the animation loop
        self.last_key = 'None' #No initial direction specified
        self.snake_size = 20
        self.boundary_limit = {'left':-15, 'right':15, 'top':15, 'bottom':-15}
        snake_home = (0,0)
        self.snake = Snake(snake_home, self.snake_size)
        self.target = Target(self.boundary_limit, self.snake_size, self.snake)
        self.enemy_snake = Snake(self.target.random_location(), self.snake_size)
        self.framework.start_game()
    
    def draw_bounds(self):
        #draws the box that defines the limit for the snake
        left = self.boundary_limit['left']
        top = self.boundary_limit['top']
        size = self.snake_size
        turtle.goto(left * size, top * size)
        turtle.pendown()
        for i in range(0, 4): #Draw a bounding square
            turtle.rt(90)
            turtle.forward(abs(left) * size * 2)
        turtle.penup()

    def next_turn(self):
        #called each time the game 'ticks'
        turtle.clear()
        snake = self.snake
        enemy_snake = self.enemy_snake
        self.target.draw_target()
        if self.last_key == 'Right':
            snake.move('right', self.target.location_tuple)
        if self.last_key == 'Up':
            snake.move('up', self.target.location_tuple)
        if self.last_key == 'Down':
            snake.move('down', self.target.location_tuple)
        if self.last_key == 'Left':
            snake.move('left', self.target.location_tuple)
        self.draw_bounds()
        snake.draw()
        enemy_snake.enemy_move(self.target.location_tuple)
        enemy_snake.draw()
        if snake.hit_self() or snake.hit_bounds(self.boundary_limit) or snake.hit_enemy(enemy_snake.snake_location) or enemy_snake.hit_enemy(snake.snake_location):
            self.framework.stop_game() #game over
            
        if snake.hit_target(self.target.location_tuple) or enemy_snake.hit_target(self.target.location_tuple):
            self.target = Target(self.boundary_limit, self.snake_size, self.snake)
                    
    def start(self):
        #starts the game
        self.setup_game() #set up the game.
        turtle.mainloop() #must appear last.


#Shouldn't need to edit this at all
class GameFramework:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.game_running = False
        self.tick = None #function to call for each animation cycle
        
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.hideturtle() #prevent turtle appearance
        turtle.tracer(False) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything

    def start_game(self):
        self.game_running = True
        self.__animation_loop()
         
    def stop_game(self):
        self.game_running = False

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func, delay):
        self.tick = func
        self.delay = delay

    def __animation_loop(self):
        if self.game_running:
            self.tick()
            turtle.ontimer(self.__animation_loop, self.delay)
   
g = SnakeGame()
g.start()