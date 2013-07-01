#        C:\Python33\Conor's_Pygame         #
#     Conor Scott's first pygame attempt    #
#       just a simple attempt at image      #
#       manipulation and keyboard input     #

    #####################
    # IMPORTING SECTION #
    # IMPORTING SECTION #                  
    # IMPORTING SECTION #                   
    #####################

import pygame, sys, random

from pygame.locals import *

try:
    import random
    import math
    import os
    import pickle
except err:
    print ("couldn't load module. %s" % err)
    sys.exit(2)

    ######################
    # INITIATION SECTION #
    # INITIATION SECTION #                 
    # INITIATION SECTION #                  
    ######################
    
#Initiate pygame, clock and font
pygame.init()
fpsClock = pygame.time.Clock()

#screen and caption initialized
listOfResolutions = pygame.display.list_modes()
indexOfResolutionList = 0

#Find best divisible by 32 resolution
for i in range(0, len(listOfResolutions)):
    if listOfResolutions[i][0] % 32 == 0 and listOfResolutions[i][1] % 32 == 0:
        indexOfResolutionList = i
        break

screen = pygame.display.set_mode(listOfResolutions[indexOfResolutionList], pygame.FULLSCREEN) #pygame.FULLSCREEN
pygame.display.set_caption("Conor's first pygame")

#make mouse invisible
pygame.mouse.set_visible(0)

    #####################
    # CONSTANTS SECTION #
    # CONSTANTS SECTION #                 
    # CONSTANTS SECTION #                  
    #####################

class Constants():
    #defining a few colour constants form: (r, g, b)
    redColor = pygame.Color(255, 0, 0)
    greenColor = pygame.Color(64, 255, 32)
    blueColor = pygame.Color(0, 0, 255)
    whiteColor = pygame.Color(255, 255, 255)
    blackColor = pygame.Color(0, 0, 0)
    screenX = listOfResolutions[indexOfResolutionList][0]
    screenY = listOfResolutions[indexOfResolutionList][1]

    ######################
    # BLOCK CLASS STARTS #
    # BLOCK CLASS STARTS #                  
    # BLOCK CLASS STARTS #                   
    ######################
    
class Block(pygame.sprite.Sprite):

    #Constructor
    def __init__(self, x, y):

        #Call parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y

        self.image = pygame.image.load("data/sprites/spriteBlock.png").convert()

        self.rect = self.image.get_rect()        
        self.rect.topleft = (self.x, self.y)
    
    ######################
    # LVL-G CLASS STARTS #
    # LVL-G CLASS STARTS #                  
    # LVL-G CLASS STARTS #                   
    ######################

class LevelGenerator():
    def generateLevel():
        level = []
        for j in range(0, (int(Constants.screenY/32))):
            level.insert(j, [])
            for i in range(0, (int(Constants.screenX/32))):
                if random.randrange(100) > 85:
                    level[j].append(Block(i*32, j*32)) ###GLOBAL POSITION HERE###
                else:
                    level[j].append(None)
        return level

    ######################
    # LEVEL CLASS STARTS #
    # LEVEL CLASS STARTS #                  
    # LEVEL CLASS STARTS #                   
    ######################

class Level():
    def __init__(self, doLoad=False):
        self.position = [None, None]
        if (doLoad):
            self.level = LevelGenerator.generateLevel()
        self.levelDict = {
            "north": None,
            "northEast": None,
            "east": None,
            "southEast": None,
            "south": None,
            "southWest": None,
            "west": None,
            "northWest": None
            }
               
    def setLevel(self, area, level):
        self.levelDict[area] = level

    def setPlayerOnLevel(self, player):
        self.level = LevelGenerator.generateLevel()
        player.level = self.level
        
        ##NORTH##
        if (self.levelDict["north"] is None):
            self.levelDict["north"] = Level(True)

            #SELF LINK
            self.levelDict["north"].setLevel("south", self)

        ##NORTH EAST##
        if (self.levelDict["northEast"] is None):
            self.levelDict["northEast"] = Level(True)

            ##SELF LINK
            self.levelDict["northEast"].setLevel("southWest", self)

            #ALGORITHM
            self.levelDict["north"].setLevel("east", self.levelDict["northEast"])
            self.levelDict["northEast"].setLevel("west", self.levelDict["north"])

        ##EAST##
        if (self.levelDict["east"] is None):
            self.levelDict["east"] = Level(True)

            ##SELF LINK
            self.levelDict["east"].setLevel("west", self)

            #ALGORITHM
            self.levelDict["east"].setLevel("north", self.levelDict["northEast"])
            self.levelDict["northEast"].setLevel("south", self.levelDict["east"])

            ##DIAGNOLS
            self.levelDict["east"].setLevel("northWest", self.levelDict["north"])
            self.levelDict["north"].setLevel("southEast", self.levelDict["east"])

        ##SOUTH EAST##
        if (self.levelDict["southEast"] is None):
            self.levelDict["southEast"] = Level(True)

            #SELF LINK
            self.levelDict["southEast"].setLevel("northWest", self)

            #ALGORITHM
            self.levelDict["southEast"].setLevel("north", self.levelDict["east"])
            self.levelDict["east"].setLevel("south", self.levelDict["southEast"])           

        ##SOUTH##
        if (self.levelDict["south"] is None):
            self.levelDict["south"] = Level(True)

            #SELF LINK
            self.levelDict["south"].setLevel("north", self)

            #ALGORITHM
            self.levelDict["south"].setLevel("east", self.levelDict["southEast"])
            self.levelDict["southEast"].setLevel("west", self.levelDict["south"])

            #DIAGNOLS
            self.levelDict["south"].setLevel("northEast", self.levelDict["east"])
            self.levelDict["east"].setLevel("southWest", self.levelDict["south"])

        ##SOUTH WEST##
        if (self.levelDict["southWest"] is None):
            self.levelDict["southWest"] = Level(True)

            #SELF LINK
            self.levelDict["southWest"].setLevel("northEast", self)

            #ALGORITHM
            self.levelDict["south"].setLevel("west", self.levelDict["southWest"])
            self.levelDict["southWest"].setLevel("east", self.levelDict["south"])
            
        ##WEST##
        if (self.levelDict["west"] is None):
            self.levelDict["west"] = Level(True)

            #SELF LINK
            self.levelDict["west"].setLevel("east", self)

            #ALGORITHM
            self.levelDict["west"].setLevel("south", self.levelDict["southWest"])
            self.levelDict["southWest"].setLevel("north", self.levelDict["west"])

            #DIAGNOLS
            self.levelDict["north"].setLevel("southWest", self.levelDict["west"])
            self.levelDict["west"].setLevel("northEast", self.levelDict["north"])
            self.levelDict["west"].setLevel("southEast", self.levelDict["south"])
            self.levelDict["south"].setLevel("norhtWest", self.levelDict["west"])
            
        ##NORTH WEST##
        if (self.levelDict["northWest"] is None):
            self.levelDict["northWest"] = Level(True)

            #SELF LINK
            self.levelDict["northWest"].setLevel("southEast", self)

            #ALGORITHM
            self.levelDict["northWest"].setLevel("south", self.levelDict["west"])
            self.levelDict["west"].setLevel("north", self.levelDict["northWest"])
            self.levelDict["north"].setLevel("west", self.levelDict["northWest"])
            self.levelDict["northWest"].setLevel("east", self.levelDict["north"])

    #######################
    # PLAYER CLASS STARTS #    
    # PLAYER CLASS STARTS #                 
    # PLAYER CLASS STARTS #                  
    #######################  

class Player(pygame.sprite.Sprite):

    #Constructor
    def __init__(self, x, y):

       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       self.x = x
       self.y = y
       self.speedX = 0
       self.speedY = 0

       self.image = pygame.image.load("data/sprites/spritePlayer.png").convert()
       self.rect = self.image.get_rect()
       self.rect.topleft = (self.x, self.y)

       self.level = None
       
    def canMoveUp(self, level):
        for row in level:
            for block in row:
                if block is not None:
                    TL = block.rect.topleft
                    testRect = Rect(TL[0], TL[1]-self.speedY, block.rect.width, block.rect.height)
                    if self.rect.colliderect(testRect):
                        return False
        return True

    def canMoveRight(self, level):
        for row in level:
            for block in row:
                if block is not None:
                    TL = block.rect.topleft
                    testRect = Rect(TL[0]-self.speedX, TL[1], block.rect.width, block.rect.height)
                    if self.rect.colliderect(testRect):
                        return False
        return True
    
    def canMoveDown(self, level):
        for row in level:
            for block in row:
                if block is not None:
                    TL = block.rect.topleft
                    testRect = Rect(TL[0], TL[1]-self.speedY, block.rect.width, block.rect.height)
                    if self.rect.colliderect(testRect):
                        return False
        return True
        
    def canMoveLeft(self, level):
        for row in level:
            for block in row:
                if block is not None:
                    TL = block.rect.topleft
                    testRect = Rect(TL[0]-self.speedX, TL[1], block.rect.width, block.rect.height)
                    if self.rect.colliderect(testRect):
                        return False
        return True

    def isUpOfLevel(self, level):
        if Constants.screenY/2 > self.y:
            return True
        return False
    
    def isRightOfLevel(self, level):
        if Constants.screenX/2 < self.x:
            return True
        return False

    def isDownOfLevel(self, level):
        if Constants.screenY/2 < self.y:
            return True
        return False
    
    def isLeftOfLevel(self, level):
        if Constants.screenX/2 > self.yx:
            return True
        return False
    
    def move(self, currLevel):
        if (self.speedX < 0 and self.canMoveLeft(self.level)):
            if (self.x) % Constants.screenX == 0:
                currLevel = currLevel.levelDict["west"]
                currLevel.setPlayerOnLevel(self)
                self.x += self.speedX
                self.rect.topleft = (self.x, self.y)
            else:
                self.x += self.speedX
                self.rect.topleft = (self.x, self.y)

        elif (self.speedX > 0 and self.canMoveRight(self.level)):
            if (self.x + 32) % Constants.screenX == 0:
                currLevel = currLevel.levelDict["east"]
                currLevel.setPlayerOnLevel(self)
                self.x += self.speedX
                self.rect.topleft = (self.x, self.y)
            else:
                self.x += self.speedX
                self.rect.topleft = (self.x, self.y)
                
        if (self.speedY < 0 and self.canMoveUp(self.level)):
            if (self.y) % Constants.screenY == 0:
                currLevel = currLevel.levelDict["north"]
                currLevel.setPlayerOnLevel(self)
                self.y += self.speedY
                self.rect.topleft = (self.x, self.y)
            else:
                self.y += self.speedY
                self.rect.topleft = (self.x, self.y)

        elif (self.speedY > 0 and self.canMoveDown(self.level)):   
            if (self.y + 32) % Constants.screenY == 0:
                currLevel = currLevel.levelDict["south"]
                currLevel.setPlayerOnLevel(self)
                self.y += self.speedY
                self.rect.topleft = (self.x, self.y)
            else:
                self.y += self.speedY
                self.rect.topleft = (self.x, self.y)

####DRAWING FUNCTIONS####

###CENETERED CAMERA AROUND PLAYER FUNCTION###

def drawLevel(level):
    for row in level:
        for block in row:
            if block is not None:

                if (block.x >= testPlayer.x):
                    if (block.y > testPlayer.y):
                        if block.x - testPlayer.x <= (Constants.screenX/2)+16:
                            if block.y - testPlayer.y <= (Constants.screenY/2)+16:
                                screen.blit(block.image, (-16 + Constants.screenX/2 + (block.x - testPlayer.x), -16 + Constants.screenY/2 + (block.y - testPlayer.y)))

                    elif block.y <= testPlayer.y:
                        if block.x - testPlayer.x <= (Constants.screenX/2)+16:
                            if testPlayer.y - block.y <= (Constants.screenY/2)+16:
                                screen.blit(block.image, (-16 + Constants.screenX/2 + (block.x - testPlayer.x), -16 + Constants.screenY/2 - (testPlayer.y - block.y)))

                elif (block.x < testPlayer.x):
                     if (block.y > testPlayer.y):
                        if testPlayer.x - block.x <= (Constants.screenX/2)+16:
                            if block.y - testPlayer.y <= (Constants.screenY/2)+16:
                                screen.blit(block.image, (-16 + Constants.screenX/2 - (testPlayer.x - block.x), -16 + Constants.screenY/2 + (block.y - testPlayer.y)))

                     elif (block.y <= testPlayer.y):
                        if testPlayer.x - block.x <= (Constants.screenX/2)+16:
                            if testPlayer.y - block.y <= (Constants.screenY/2)+16:
                                screen.blit(block.image, (-16 + Constants.screenX/2 - (testPlayer.x - block.x), -16 + Constants.screenY/2 - (testPlayer.y - block.y)))
                

###PRE GAME LOOP INITIALIZATIONS###

screen.fill(Constants.whiteColor)
direction = [0, 0]

testPlayer = Player((Constants.screenX/2)-16, ((Constants.screenY/2)-16))
testBlock = Block(128, 128)

currLevel = Level(True)
currLevel.setPlayerOnLevel(testPlayer)

    #####################
    # GAME LOGIC STARTS #
    # GAME LOGIC STARTS #                 
    # GAME LOGIC STARTS #                  
    #####################

while True:
    
    ###CREATES AN EMPTY CANVAS TO BE FILLED EVERY FRAME###
    screen.fill(Constants.greenColor)

    ###EVENT LOOP FOR KEYBOARD INPUT###
    for event in pygame.event.get():

        #QUIT SEQUENCES
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        ###WHAT HAPPENS WHEN KEYS ARE PRESSED
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            elif event.key == K_SPACE:
                currLevel.setPlayerOnLevel(testPlayer)
            elif event.key == K_RCTRL:
                testBlock.shrink(2)
            elif event.key == K_RALT:
                testBlock.image = pygame.transform.smoothscale(testBlock.image, (16, 16))
            elif event.key == K_LALT:
                testBlock.image = pygame.transform.smoothscale(testBlock.image, (32, 32))

        ###WHAT HAPPENS WHEN KEYS RELEASED
        if event.type == KEYUP:
            testPlayer.speedX = 0
            testPlayer.speedY = 0

        #######################
        # KEY POLLLING STARTS #
        # KEY POLLLING STARTS #                 
        # KEY POLLLING STARTS #                  
        #######################
        
        #GET KEYS PRESSED
        keys = pygame.key.get_pressed()
        
        #WHAT TO DO FOR EACH KEY 
        if keys[K_a]:
            testPlayer.speedX = -2
        if keys[K_d]:
            testPlayer.speedX = 2
        if keys[K_w]:
            testPlayer.speedY = -2
        if keys[K_s]:
            testPlayer.speedY = 2
            
    ###PLAYER MOVEMENT###
    if (testPlayer.speedX != 0 or testPlayer.speedY != 0):
        testPlayer.move(currLevel)

    ###DRAW BLOCKS OF CURRENT LEVEL###
    drawLevel(testPlayer.level)

    ###DRAW PLAYER###
    screen.blit((testPlayer.image), (((Constants.screenX/2)-16), (Constants.screenY/2)-16))                    

    #Updating graphics and limiting FPS to 30 
    pygame.display.flip()
    fpsClock.tick(60)

pygame.quit() #Being IDLE friendly

#   HOW TO USE PICKLE   #
#########################
#import pickle
#dbfile = open('people-pickle', 'rb') <---- OPEN people-pickle file, 'rb' means READ BINARY MODE
#db = pickle.load(dbfile) <---- GETS OBJECT
#dbfile.close() <--- SO NOW YOU CAN CLOSE
#db['sue']['pay'] *= 1.10
#db['tom']['name'] = 'Tom Tom' MAKE CHANGES
#dbfile = open('people-pickle', 'wb') <---- NOW SET TO WRITING SO YOU CAN SERIALIZE
#pickle.dump(db, dbfile) <---- THIS IS THE COMMAND TO PICKLE IT
#dbfile.close() <--- CLOSE TO FREE UP RESOURCES
