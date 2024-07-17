#import pygame
import pygame, random

#initialize pygame
pygame.init()

#set display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Snake eat the apple!")

#set FPS and clock
FPS = 20
clock = pygame.time.Clock()

#set game values
#snake is a square and so 20 x 20
SNAKE_SIZE = 13

#snake has a head and a body
#the head is what we control and the body follows along
#coordinates of head
head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2 + 100

#keep track of direction
#variables to keep track of how headis moving
#initially snake at rest, Zero means snake is not moving in that direction
#vales are 1, -1, 0: 1 meaning it is moving in that direction
#for example: pushing right key snake_dx = 1
# if press up key snake_dx=0 and snake_dy = 1
#if press down key snake_dx=0 and snake_dy = -1
snake_dx = 0
snake_dy = 0

#score variable
score = 0

#set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)

#set font
font = pygame.font.SysFont('gabriola', 48)

#set text
title_text = font.render("Snake  ", True, GREEN, DARKRED)
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

game_over_text = font.render("GAMEOVER!", True, RED, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("TO CONTINUE press any key!", True, RED, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#load sounds
pick_up_sound = pygame.mixer.Sound("pick_up_sound.wav")

#load images
#we don't have any images, just drawing rects on the screen
#going to use pygame's draw function
#the snake is eating a square or apple and keeps getting bigger with each apple
#just use coordinates
#for a rectangle you need x and y coordinates, and width and height: (topleft x, top left y, width, height)
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

#initially the snake is just a head
body_coords = []


#main game loop
running = True
while running:
    #check to see if user wants to quit
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            #set running to false
            running = False        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1*SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT:
                snake_dx = 1*SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1*SNAKE_SIZE
            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = 1*SNAKE_SIZE
    #add the head coordinate to the first index of the body coordinate list
    #this will essentially move all of the snakes body by one position in the list
    body_coords.insert(0, head_coord)
    body_coords.pop()

    #update x and y position of snake head, and make a new coordinate
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    #check for game over
    if head_rect.left < 0 or head_rect.right > WINDOW_HEIGHT or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_coords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #pause game until player preseeses a key, then reset game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0

                    head_x = WINDOW_WIDTH//2
                    head_y = WINDOW_HEIGHT//2 + 100
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

                    body_coords = []

                    snake_dx = 0
                    snake_dy = 0

                    is_paused = False

                #if player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    #check for collisions
    #if head_rect collides with apple_rect
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        #move apple
        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        #new apple coordinate
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        #whereever the head is the bosy will follow
        body_coords.append(head_coord)


    #update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)


    #fill the surface
    display_surface.fill(WHITE)

    #blit HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)

    #blit "assets" or drawn items
    #loop through body coordinates and draw rects
    #appending coordinates to the body
    #body will sppear now, but we still need to move it with the snake
    #the first coordinates of the body should go to where the head just was
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)

    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    pygame.display.update()
    clock.tick(FPS)

#quit game
pygame.quit()


