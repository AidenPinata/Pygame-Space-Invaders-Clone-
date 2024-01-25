#All Laser functions are taken from Programming with Nick on YT
#https://www.youtube.com/watch?v=PFMoo_dvhyw&t=5s

#The port of getting pygame into python
import pygame, sys
from pygame.locals import *
import random

#Global variable for the levels in the game.
level = 1
highscore = 0

#Class for the main ship of the game
class Ship(pygame.sprite.Sprite):
    def __init__(self,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.startinghealth = health
        self.remaininghealth = health
        self.ship_img = mainSpaceinvadership
        self.ship_img2 = mainSpaceinvadership2
        
        self.x = x
        self.y = y
        self.laser_group = pygame.sprite.Group()
        self.laser_Ready = True
        self.lasertime = 0
        self.laser_delay = 300

    #Import to screen
    def draw(self):
        self.rect = Rect(self.x,self.y,80,80)
        if char == 1: 
            displaySurface.blit(self.ship_img,(self.x,self.y))
        else:
            displaySurface.blit(self.ship_img2,(self.x,self.y))

    #Moving ship
    def move(self,direction: str):
        if direction == "Left":
            if self.x > 2:
                self.x -= 12
        elif direction == "Right":
            if self.x < 1112:
                self.x += 12
    
    #To shoot the laser from the users input
    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.laser_Ready:
            self.laser_Ready = False
            laser = Laser((self.x + 40, self.y), 5, 600)  # Adjust the position and screen height as needed
            self.laser_group.add(laser)
            self.lasertime = pygame.time.get_ticks()

    #Recharge for the laser when shooting
    def Laser_Recharge(self):
        if not self.laser_Ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.lasertime >= self.laser_delay:
                self.laser_Ready = True

    #Healthbar for ship
    def healthbar(self):
        pygame.draw.rect(displaySurface,Red,(self.x + 5,self.y + 95,75,10))
        if self.remaininghealth > 0:
            pygame.draw.rect(displaySurface,Lightgreen,(self.x + 5,self.y + 95,75 - (self.startinghealth - self.remaininghealth),10))
 
#Taken from Programming With Nick on YT
class Laser(pygame.sprite.Sprite):
    def __init__(self,position,speed,screenx):
        super().__init__()
        self.image = pygame.Surface((4,15))
        self.image.fill((Lightgreen))
        self.rect = self.image.get_rect(center = position)
        self.speed = 20
        self.screenx = screenx

    #For the laser to delete when reached the top of the screen
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screenx + 15 or self.rect.y < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, invader_group,True):
            global highscore
            highscore += 100
            self.kill()

#Taken from Coding with Russ on YT
#Class for the invaders class of the game
class Invader(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("assets/images/invader5.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
    
    #Moves the invaders at the end of the screens width
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if abs(self.move_counter) > 350:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

# Class for the invaders lasers (sprite class)
class InvaderLasers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/Invader_laser.png")
        self.rect = self.image.get_rect(center=(int(x), int(y)))

    # Lasers removal when the invaders lasers hit the bottom of the screen
    def update(self):
        global ship_group,ship

        self.rect.y += 2
        if self.rect.top > 600:
            self.kill()

        # Check for collision with the ship
        hit_ships = pygame.sprite.spritecollide(self, ship_group, False)
        if hit_ships != []:
    
            #Removes the healthbar slowly
            ship.remaininghealth -= 25
            print(ship.remaininghealth)

            # Check if the ship's health has reached zero
            if ship.remaininghealth <= 0:
                endscreen()
            self.kill()


#Calling sprite groups
invader_group = pygame.sprite.Group()
invader_lasergroup = pygame.sprite.Group()
ship_group = pygame.sprite.Group()

#Variables for the formation of the invaders
rows = 4
cols = 5

#Laser cooldown and time for shooting for the invaders
invader_cooldown = 1250
lastlaser = pygame.time.get_ticks()

#For the formation for the invaders in the game
def invaderformation():       
        for row in range(rows):
            for item in range(cols):
                invader = Invader(400 + item * 100, 80 + row * 70)
                invader_group.add(invader)


#Next waves of invaders
def next_level():
    global level, invader_group
    # Check if all invaders have been destroyed
    if len(invader_group) == 0:
        level += 1
        # Respawn a new wave of invaders
        invaderformation()

#Call of the formation of the invaders
invaderformation()

#Call for music working
pygame.mixer.init()

#FPS for the game.
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

# set up the window
displaySurface = pygame.display.set_mode((1200,600))
pygame.display.set_caption('Space Invaders')

#Font for the game
gameFont = pygame.font.Font("assets/fonts/RETROTECH.ttf",48)
SmallergameFont = pygame.font.Font("assets/fonts/RETROTECH.ttf",25)
BiggergameFont = pygame.font.Font("assets/fonts/RETROTECH.ttf",65)

#Each load of the images
Background = pygame.image.load("assets/images/space1.jpg")
Background = pygame.transform.scale(Background,(1200,700))

IMGSpaceinvadership = pygame.image.load("assets/images/Space-Invaders-Ship.png")
IMGSpaceinvadership = pygame.transform.scale(IMGSpaceinvadership,(400,400))

IMGSpaceinvaderinvader = pygame.image.load("assets/images/invader1.png")
IMGSpaceinvaderinvader = pygame.transform.scale(IMGSpaceinvaderinvader,(400,300))

mainSpaceinvadership= pygame.image.load("assets/images/Space-Invaders-Ship.png")
mainSpaceinvadership = pygame.transform.scale(mainSpaceinvadership,(80,80))

mainSpaceinvadership2= pygame.image.load("assets/images/Space-Invaders-Ship2.png")
mainSpaceinvadership2 = pygame.transform.scale(mainSpaceinvadership2,(80,80))

mainSpaceinvaderinvader = pygame.image.load("assets/images/invader1.png")
mainSpaceinvaderinvader = pygame.transform.scale(mainSpaceinvaderinvader,(50,50))

Keyboard = pygame.image.load("assets/images/keyboard.png")
Keyboard = pygame.transform.scale(Keyboard,(800,300))

NightGame1Background = pygame.image.load("assets/images/spacemain1.jpg")
NightGame1Background = pygame.transform.scale(NightGame1Background,(1200,700))

NightGame2Background = pygame.image.load("assets/images/spacemain2.jpg")
NightGame2Background = pygame.transform.scale(NightGame2Background,(1200,700))

DayGameBackground = pygame.image.load("assets/images/skyimg.png")
DayGameBackground = pygame.transform.scale(DayGameBackground,(1200,700))

DayGame2Background = pygame.image.load("assets/images/skyimg2.png")
DayGame2Background = pygame.transform.scale(DayGame2Background,(1200,700))

SmallerNightbackground = pygame.image.load("assets/images/spacemain1.jpg")
SmallerNightbackground = pygame.transform.scale(SmallerNightbackground,(200,100))

SmallerDaybackground = pygame.image.load("assets/images/skyimg.png")
SmallerDaybackground = pygame.transform.scale(SmallerDaybackground,(200,100))

Leftarrow = pygame.image.load("assets/images/arrow1.png")
Leftarrow = pygame.transform.scale(Leftarrow,(100,100))

Rightarrow = pygame.image.load("assets/images/arrow2.png")
Rightarrow = pygame.transform.scale(Rightarrow,(100,100))

Backbutton = pygame.image.load("assets/images/backbutton.png")
Backbutton = pygame.transform.scale(Backbutton,(200,100))

#Each load of the sounds
clicksound = pygame.mixer.Sound("assets/sounds/clicksound.wav")
clicksound.set_volume(0.2)

#Position for the scrolling background
position = 0
pos2 = -600

#create colour tuples - (R,G,B)
White = (255,255,255)
Orange = (255, 125, 3)
Black = (0,0,0)
Red = (255, 0, 0)
Green = (0, 128, 0)
Lightgreen = (0, 252, 34)
Blue = (0, 0, 255)

#Menu opition for the game
char = 1
dayornight = 1

def background():
    #Global function to allow rotation
    global position,pos2,dayornight,char

    #If user picks either of the day or night features
    if dayornight == 1:
        displaySurface.blit(NightGame1Background, (0,position))
        displaySurface.blit(NightGame2Background,(0,pos2))
        if abs(position) > NightGame1Background.get_height():
            position = -600
        if abs(pos2) > NightGame1Background.get_height():
            pos2 = -600
    #If user picks either of the spaceship features
    else:
        displaySurface.blit(DayGameBackground, (0,position))
        displaySurface.blit(DayGame2Background,(0,pos2))
        if abs(position) > DayGameBackground.get_height():
            position = -600
        if abs(pos2) > DayGameBackground.get_height():
            pos2 = -600
    #Movement of the screens
    position += 3
    pos2 += 3

def creditscreen():
    while True:
        #Background of the end screen
        displaySurface.fill(Black)
        
        #Text for an illusion of inserting a coin to play
        txtforPressStart = BiggergameFont.render("Press Start",True,Orange)
        displaySurface.blit(txtforPressStart,(390,220))

        txtforcredit = SmallergameFont.render("Please Insert Coin To Continue",True,White)
        displaySurface.blit(txtforcredit,(395,290))

        #Events for the user inputs
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                startscreen()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()
        fpsClock.tick(FPS)

def startscreen():
    #PLAYING MUSIC 
    pygame.mixer.music.load("assets/sounds/startmenu.mp3")
    pygame.mixer.music.play(-1)
    
    while True:
        #Blit command used to grab images to the start screen
        displaySurface.blit(Background,(0,0))
        displaySurface.blit(IMGSpaceinvadership,(0,100))
        displaySurface.blit(IMGSpaceinvaderinvader, (750,150))

        #Text for Title for start screen
        Title = gameFont.render("Space Invaders",True,White)
        displaySurface.blit(Title,(400, 13))

        #Text for the Credit for start screen
        Credittitle = SmallergameFont.render("Credits: 1",True,White)
        displaySurface.blit(Credittitle,(1090, 580))
        
        #Text for the new game in the start screen
        New_Game = gameFont.render("New game",True,White)
        displaySurface.blit(New_Game,(460, 240))
        New_Gamehitbox = pygame.Rect(456, 239, 240, 40)

        #Text for the Manu in the start screen
        Menu = gameFont.render("Menu",True,White)
        displaySurface.blit(Menu,(514, 352))
        Menuhitbox = pygame.Rect(513, 352, 120, 40)

        #Text for quitting in the start screen
        Quit = gameFont.render("Quit",True,White)
        displaySurface.blit(Quit,(525, 450))
        Quithitbox = pygame.Rect(526, 447, 120, 30)
    
    #Basic events for the users input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
            #When users uses the mouse.
            if event.type == MOUSEBUTTONDOWN: 
                point = pygame.mouse.get_pos()
                clicksound.play()
                
                #hitboxes for the the buttons so they are able to switch
                if New_Gamehitbox.collidepoint(point):
                    pygame.mixer.music.stop()
                    controlscreen()
            
                elif Menuhitbox.collidepoint(point):
                    pygame.mixer.music.stop()
                    Menuopition()
            
                elif Quithitbox.collidepoint(point):
                    event.type == QUIT
                    pygame.quit()
                    sys.exit()
                
        pygame.display.update()
        fpsClock.tick(FPS)

def NewGame():
    global lastlaser,ship,ship_group,level

    #Ship position
    ship = Ship(552,490,75)
    ship_group.add(ship)
    print(ship_group)
    #Music for the background of the game
    pygame.mixer.music.load("assets/sounds/maingame.mp3")
    pygame.mixer.music.play(-1)

    while True:  
        #Scrolling background function for the background of the game
        background()

        #Created lasers for the invaders
        time_now = pygame.time.get_ticks()
        
        #For if the lasers time is with the invaders on the screen including its cooldown being normal, it allows the random invaders to shoot when on the screen inclduing its cooldown
        if time_now - lastlaser > invader_cooldown and len(invader_lasergroup) < 5 and len (invader_group) > 0:
            invader1 = random.choice(invader_group.sprites())
            invader_laser = InvaderLasers(invader1.rect.centerx,invader1.rect.bottom)
            invader_lasergroup.add(invader_laser)
            lastlaser = time_now
       
        #Calling Methods
        ship.draw()
        ship.healthbar()
        ship.shoot()
        ship.Laser_Recharge()

        #Calling Sprite methods
        ship.laser_group.update()
        ship.laser_group.draw(displaySurface)
        
        invader_group.update()
        invader_group.draw(displaySurface)

        invader_lasergroup.update()
        invader_lasergroup.draw(displaySurface)
  
        #Text for continous levels for the game
        Txtforlevel = gameFont.render(f"Wave:{level}",True,White)
        displaySurface.blit(Txtforlevel,(14, 20))

        txt_for_highscore = SmallergameFont.render(f"Highscore: {highscore}",True,White)
        displaySurface.blit(txt_for_highscore,(14,100))

        #Keys input by the user and its recommanded output (movement)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            ship.move("Left")

        elif keys [K_RIGHT]:
            ship.move("Right")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Check for next level after a short delay
        if time_now % 350 == 0:  # Adjust the delay as needed
            next_level()
                
        pygame.display.update()
        fpsClock.tick(FPS)

def Menuopition():
    #PLAYING MUSIC FOR THE MENU
    pygame.mixer.music.load("assets/sounds/menumusic.mp3")
    pygame.mixer.music.play(-1)

    while True:
        global char,dayornight

        #Space background for the menu
        displaySurface.blit(Background,(0,0))
        
        #Character selection
        displaySurface.blit(Leftarrow,(393,227))
        first_leftarrowhitbox = pygame.Rect((402, 237,100,100))

        displaySurface.blit(Rightarrow, (738,227))
        first_Rightarrowhitbox = pygame.Rect((742, 237,100,100))

        #Background selection
        displaySurface.blit(Leftarrow,(393,500))
        second_leftarrowhitbox = pygame.Rect((396, 515,100,100))

        displaySurface.blit(Rightarrow, (738,500))
        second_Rightarrowhitbox = pygame.Rect((739, 511,100,100))

        #Back button for menu
        displaySurface.blit(Backbutton,(23,32))
        backbuttonhitbox = pygame.Rect((50,49,100,100))

        #If the user picks day or night time
        if dayornight % 2 != 0:
            image = SmallerNightbackground
        else:
            image = SmallerDaybackground

        displaySurface.blit(image,(500,470))

        #If the user picks on of the two space ships
        if char % 2 != 0:
            character = mainSpaceinvadership
        else:
            character = mainSpaceinvadership2

        displaySurface.blit(character,(575,235))

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()
                clicksound.play()
                
                #hitboxes for the the buttons so they are able to switch
                if first_leftarrowhitbox.collidepoint(point):
                    char -= 1

                elif first_Rightarrowhitbox.collidepoint(point):
                    char += 1

                elif second_leftarrowhitbox.collidepoint(point):
                    dayornight -= 1

                elif second_Rightarrowhitbox.collidepoint(point):
                    dayornight += 1

                elif backbuttonhitbox.collidepoint(point):
                    pygame.mixer.music.stop()
                    startscreen()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)

#Used for a transparent rectangle for indicating what the user can control.
def drawRect(x: int, y: int, width: int, height: int, color: tuple, alpha: int):
    s = pygame.Surface((width, height))  # the size of your rect
    s.set_alpha(alpha)
    s.fill(color) # this fills the entire surface
    displaySurface.blit(s, (x, y))  

def controlscreen():
    #Allows pause and time for certain text to enter.
    time = 0

    while True:
        #Background and images
        displaySurface.fill(Black)
        displaySurface.blit(Keyboard,(180,150))
        
        #Text for indication on where the controls are
        Txtforshoot = SmallergameFont.render("To fire lasers",True,White)
        displaySurface.blit(Txtforshoot,(507, 475))
        Txtformoving = SmallergameFont.render("To move ship left and right",True,White)
        displaySurface.blit(Txtformoving,(860, 482))

        #Time function for no inputs
        time += 1/FPS

        #If statement so user can't access the game without looking at controls
        if time >= 4:
            Nextscreen = gameFont.render("Enter any key to start the game.",True,White)
            displaySurface.blit(Nextscreen,(230, 13))

        #Green Rect for spacebar.
        drawRect(503,398,257,50,Lightgreen,128)

        #Green Rect for left arrow key.
        drawRect(857,396,40,50,Lightgreen,128)

        #Green Rect for right arrow key.
        drawRect(933,395,40,50,Lightgreen,128)

        #Event type for letting user get into the next game.
        for event in pygame.event.get():
            if event.type == KEYDOWN and time >= 4:
                NewGame()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()
        fpsClock.tick(FPS)
                
def endscreen():
    #Pauses for credit screen
    time = 0 
    #Countdown method for displaying a countdown
    countdown = 6
    last_count = pygame.time.get_ticks()

    pygame.mixer.music.load("assets/sounds/gameover.wav")
    pygame.mixer.music.play(-1)

    while True:
        global level,char,dayornight,highscore
        #Background for game over
        displaySurface.fill(Black)

        #Text for retro game over (Super Mario feel)
        txtforgameover = gameFont.render("Game Over",True,Red)
        displaySurface.blit(txtforgameover,(450,300))

        #Time function for no inputs
        time += 1/FPS
        
        #If statement for the known time 
        if time > 6:
            level = 1
            highscore = 0
            dayornight = 1
            char = 1
            pygame.mixer.music.stop()
            invader_lasergroup.empty()
            invader_group.empty()
            invaderformation()
            creditscreen()

        #If statement indicating the countdown being rendered higher than 0 (intial value)
        if countdown >= 0:
            #Txt for the prompt for continuing
            txtforcontinue = SmallergameFont.render("Please Insert a new Coin to Continue",True,White)
            displaySurface.blit(txtforcontinue,(360,360))
            txtforcountdown = SmallergameFont.render(str(countdown),True,White)
            displaySurface.blit(txtforcountdown,(580,420))
            #Getting the ticks
            count_timer = pygame.time.get_ticks()
            
            #If statement to indicate the downward count for the time in insert a new coin
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

            #If the user does presses a key, it renders as a new coin including quit.
            for event in pygame.event.get():
                if event.type == KEYDOWN and time > 2:
                    highscore = 0
                    level = 1
                    pygame.mixer.music.stop()
                    invader_lasergroup.empty()
                    invader_group.empty()
                    invaderformation()
                    NewGame()
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)

#All def functions in the order they should be.
        
creditscreen()
startscreen()
controlscreen()
Menuopition()
background()
NewGame()
endscreen()