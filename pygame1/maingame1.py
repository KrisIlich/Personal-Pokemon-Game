import pygame
import random
import math
import time
from pygame import mixer

#intialize pygame
pygame.init()

#create the game screen
screen = pygame.display.set_mode((800, 600))

#bkgd
bkgd = pygame.image.load('bkgd.png')

#bkgd sound
mixer.music.load('theme.mp3')
mixer.music.play()
pygame.mixer.music.set_volume(0.1)

#Title and Icon
pygame.display.set_caption("Pokemon: The Kris Version")
icon = pygame.image.load('r.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 458
playerX_move = 0

#enemy list
enemyImg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []
num_of_enemies = 4

#enemy
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg.append(pygame.image.load('bird.png'))
    enemyX.append(random.randint(0,699))
    enemyY.append(random.randint(50,150))
    enemyX_move.append(0.7)
    enemyY_move.append(25)

#ball
#"ready" bullet isnt visible
#"fire" bullet is animated
ballImg = pygame.image.load('ball.png')
ballX = 0
ballY = 458
ballX_move = 0
ballY_move = 0.8 
ball_state = "ready"

#greatBallImg = pygame.image.load('greatball.png')
#greatBallX = 0
#greatBallY = 458
#greatBallX_move = 0
#greatBallY_move = 0.4
#greatBall_state = "ready"

#score
score_value = 0
font = pygame.font.Font('PocketMonk-15ze.ttf', 40)
textX = 10
textY = 10


#game over text
game_over_font = pygame.font.Font('PocketMonk-15ze.ttf', 72)

#functions ------------------------------------------------------------------------------------
 

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (275  , 250))
 
 #score function
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#collision
def collide(enemyX, enemyY, ballX, ballY):
    distance = math.sqrt((math.pow(enemyX - ballX,2)) + (math.pow(enemyY - ballY,2)))
    if distance < 30:
        return True
    else:
        return False
    
def collide_player(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX,2)) + (math.pow(enemyY - playerY,2)))
    if distance < 55:
        return True
    else:
        return False

#player image function takes in x and y coordinates, when called puts in playerX and playerY for player starting position
def player(x, y):
    screen.blit(playerImg, (x, y))  

#enemy function for movement same as above
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  

#pokeball starting position same as above
def fire_ball(x, y):
     global ball_state
     ball_state = "fire"
     screen.blit(ballImg, (x, y))

#def fire_greatball(x, y):
    #global greatBall_state
    #greatBall_state = "fire"
    #screen.blit(greatBallImg, (x, y))



#Game Infinite loop --------------------------------------------------------------------------------------
running = True
while running:

    #RGB bkgd
    screen.fill((0,0,0))

    #Background Img
    screen.blit(bkgd, (0,0))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #player movement
        #if key is pressed player will move       
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_move = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_move = 0.3

            if event.key == pygame.K_SPACE:
                if ball_state == "ready":
                    ballSound = mixer.Sound('ballthrow.mp3')
                    ballSound.play()
                    ballSound.set_volume(0.2)  
                    ballX = playerX
                    fire_ball(ballX, ballY)

            #if event.key == pygame.K_SPACE:
                #if greatBall_state is "ready":
                    #greatBallX = playerX
                    #fire_greatball(greatBallX, greatBallY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0

    #player out of bounds
    playerX += playerX_move
    if playerX <= 0:
        playerX = 0
    elif playerX >= 700:
            playerX = 700


    #enemy movement
    for i in range(num_of_enemies):

        #gameover
#        if enemyY[i] > 400:
 #           for j in range(num_of_enemies):
  #             enemyY[j] = 2000
   #         game_over()
    #        break

        if enemyY[i] > 400 and abs(playerX-enemyX[i]) < 80:
            for j in range(num_of_enemies):
                enemyY[j] = 2000     
            game_over()
            break
            


        enemyX[i] += enemyX_move[i]
        if enemyX[i] <= 0:
            enemyX_move[i] = 0.7
            enemyY[i] += enemyY_move[i]
        elif enemyX[i] >= 750:
                enemyX_move[i] = -0.7
                enemyY[i] += enemyY_move[i]



        collision = collide(enemyX[i], enemyY[i], ballX, ballY)
        if collision:
            catchSound = mixer.Sound('catch.mp3')
            catchSound.play()  
            catchSound.set_volume(0.2)  
            ballY = 458
            ball_state = "ready"
            score_value += 100
            enemyX[i] = random.randint(0,699)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)
        

    #pokeball movement
    if ballY <= 0:
        ballY = 458
        ball_state = "ready"
    if ball_state == "fire":
        fire_ball(ballX, ballY)
        ballY -= ballY_move

    #great ball movement
    #if greatBallY <= 0:
            #greatBallY = 458
            #greatBall_state = "ready"
    #if ball_state is "fire":
        #fire_greatball(greatBallX, greatBallY)
        #greatBallY -= greatBallY_move
         


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()