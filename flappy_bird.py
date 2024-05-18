import pygame
from pygame.locals import *
import random

pygame.init()

# Dimensions of the screen window that will appear when program runs
screen_width = 864
screen_height = 936

# defining the frame rate so that everything runs at a consistent rate (instead of making it run as fast as it can)
clock = pygame.time.Clock()
fps = 60

# Sets the screen to a variable so that the screen appears when it runs with
# both the "screen_width" and the "screen_height" variable. The second line adds the title to the game window

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# define colours
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 # milliseconds
last_pipe = pygame.time.get_ticks() # measuring the time
score = 0
pass_pipe = False


# load images (that is what the bg variable contains)
bg = pygame.image.load('bg.png')
ground_img = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')

# creating a function to draw text on the screen (by converting the text to an image and using the blit function to display it on the screen)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# reset game function that automaticially sets game variables to zero
def reset_game():
    # '.empty' deletes everything in 'pipe_group'
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


# make a bird class while also using pygame's sprite class. pygame's sprite function already has built in 
# code so you don't need to code blit funcitoins and update functions
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # creating the list of images that will flip through in order to animate the bird (like a flipbook). 
        # self.images is the list of images, self.index is which image is being displayed, and self.counter is the speed that each image is being displayed for.
        self.images = []
        self.index = 0
        self.counter = 0

        # this for loop is cycling through the images by using num as a range of 1 through 4 since there are three images and formatting the string so that it cycles through each image while adding it to the self.images list afterwards
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        # loading bird image and also adding positioning. self.rect creates a 'rectangle' around the image 
        # that adds boundaries to the image. 'self.rect.center' is the function used to position the rectangle
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # the velocity of the bird
        self.vel = 0
        self.clicked = False
    
    def update(self):

        if flying == True:
            # making the velocity of the bird (gravity)
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # making it so that when the bird hits the ground it doesn't move down (it only drops when it is above the ground)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

            # handle the animation
            self.counter += 1
            flap_cooldown = 5
            # switching between each image and resetting to the first image once self.index goes higher than the list values
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            # updating the image
            self.image = self.images[self.index]

            # rotating the bird (by using built-in oygame functions). the first value is the image that is rotating, and the second value is the angle that it is rotating, by default it rotates anti-clockwise so you have to multiply it by a 
            # negative number in order to make it rotate clockwise.
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# creating the pipes ( similar to creating the bird)
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        # this is a pygame function that inherits sprite functions from the sprite class
        pygame.sprite.Sprite.__init__(self)
        # loading image and the rectangle around the image
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, position -1 is from the bottom. '.transform' is a pygame method that lets you flip images
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) 
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

# class to create a button (creating the image and making a rectangle around it) with positioning
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        
        action = False

        # get mouse position (using built in pygame functions)
        pos = pygame.mouse.get_pos()

        # check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# a special list used to manage and contain multiple sprite objects (although we only have one at a time)
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# defining the acutal bird, with the position of where it is going to be
flappy = Bird(100, int(screen_height / 2))

# adding flappy bird to 'bird_group'
bird_group.add(flappy)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

# run is a variable which is always true when the game is running except for when the game closes.
run = True
while run:

    # using .tick to actually set the framerate after defining it
    clock.tick(fps)
    
    # blit function is how you display images onto the screen
    # draw background
    screen.blit(bg, (0,0))

    # drawing the birds ('bird_group'). '.draw' is a built in function in the sprite class
    bird_group.draw(screen)
    bird_group.update()
    # drawing the pipes
    pipe_group.draw(screen)

    # check the score (by checking if the right or left side of the triangle have crossed certain points accross the pipes)
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # look for collisions (with pipes)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # check if bird has hit the ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 768))
    
    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # draw and scroll the ground (abs is the "absolute function" which always returns a positive value)
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()


    # check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()


    # The for loop adds the function so that you can actually exit the game window by pressing the X button. Without this for loop you cannot exit out of the game window
    # even if you press the X button.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # this lets you start the game instead of it running as soon as the program starts
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    # an extra function that is needed to update everything above (in the while loop)
    pygame.display.update()

pygame.quit()