### for the file stuff on visual studio
import sys, os
print(os.listdir())

import sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *




# six is the special number or the power number its red btw

levels = (
(1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,6,1,1,1,1,1,1,6,1,1, 
 1,1,1,6,1,1,1,1,6,1,1,1, 
 1,1,1,1,6,1,1,6,1,1,1,1, 
 1,1,1,1,1,6,6,1,1,1,1,1, 
 1,1,1,1,1,6,6,1,1,1,1,1, 
 1,1,1,1,6,1,1,6,1,1,1,1, 
 1,1,1,6,1,1,1,1,6,1,1,1, 
 1,1,6,1,1,1,1,1,1,6,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1),

(2,2,2,2,2,2,2,2,2,2,2,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,2,2,2,2,2,2,2,2,2,2,2),

(3,3,3,3,3,3,3,3,3,3,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,3,3,3,3,3,3,3,3,3,3, 
 3,3,3,3,3,3,3,3,3,3,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,3,3,3,3,3,3,3,3,3,3),
)
    
#this function increments the level
def goto_next_level():
    global level, levels
    level += 1
    if level > len(levels)-1: level = 0
    load_level()

#this function updates the blocks in play
def update_blocks():
    global block_group, waiting
    if len(block_group) == 0: #all blocks gone?
        goto_next_level()
        waiting = True
    block_group.update(ticks, 50)
    special_block_group.update(ticks, 50)
        
#this function sets up the blocks for the level
def load_level():
    global level, block, block_image, block_group, levels, special_block_group
    
    block_image = pygame.image.load("blocks.png").convert_alpha()

    block_group.empty() #reset block group
    special_block_group.empty() #reset block group

    
    for bx in range(0, 12):
        for by in range(0,10):
            block = MySprite()
            block.set_image(block_image, 58, 28, 4)
            x = 40 + bx * (block.frame_width+1)
            y = 250 + by * (block.frame_height+1)
            block.position = x,y

            #read blocks from level data
            num = levels[level][by*12+bx]
            block.first_frame = num-1
            block.last_frame = num-1

            if num > 4: # for the special blocks 
                special_block_group.add(block)

            elif num > 0: #0 is blank
                block_group.add(block)

            
        




class paddle_and_balls():
    def __init__(self,x,y,side):

    #create the paddle sprite
        self.paddle = MySprite()
        self.paddle.load("paddle.png")
        self.paddle.position = x, y
        paddle_group.add(self.paddle)

        #create ball sprite
        self.ball = MySprite()
        self.ball.load("ball.png")
        self.ball.position = x,y
        ball_group.add(self.ball)

        # which paddle it is on the top or the one down one 
        self.location = side

        # this the scoreing stuff for each of the player
        self.waiting = True
        self.score = 0
        self.lives = 3
        self.player_active = True


    #this function resets the ball's velocity
    def reset_ball(self):
        self.ball.velocity = Point(-4.5, +7.0)


    #this function moves the paddle
    def move_paddle(self,right,left,space):
        global movex,movey,keys,waiting

        paddle_group.update(ticks, 60)


        if right == True : self.paddle.velocity.x = -6
        elif left == True : self.paddle.velocity.x = 6
        else:
            if movex < -2: self.paddle.velocity.x = movex
            elif movex > 2: self.paddle.velocity.x = movex
            else: self.paddle.velocity.x = 0
        
        self.paddle.X += self.paddle.velocity.x
        if self.paddle.X < 0: self.paddle.X = 0
        elif self.paddle.X > 710: self.paddle.X = 710

    




    #this function moves the ball
    def move_ball(self):
        global waiting, ball, game_over, lives

        #move the ball            
        ball_group.update(ticks, 50)
        if self.waiting:
            # if its the paddle on the bottom
            if self.location == 'down':
                self.ball.X = self.paddle.X + 40
                self.ball.Y = self.paddle.Y - 20
            # if its the paddle on the top
            elif self.location == 'top':
                self.ball.X = self.paddle.X + 40
                self.ball.Y = self.paddle.Y + 40
            else:
                print('error in recongsing where the ball should be put of the paddle')
                
        self.ball.X += self.ball.velocity.x
        self.ball.Y += self.ball.velocity.y

        # if its the paddle on the bottom
        if self.location == 'down':
                
            if self.ball.X < 0:
                self.ball.X = 0
                self.ball.velocity.x *= -1
            elif self.ball.X > 780:
                self.ball.X = 780
                self.ball.velocity.x *= -1
            if self.ball.Y < 0:
                self.ball.Y = 0
                self.ball.velocity.y *= -1
            elif self.ball.Y > 750: #missed paddle
                self.waiting = True
                self.lives -= 1
                if self.lives < 1: self.player_active = False
        
        # if its the paddle on the top
        elif self.location == 'top':
                
            if self.ball.X < 0:
                self.ball.X = 0
                self.ball.velocity.x *= -1
            elif self.ball.X > 780:
                self.ball.X = 780
                self.ball.velocity.x *= -1
            if self.ball.Y > 750:
                self.ball.Y = 749
                self.ball.velocity.y *= -1
            elif self.ball.Y < 0 : #missed paddle
                self.waiting = True
                self.lives -= 1
                if self.lives < 1: self.player_active = False

    #this function test for collision between ball and paddle
    def collision_ball_paddle(self):
        if pygame.sprite.collide_rect(self.ball, self.paddle):

            # if its the paddle on the bottom
            if self.location == 'down':
                self.ball.velocity.y = -abs(self.ball.velocity.y)
                bx = self.ball.X + 8
                by = self.ball.Y + 8
                px = self.paddle.X + self.paddle.frame_width/2
                py = self.paddle.Y + self.paddle.frame_height/2
                if bx < px: #left side of paddle?
                    self.ball.velocity.x = -abs(self.ball.velocity.x)
                else: #right side of paddle?
                    self.ball.velocity.x = abs(self.ball.velocity.x)

            # if its the paddle on the top
            elif self.location == 'top':
                self.ball.velocity.y = +abs(self.ball.velocity.y)
                bx = self.ball.X + 8
                by = self.ball.Y + 8
                px = self.paddle.X + self.paddle.frame_width/2
                py = self.paddle.Y + self.paddle.frame_height/2
                if bx < px: #left side of paddle?
                    self.ball.velocity.x = -abs(self.ball.velocity.x)
                else: #right side of paddle?
                    self.ball.velocity.x = abs(self.ball.velocity.x)



    #this function tests for collision between ball and blocks  # normal blocks 
    def collision_ball_blocks(self):
        global score, block_group, ball


        hit_block = pygame.sprite.spritecollideany(self.ball, block_group)
        if hit_block != None:
            self.score += 50
            block_group.remove(hit_block)
            bx = self.ball.X + 8
            by = self.ball.Y + 8

            #hit middle of block from above or below?
            if bx > hit_block.X+5 and bx < hit_block.X + hit_block.frame_width-5:
                if by < hit_block.Y + hit_block.frame_height/2: #above?
                    self.ball.velocity.y = -abs(self.ball.velocity.y)
                else: #below?
                    self.ball.velocity.y = abs(self.ball.velocity.y)

            #hit left side of block?
            elif bx < hit_block.X + 5:
                self.ball.velocity.x = -abs(self.ball.velocity.x)
            #hit right side of block?
            elif bx > hit_block.X + hit_block.frame_width - 5:
                self.ball.velocity.x = abs(self.ball.velocity.x)

            #handle any other situation
            else:
                self.ball.velocity.y *= -1

    
     #this function tests for collision between ball and blocks  # special blocks 
    def collision_ball_blocks_special(self):
        global score, special_block_group, ball


        hit_block = pygame.sprite.spritecollideany(self.ball, special_block_group)
        if hit_block != None:
            self.score += 100
            special_block_group.remove(hit_block)
            bx = self.ball.X + 8
            by = self.ball.Y + 8

            #hit middle of block from above or below?
            if bx > hit_block.X+5 and bx < hit_block.X + hit_block.frame_width-5:
                if by < hit_block.Y + hit_block.frame_height/2: #above?
                    self.ball.velocity.y = -abs(self.ball.velocity.y)
                else: #below?
                    self.ball.velocity.y = abs(self.ball.velocity.y)

            #hit left side of block?
            elif bx < hit_block.X + 5:
                self.ball.velocity.x = -abs(self.ball.velocity.x)
            #hit right side of block?
            elif bx > hit_block.X + hit_block.frame_width - 5:
                self.ball.velocity.x = abs(self.ball.velocity.x)

            #handle any other situation
            else:
                self.ball.velocity.y *= -1

    # this will end up deleting the paddle and the ball of a certain player
    def exterminate(self):
        
        print ("deleted")


   


#this function initializes the game
def game_init():
    global screen, font, timer
    global paddle_group, block_group, ball_group, special_block_group
    global paddle, block_image, block, ball

    pygame.init()
    screen = pygame.display.set_mode((1100,800))
    pygame.display.set_caption("Block Breaker Game")
    font = pygame.font.Font(None, 36)
    pygame.mouse.set_visible(False)
    timer = pygame.time.Clock()

    #create sprite groups
    paddle_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()
    special_block_group = pygame.sprite.Group()





    
#main program begins
game_init()
game_over = False
level = 0
load_level()


# this is when the right button or the left button are being actiavted
right_side_1 = False
left_side_1 = False
right_side_2 = False
left_side_2 = False

# these are the paddle and balls being places
# place inputs below will be the x value and the y value of the slider thign and the thrid value is where it is gonna be on the screen 
player_1 = paddle_and_balls(450,750,'down')
player_2 = paddle_and_balls(450,50,'top')


time.sleep(1) # this been places to stop a certain error




#repeating loop
while True:


    timer.tick(30)
    ticks = pygame.time.get_ticks()



    #handle events
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()


    #handle key presses
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()



    # player one controls
    try:
        if keys[K_RIGHT] :
            right_side_1 = True
        elif keys[K_LEFT] :
            left_side_1 = True
        elif keys[K_m] :
            if player_1.waiting:
                player_1.waiting = False
                player_1.reset_ball()
        elif event.type == KEYUP:
            if event.key == K_RETURN: goto_next_level()
    except:
        pass

    # player two controls
    try:    
        if keys[K_a] :
            right_side_2 = True
        elif keys[K_d] :
            left_side_2 = True
        elif keys[K_x] :
            if player_2.waiting:
                player_2.waiting = False
                player_2.reset_ball()
        elif event.type == KEYUP:
            if event.key == K_RETURN: goto_next_level()
    except:
        pass
    
    # the reason why those try and expect loops are above is because if one player died and they tried click the buttons no errors will come on screen 
    


    # if a single player is deactiavted then we need to make sure they are canclled

    if player_1.player_active == False:
        player_1.exterminate
    if player_2.player_active == False:
        player_2.exterminate
    

    # if both players are dead at the game then its game over 

    if player_1.player_active == False and player_2.player_active == False:
        game_over = True



    #do updates
    if not game_over:

        update_blocks()

        # player one functions 

        # this is player ones controls being inputed in fucntion 
        if player_1.player_active == True:  # seees if that player is active to use

            if right_side_1 == True :
                player_1.move_paddle(right=True,left=False,space=False)
                right_side_1 = False

            if left_side_1 == True :
                player_1.move_paddle(right=False,left=True,space=False)
                left_side_1 = False

            player_1.move_ball()
            player_1.collision_ball_paddle()
            player_1.collision_ball_blocks_special()
            player_1.collision_ball_blocks()

     
        # player two functions 
        
        # this is player ones controls being inputed in fucntion 
        if player_2.player_active == True:  # seees if that player is active to use

            if right_side_2 == True :
                player_2.move_paddle(right=True,left=False,space=False)
                right_side_2 = False

            if left_side_2 == True :
                player_2.move_paddle(right=False,left=True,space=False)
                left_side_2 = False
            
            player_2.move_ball()
            player_2.collision_ball_paddle()
            player_2.collision_ball_blocks_special()
            player_2.collision_ball_blocks()
           
    



        #do drawing
        paddle_group.update(time.time()) # i still dont know why i added this but its works with it
        screen.fill((50,50,100))
        special_block_group.draw(screen)
        block_group.draw(screen)
        ball_group.draw(screen)
        paddle_group.draw(screen)


    print_text(font, 805, 0, "Player One " + str(player_1.score))
    print_text(font, 805, 20, "Player Two " + str(player_2.score))
    print_text(font, 805, 40, "Blocks Remaning " + str(len(block_group)))
    print_text(font, 805,60, " Levels "  + str(level))
    
   
    if game_over:
        print_text(font, 300, 380, "G A M E   O V E R")
    pygame.display.update()
    

### find a way to display the scores for both players

### power ups 
### keybaord 
### sound 
### image 
### if u hit certain blocks the paddle either becomes smaller or larger 
