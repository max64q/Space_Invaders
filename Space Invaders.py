import pygame
import random
import math

#initialize pygame
pygame.init()

#create screen
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen_color = red, green, blue = 100, 100, 100 

gamespeed = 2

#title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo.png') #32x32 icon
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerMoveSpeed = 0.3 * gamespeed

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
enemyMoveSpeed = 0.2 * gamespeed

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, width - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemyMoveSpeed)
    enemyY_change.append(30)

#bullet
# ready - not on screen
#fire - on screen
bulletImg = pygame.image.load('lightning.png')
bulletX = 0
bulletY = playerY
bulletMoveSpeed = 0.5 * gamespeed
bullet_state = 'ready'

#scoring
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
font_color = red, green, blue = 255, 255, 255

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def showScore(x, y, color):
    score = font.render('Score: ' + str(score_val), True, color)
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg[0], (x, y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10)) #additions to place bullet center

#game over
def game_over(x,y, color):
    over_text = font.render('Score: ' + str(score_val), True, color)
    screen.blit(over_text, (x, y))

#collision check
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    if distance < 27:
        return True
    else:
        return False
        
    
    
#game loop
running = True
while running: #keeps window open until running = False
    screen.fill(screen_color) #screen background
    for event in pygame.event.get(): #loops through events to find quit
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        #check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change += -playerMoveSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change += playerMoveSpeed
            if event.key == pygame.K_UP:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change += playerMoveSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change += -playerMoveSpeed
        
            
    #boundary checks
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    if playerX > width - 64: #display width minus width of player
        playerX = width - 64
    
    #enemy movement
    for i in range(num_enemies):
        
        #game over
        if enemyY[i] >= playerY:
            for j in range(num_enemies):
                enemyY[j] = height + 100
                game_over(width / 2, height / 2, font_color)
                break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemyMoveSpeed
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= width - 64:
            enemyX_change[i] = -enemyMoveSpeed
            enemyY[i] += enemyY_change[i]
    
    #bullet movement
    if bulletY <= 0:
            bullet_state = 'ready'
            bulletY = playerY
            
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletMoveSpeed
    
    #collision
    for i in range(num_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = 'ready'
            score_val += 1
            enemyX[i] = random.randint(0, width - 64)
            enemyY[i] = random.randint(50, 150)
    
    showScore(textX, textY, font_color)
    player(playerX, playerY)
    for i in range(num_enemies):
        enemy(enemyX[i], enemyY[i])
    pygame.display.update() #updates screen
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
