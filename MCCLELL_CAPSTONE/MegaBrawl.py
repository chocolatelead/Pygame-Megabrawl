#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      2202075
#
# Created:     06/06/2016
# Copyright:   (c) 2202075 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pygame,sys,time
from pygame.locals import *


ScreenW = 800
ScreenH = 600

black = (0,0,0)
white = (255,255,255)
nblue = (0,0,128)
red = (255,0,0)
orange = (255,165,0)


#http://programarcadegames.com/index.php?&chapter=example_code_platformer
#this website is very helpful, its in depth videos were easy to understand and
#were a good place to look when you are frustrated and need guidance


class SpriteSheet(object):#class to upload an image, then take out a smaller piece of the image
    def __init__(self,file):
        self.sprite_sheet = pygame.image.load(file).convert()#loads file

    def Pic_Loc(self,x,y,w,h):
        image = pygame.Surface([w,h]).convert()#creates new blank photo
        image.blit(self.sprite_sheet,(0,0),(x,y,w,h))#prints image onto photo
        image.set_colorkey(white)#The backgound color is white
        return image

class PlasmaBlast(pygame.sprite.Sprite):# class to create the bullets that the user shoots
    def __init__(self,facing,size,damage,color):
        super().__init__()
        self.facing = facing
        self.damage = damage
        self.color = color
        self.image = pygame.Surface([size,size])#create block
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update(self):
        if self.facing == "r":#moves right
            self.rect.x +=10
        if self.facing == "l":#moves left
            self.rect.x -= 10


class Player(pygame.sprite.Sprite):#class to create player

    def __init__(self,file,start_face):

        super().__init__()


        self.jumping = False   #variables for player, so that player1 and player2 have the same variables, but have different values
        self.shooting = False
        self.falling = False
        self.walk_r = []
        self.walk_l = []
        self.stand = []
        self.shoot_r = []
        self.shoot_l = []
        self.jump_r = []
        self.jump_l = []
        self.facing = ""
        self.health = 100
        self.start_face = start_face
        self.stop = True
        self.level = None
        self.dX = 0
        self.dY = 0
        self.frame_counter = 0


        #import all of the images from sprite sheets
        sprite_sheet = SpriteSheet(file)
        image = sprite_sheet.Pic_Loc(212,0,38,46)#x,y,w,h

        #walking sprites
        #right
        self.stand.append(image)
        image = sprite_sheet.Pic_Loc(160,0,44,46)
        self.walk_l.append(image)
        image = sprite_sheet.Pic_Loc(124,0,28,46)
        self.walk_l.append(image)
        image = sprite_sheet.Pic_Loc(76,0,41,46)
        self.walk_l.append(image)
        #left
        image = sprite_sheet.Pic_Loc(212,0,38,46)#x,y,w,h
        image = pygame.transform.flip(image,True,False)#image,xbool,ybool
        self.stand.append(image)
        image = sprite_sheet.Pic_Loc(160,0,44,46)
        image = pygame.transform.flip(image,True,False)
        self.walk_r.append(image)
        image = sprite_sheet.Pic_Loc(124,0,28,46)
        image = pygame.transform.flip(image,True,False)
        self.walk_r.append(image)
        image = sprite_sheet.Pic_Loc(76,0,41,46)
        image = pygame.transform.flip(image,True,False)
        self.walk_r.append(image)


        #shooting sprites
        #right
        image = sprite_sheet.Pic_Loc(0,116,58,46)#x,y,w,h
        self.shoot_l.append(image)#adds to list
        image = sprite_sheet.Pic_Loc(67,116,48,46)
        self.shoot_l.append(image)
        image = sprite_sheet.Pic_Loc(125,116,58,46)
        self.shoot_l.append(image)
        image = sprite_sheet.Pic_Loc(190,116,58,46)
        self.stand.append(image)
        #left
        image = sprite_sheet.Pic_Loc(0,116,58,46)#x,y,w,h
        image = pygame.transform.flip(image,True,False)
        self.shoot_r.append(image)
        image = sprite_sheet.Pic_Loc(67,116,48,46)
        image = pygame.transform.flip(image,True,False)
        self.shoot_r.append(image)
        image = sprite_sheet.Pic_Loc(125,116,58,46)
        image = pygame.transform.flip(image,True,False)
        self.shoot_r.append(image)
        image = sprite_sheet.Pic_Loc(190,116,58,46)
        image = pygame.transform.flip(image,True,False)
        self.stand.append(image)

        #jumping sprites
        #right
        image = sprite_sheet.Pic_Loc(79,55,58,60)#x,y,w,h
        self.jump_l.append(image)
        image = sprite_sheet.Pic_Loc(140,55,58,60)
        self.jump_l.append(image)
        image = sprite_sheet.Pic_Loc(200,55,58,60)
        self.jump_l.append(image)
        #left
        image = sprite_sheet.Pic_Loc(79,55,58,60)#x,y,w,h
        image = pygame.transform.flip(image,True,False)
        self.jump_r.append(image)
        image = sprite_sheet.Pic_Loc(140,55,58,60)
        image = pygame.transform.flip(image,True,False)
        self.jump_r.append(image)
        image = sprite_sheet.Pic_Loc(200,55,58,60)
        image = pygame.transform.flip(image,True,False)
        self.jump_r.append(image)







        #image = sprite_sheet.Pic_Loc()
        if self.start_face == 'r':
            self.image = self.stand[0]
        elif self.start_face == 'l':
            self.image = self.stand[1]

        self.rect = self.image.get_rect()








    def update(self):
        self.calc_grav()#calls function that makes user go down

        if self.dY > 1:  #if user is moving down due to the gavity function, he is considered falling
            self.falling = True
        self.rect.x += self.dX
        pos = self.rect.x #moves character in the x direction

        if self.stop == True:#Sprite images for when player isnt moving left or right

            if self.facing == 'r':#if player is facing r and not moving left or right
                if self.jumping == False and self.falling == False and self.shooting == False:#if player is standing still
                    self.image = self.stand[1]
                elif self.shooting == True and (self.jumping == True or self.falling == True):#if player is shooting and is either falling or jumping
                    self.image = self.jump_r[0]

                elif self.jumping == True:#if player is jumping
                    self.image = self.jump_r[1]
                elif self.falling == True:#if player is falling
                    self.image = self.jump_r[2]
                elif self.shooting == True: #if player is shooting and on ground
                    self.image = self.stand[3]

            elif self.facing == 'l':
                if self.jumping == False and self.falling == False and self.shooting == False:
                    self.image = self.stand[0]
                elif self.shooting == True and (self.jumping == True or self.falling == True):
                    self.image = self.jump_l[0]
                elif self.jumping == True:
                    self.image = self.jump_l[1]
                elif self.falling == True:
                    self.image = self.jump_l[2]
                elif self.shooting == True:
                    self.image = self.stand[2]


        elif self.stop == False:#sprite images for when player is moving left or right
            if self.facing == "r":
                if self.shooting == True and (self.jumping == True or self.falling == True):
                    self.image = self.jump_r[0]
                elif self.shooting == True:
                    frame = (pos // 30) % len(self.shoot_r)
                    self.image = self.shoot_r[frame]
                elif self.jumping == True:
                    self.image = self.jump_r[1]
                elif self.falling == True:
                    self.image = self.jump_r[2]
                else:
                    frame = (pos // 30) % len(self.walk_r)
                    self.image = self.walk_r[frame]
            elif self.facing == 'l':
                if self.shooting == True and (self.jumping == True or self.falling == True):
                    self.image = self.jump_l[0]
                elif self.shooting == True:
                    frame = (pos // 30) % len(self.shoot_l)
                    self.image = self.shoot_l[frame]
                elif self.jumping == True:
                    self.image = self.jump_l[1]
                elif self.falling == True:
                    self.image = self.jump_l[2]
                else:
                    frame = (pos // 30) % len(self.walk_l)
                    self.image = self.walk_l[frame]

        block_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for block in block_hit_list:#if player hits block, make edge of block equal edge of character
            if self.dX>0:
                self.rect.right = block.rect.left
            elif self.dX<0:
                self.rect.left = block.rect.right

        self.rect.y += self.dY#moves character in y direction

        block_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for block in block_hit_list:#if player hits block, make edge of block equal edge of character
            if self.dY>=0:
                self.jumping = False
                self.falling = False
                self.rect.bottom = block.rect.top
            elif self.dY<0:
                self.jumping = False
                self.falling = True #if player hits head on block, use falling sprite
                self.rect.top = block.rect.bottom
            self.dY = 0

    def jump(self):
        self.jumping = True
        self.rect.y += 2 #moves down to check if there is a block under
        jump_block_hit_list = pygame.sprite.spritecollide(self,self.level.wall_list, False)
        self.rect.y -=2
        #if he is on a platform and higher than bottom of screen, he can jump
        if len(jump_block_hit_list) > 0 or self.rect.bottom >= ScreenH:
            self.dY = -10

    def calc_grav(self):#moves character down
        if self.dY == 0:# if user is not moving, move down
            self.dY = 1
        else:
            self.dY+= .35 #moves player down more if in air

        if self.rect.y > ScreenH - self.rect.h and self.dY >=0: #if player hits bottom opening, appear at top
            self.rect.y = 0
    def shoot(self):
        self.shooting = True
    def stop_shoot(self):
        self.shooting = False

    def right(self):#moves right
        self.dX = 6
        self.facing = "r"
        self.stop = False #bool for when character is moving
    def left(self):#moves left
        self.dX = -6
        self.facing = "l"
        self.stop = False

    def stopped(self):
        self.dX = 0 #makes player unable to move in x direction
        self.stop = True #bool for showing player is stoppped



class Wall(pygame.sprite.Sprite):#class to create walls
    def __init__(self, w, h):

        super().__init__()

        self.image = pygame.Surface([w,h])
        self.image.fill(white)

        self.rect = self.image.get_rect()
class Level(object):#class to create level
    def __init__(self,player1,player2):
        self.wall_list = pygame.sprite.Group()#create sprite lists so we can later compare two sprite groups colliding
        self.bullet_list = pygame.sprite.Group()
        self.player1 = player1
        self.player2 = player2
        self.background = pygame.image.load('bg.png')
    def update(self):#updates locations of sprites
        self.wall_list.update()
        self.bullet_list.update()
    def draw(self,screen):#draws screen
        screen.fill(nblue)
        screen.blit(self.background, (0,0))
        self.wall_list.draw(screen)
        self.bullet_list.draw(screen)
class Level1(Level):#this creates a specific level, we can create more
    def __init__(self,player1,player2):
        Level.__init__(self,player1,player2)
        walls = [[300,20,0,0],#w,h,x,y values of each wall
                 [300,20,0,580],
                 [300,20,500,0],
                 [300,20,500,580],
                 [20,ScreenH,0,0],
                 [20,ScreenH,780,0],
                 [280,20,20,375],
                 [280,20,500,375],
                 [300,20,250,475],
                 [100,20,120,250],
                 [100,20,580,250],
                 [400,20,200,150],
                 ]
        #adds each wall to a list
        for i in walls:
            wall = Wall(i[0],i[1])#calls wall function to create a wall with width and height
            wall.rect.x = i[2]#x value
            wall.rect.y = i[3]#y value
           # wall.player1 = self.player1
            #wall.player2 = self.player2
            self.wall_list.add(wall) #adds wall to sprite group



def game():
    pygame.init()
    #create screen
    screenSize = [ScreenW,ScreenH]
    screen = pygame.display.set_mode(screenSize)
    color =(0,255,255)
    screen.fill(color)
    font_name = pygame.font.SysFont('sans', 16)
    name_color = (169,169,169)
    pygame.display.set_caption("MegaBrawl")
    font1 = pygame.font.SysFont('sans', 32)
    textcolor =(0,153,153)
    #function to print text on screen
    def text(text, font, screen, x, y):
        textobj = font.render(text, 1, textcolor)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)#position of top left corner
        screen.blit(textobj, textrect)#draws sentence
    #function to print semi transparent text on screen
    def trans_text(text, font, screen, x, y):
        textobj = font.render(text, 1, textcolor)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)#position of top left
        textobj.set_alpha(128)#makes object seethrough
        screen.blit(textobj, textrect)#draws sentence

    #import helmets for health
    h1 = pygame.image.load('h1.png').convert()#convert makes the background transparent
    h1.set_colorkey(white)                    #set_colorkey(white) assumes the background that it is to erase is the color white
    h2 = pygame.image.load('h2.png').convert()
    h2.set_colorkey(white)
    transform1 = pygame.transform.scale(h1, (30,30))
    h1Rect = pygame.Rect(100,30,30,30)
    transform2 = pygame.transform.scale(h2, (30,30))
    h2Rect = pygame.Rect(600,30,30,30)
    #sounds
    shot = pygame.mixer.Sound('shoot.wav')
    die = pygame.mixer.Sound('death.wav')
    hit = pygame.mixer.Sound('hit.wav')
    pygame.mixer.music.load('music.mp3')

    #set up level
    player1 = Player("p1.3.png",'r')#sets up players with individual sprite sheets and starting positions
    player2 = Player("p2.3.png",'l')
    level_list = []
    level_list.append(Level1(player1,player2))
    level_used = level_list[0]
    player1.level = level_used#level used is the level being used
    player2.level = level_used
    player1.rect.x = 200 #starting x position
    player2.rect.x = 600
    player1.rect.y = ScreenH - player1.rect.h#starting y position
    player2.rect.y = ScreenH - player2.rect.h
    player1.facing = 'r'#which direction the player faces when they spawn
    player2.facing = 'l'
    size_counter = 30
    size_counter2 = 30
    win1 =False #anything with 1 relates to player 1
    win2 = False #anything with 2 relates to player 2
    draw = False
    damage = 0
    sprites = pygame.sprite.Group()
    sprites.add(player1)#adds the players to a sprite group so we can check collisions with other sprite groups
    sprites.add(player2)
    x = False#used for holding down shoot
    y = False
    run = True
    clock = pygame.time.Clock()


    #pause function
    def waitForPlayerToPressKey():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    return
    font3 = pygame.font.SysFont('arial',16)
    #Start Screen
    text('Welcome to MegaBrawl!', font1, screen, 200, 50)
    text('You should use your left hand to control your character', font3, screen, 175, 125)
    text('As player 1 you use a and d to move sidweways,', font3, screen, 175, 150)
    text('use w to jump, and spacebar to shoot your blaster', font3, screen, 175, 175)
    text('As player 2 you use 4 and 6 on the numpad to move sideways,', font3, screen, 175, 200)
    text('use 8 to jump, and enter to shoot your blaster', font3, screen, 175, 225)
    text('Your goal is to deplete your opponents health by hitting him', font3, screen, 175, 250)
    text('with your plasma balls that are launched from your hand cannon!', font3, screen, 175, 275)
    text('Hold down the shoot button to do more damage!', font3, screen, 175, 300)
    text('The game will end once a player loses all his health, or the time runs out.', font3, screen, 175, 325)
    text('Have fun, and good luck!', font3, screen, 175, 350)

    pygame.display.update()
    waitForPlayerToPressKey()
    #screen to obtain player 1's username
    color1 = (0,255,255)
    font2 = pygame.font.SysFont("arial",72)
    textcolor =(0,153,153)
    screen.fill(color1)
    p1_name = ""
    x = True
    while x is True:#getting key presses for username
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.unicode.isalpha():
                    p1_name += event.unicode#if key is alphabetical, add it to name
                elif event.key == K_BACKSPACE:
                    p1_name = p1_name[:-1]#removes 1 character from list
                elif event.key == K_RETURN:
                    x = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        if len(p1_name) >4:
            p1_name = p1_name[:-1]
        clock.tick(60)
        #draws the end screen
        text(("Username: %s"%(p1_name)),font2,screen,150,500)
        text(("Player 1, please"),font2,screen,150,50)
        text(("enter your username!"),font2,screen,175,125)
        text(("It can only be 4"),font2,screen,175,200)
        text(("letters long."),font2,screen,175,275)
        text(("Then press enter"),font2,screen,175,350)
        pygame.display.update()
        screen.fill(color1)


    #screen for obtaining player2's username
    pygame.display.update()
    color1 = (255,128,0)
    font2 = pygame.font.SysFont("arial",72)
    textcolor =(153,0,0)
    screen.fill(color1)
    p2_name = ""
    x = True
    while x is True:#getting key presses for username
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.unicode.isalpha():
                    p2_name += event.unicode
                elif event.key == K_BACKSPACE:
                    p2_name = p2_name[:-1]
                elif event.key == K_RETURN:
                    x = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        if len(p2_name) >4:
            p2_name = p2_name[:-1]
        clock.tick(60)
        #draws the end screen
        text(("Username: %s"%(p2_name)),font2,screen,150,500)
        text(("Player 2, please"),font2,screen,150,50)
        text(("enter your username!"),font2,screen,175,125)
        text(("It can only be 4"),font2,screen,175,200)
        text(("letters long."),font2,screen,175,275)
        text(("Then press enter"),font2,screen,175,350)

        pygame.display.update()
        screen.fill(color1)

    color1 = (128,128,128)
    font1 = pygame.font.SysFont("arial",96)
    textcolor =(64,64,64)
    screen.fill(color1)
    text('Press any key', font1, screen, 150, 150)
    text('to start!', font1, screen, 250, 300)
    pygame.display.update()
    waitForPlayerToPressKey()




    #starts music
    pygame.mixer.music.play(-1,0)
    t1 = time.time()#t1 is the time that the game begins
    font1 = pygame.font.SysFont('sans', 32)
    while run:

         #Timer
        t2 = time.time()#time at the moment of tick
        dT = t2-t1 #Change in time
        seconds=(180-(dT)) #calculate how many seconds
        if seconds<0: # if the timer is zero or less, end the game
            draw = True
            break




        #movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and event.key == pygame.K_KP8:
                    player2.jump()
                    player1.jump()
                if event.key == pygame.K_d and event.key == pygame.K_KP6:
                    player2.right()
                    player1.right()
                if event.key == pygame.K_KP4:
                    player2.left()
                if event.key == pygame.K_KP6:
                    player2.right()
                if event.key == pygame.K_KP8:
                    player2.jump()

                if event.key == pygame.K_a:
                    player1.left()
                if event.key == pygame.K_d:
                    player1.right()
                if event.key == pygame.K_w:
                    player1.jump()


                if event.key == pygame.K_SPACE:
                    y = True
                    if player1.facing == "l" and player1.jumping == False and player1.falling == False:#move sprite over to compensate for the sprite foot placement change
                        player1.rect.x -=20

                if event.key == pygame.K_KP_ENTER:
                    x = True
                    if player2.facing == "l" and player2.jumping == False and player2.falling == False:
                        player2.rect.x -=20



            if event.type == pygame.KEYUP:

                if event.key == pygame.K_KP4 and player2.dX <0:#if player removes finger from left/right keys, the character will stop
                    player2.stopped()

                if event.key == pygame.K_KP6 and player2.dX >0:
                    player2.stopped()

                if event.key == pygame.K_a and player1.dX <0:
                    player1.stopped()

                if event.key == pygame.K_d and player1.dX >0:
                    player1.stopped()

                if event.key == pygame.K_SPACE:

                    y = False
                    if size_counter2 <=125 and size_counter2 >85:#determines damage based on size of bullet
                        damage = 10
                        color = red

                    elif size_counter2 <=85 and size_counter2 >50:
                        damage = 5
                        color = orange

                    elif size_counter2 <= 50:
                        damage = 1
                        color = white

                    if player1.facing == "l":#shoots left
                        shoot = PlasmaBlast('l',size_counter2/ 5,damage,color)
                        if size_counter2 < 50:
                            shoot.rect.y = player1.rect.y + 20#changes x and y values depending on bullet size, so it will always look like it is coming out of the blaster
                            shoot.rect.x = player1.rect.x - 10
                        else:
                            shoot.rect.y = player1.rect.y +10
                            shoot.rect.x = player1.rect.x - 10
                            if player1.jumping == True: #as user holds down shoot, the bullet gets bigger in the x direction, so when moving left, the player collides with the bullet that grew right
                                shoot.rect.x = player1.rect.x - 30
                        player1.level.bullet_list.add(shoot)
                        if player1.jumping == False and player1.falling == False:
                            player1.rect.x +=20
                        shot.play()
                    elif player1.facing == "r":
                        shoot = PlasmaBlast('r',size_counter2/5,damage,color)
                        if size_counter2 < 50:
                            shoot.rect.y = player1.rect.y + 20
                        else:
                            shoot.rect.y = player1.rect.y + 10
                        shoot.rect.x = player1.rect.x + 40
                        player1.level.bullet_list.add(shoot)
                        shot.play()
                    size_counter2 = 30
                    player1.stop_shoot()


                if event.key == pygame.K_KP_ENTER:
                    x = False
                    if size_counter <=125 and size_counter >85:
                        damage = 10
                        color = red
                    elif size_counter <=85 and size_counter >50:
                        damage = 5
                        color = orange
                    elif size_counter <= 50:
                        damage = 1
                        color = white
                    if player2.facing == "l":
                        shoot = PlasmaBlast('l',size_counter/ 5,damage,color)

                        if size_counter < 50:
                            shoot.rect.y = player2.rect.y + 20
                            shoot.rect.x = player2.rect.x - 10
                        else:
                            shoot.rect.y = player2.rect.y + 10
                            shoot.rect.x = player2.rect.x - 10
                            if player2.jumping == True:
                                shoot.rect.x = player1.rect.x - 30

                        player2.level.bullet_list.add(shoot)
                        if player2.jumping == False and player2.falling == False:
                            player2.rect.x += 20
                        shot.play()
                    elif player2.facing == "r":
                        shoot = PlasmaBlast('r',size_counter/5,damage,color)
                        if size_counter < 50:
                            shoot.rect.y = player2.rect.y + 20
                        else:
                            shoot.rect.y = player2.rect.y + 10
                        shoot.rect.x = player2.rect.x + 40
                        player2.level.bullet_list.add(shoot)
                        shot.play()
                    size_counter = 30
                    player2.stop_shoot()


        if x:#holds down shoot
            player2.shoot()
            size_counter += 1

            if size_counter >= 125:
                size_counter = 125

        if y:
            player1.shoot()
            size_counter2 += 1
            if size_counter2 >= 125:
                size_counter2 = 125
        #bullet hits wall, remove bullet
        for bullet in level_used.bullet_list:
            block_hit_list = pygame.sprite.spritecollide(bullet, level_used.wall_list, False)
            for block in block_hit_list:
                level_used.bullet_list.remove(bullet)
        #bullet hits player, remove bullet and damgae character
            block_hit_list = pygame.sprite.spritecollide(player1, player2.level.bullet_list, False)
            for block in block_hit_list:
                hit.play()
                player1.health -= block.damage
                if player1.health <=0:
                    die.play()
                    run = False
                    win2 = True
                player2.level.bullet_list.remove(block)

            block_hit_list = pygame.sprite.spritecollide(player2, player1.level.bullet_list, False)
            for block in block_hit_list:
                hit.play()
                player2.health -= block.damage
                if player2.health <= 0:
                    die.play()
                    run = False
                    win1 = True
                player1.level.bullet_list.remove(block)

        if len(p1_name)== 4:#changes x position of nametag depending on sprite
            x1 = 7
        elif len(p1_name)== 3:
            x1 = 9
        elif len(p1_name)== 2:
            x1 = 10
        elif len(p1_name)== 1:
            x1 = 15
        if player1.facing =="r" and (player1.jumping == True or player1.falling == True):
            x1 += 15
        if player1.facing =="l" and (player1.jumping == True or player1.falling == True):
            x1 += 8
        if player1.facing =="l" and player1.shooting == True and player1.jumping == False and player1.falling == False:
            x1 +=20

        if len(p2_name)== 4:
            x2 = 7
        elif len(p2_name)== 3:
            x2 = 9
        elif len(p2_name)== 2:
            x2 = 10
        elif len(p2_name)== 1:
            x2 = 15
        if player2.facing =="r" and (player2.jumping == True or player2.falling == True):
            x2 += 15
        if player2.facing =="l" and (player2.jumping == True or player2.falling == True):
            x2 += 8
        if player2.facing =="l" and player2.shooting == True and player2.jumping == False and player2.falling == False:
            x2 +=20
        #updates screen
        sprites.update()
        level_used.update()
        level_used.draw(screen)
        sprites.draw(screen)
        #shows health and timer
        screen.blit(transform1,h1Rect)
        textcolor = white
        text("%d "%(player1.health) + '%',font1,screen,150,30)
        screen.blit(transform2,h2Rect)
        text("%d "%(player2.health) + '%',font1,screen,650,30)
        text(("%.2f" %(seconds)),font1,screen,350,30) #print how many seconds

        textcolor = name_color


        #prints nametag above characters
        trans_text((str(p1_name)),font_name,screen,player1.rect.x+x1,player1.rect.y - 20)
        trans_text((str(p2_name)),font_name,screen,player2.rect.x+x2,player2.rect.y - 20)
        clock.tick(60)
        pygame.display.update()



    #player 1 wins
    if win1 == True:
        color1 = (0,255,255)
        font2 = pygame.font.SysFont("arial",32)
        textcolor =(0,153,153)
        screen.fill(color1)
        pygame.mixer.music.pause()
        f = open("Score.txt",'a')#adding to the Score notepad list

        #draws the end screen
        text(("Congratulations %s!"%(p1_name)),font2,screen,150,150)
        text(("You successfully defeated %s with %d health left."%(p2_name, player1.health)),font2, screen,100,200)
        text("Press any key to restart.",font2,screen,100,300)
        pygame.display.update()
        waitForPlayerToPressKey()


        #restarts

        pygame.display.update()
        f.write("Player 1: " +str(p1_name) + "  Health left: " + str(player1.health)+ "  Time taken: %.2f seconds" %(dT) +'\n')#adds the score to the text file
        f.close()

        game()


    #player 2 wins
    elif win2 == True:
        color1 = (255,128,0)
        font2 = pygame.font.SysFont("arial",32)
        textcolor =(153,0,0)
        screen.fill(color1)
        pygame.mixer.music.pause()
        f = open("Score.txt",'a')#adding to the Score notepad list

        text(("Congratulations %s"%(p2_name)),font2,screen,150,150)
        text(("You successfully defeated %s with %d health left."%(p1_name, player2.health)),font2, screen,100,200)
        text("Press any key to restart.",font2,screen,100,300)
        pygame.display.update()
        waitForPlayerToPressKey()
    #restarts

        pygame.display.update()
        f.write("Player 2: " + str(p2_name) + "  Health left: " + str(player2.health)+"  Time taken: %.2f seconds" %(dT) +'\n')#adds the score to the text file
        f.close()

        game()
    #neither wins
    elif draw == True:
        color1 = (128,128,128)
        font2 = pygame.font.SysFont("arial",32)
        textcolor =(64,64,64)
        screen.fill(color1)
        pygame.mixer.music.pause()
        f = open("Score.txt",'a')#adding to the Score notepad list

        text(("Neither player won!"),font2,screen,150,150)
        text(("%s had %d health left,"%(p1_name, player1.health)),font2, screen,100,200)
        text(("while %s had %d health left."%(p2_name, player2.health)),font2, screen,100,250)
        text("Press any key to restart.",font2,screen,100,350)
        pygame.display.update()
        waitForPlayerToPressKey()
        #restarts

        pygame.display.update()
        f.write("Player 1 : Health left: " + str(player2.health) +"Player 2: Health left: " + str(player2.health) +'\n')#adds the score to the text file
        f.close()

        game()







    pygame.quit()
#run game
game()













