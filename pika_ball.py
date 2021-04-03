'''
very simple pikaball clone
'''
import pygame
import sys
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import time
import random
import math
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()   
        self.v = 0

    def setsurf(self,*size):
        self.surf = pygame.Surface(size)

    def setrect(self,position):
        self.rect = self.surf.get_rect(center = position)

    def add_image_ball(self,directory):#add image method for ball
        self.image = pygame.image.load(directory).convert_alpha()
        self.image = pygame.transform.scale(self.image,
            (BALLRADIUS,BALLRADIUS))

    def add_image(self,directory):
        self.image = pygame.image.load(directory).convert_alpha()
        self.image = pygame.transform.scale(self.image,
            (PIKAWIDTH,PIKAHEIGHT))

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self):#move using arrow key
        if pygame.key.get_pressed()[K_RIGHT]:#right is pressed
            if self.rect.x < SCREENWIDTH - PIKAWIDTH:
                self.rect.move_ip(HORIZONTAL_SPEED,0)
        if pygame.key.get_pressed()[K_LEFT]:#left is pressed
            if self.rect.x > SCREENWIDTH / 2 + NETWIDTH / 2:
                self.rect.move_ip(-HORIZONTAL_SPEED,0)

    def movewasd(self):#move using wasd
        if pygame.key.get_pressed()[K_a]:
            if self.rect.x > 0:
                self.rect.move_ip(-HORIZONTAL_SPEED,0)
        if pygame.key.get_pressed()[K_d]:
            if self.rect.x < SCREENWIDTH / 2 - NETWIDTH / 2 - PIKAWIDTH:
                self.rect.move_ip(HORIZONTAL_SPEED,0)

    def jump(self):#jump using up
        if pygame.key.get_pressed()[K_UP]:
            if self.rect.y >= SCREENHEIGHT - PIKAHEIGHT:
                self.v = -JUMP_VELOCITY

    def jumpw(self):#jump using w
        if pygame.key.get_pressed()[K_w]:
            if self.rect.y >= SCREENHEIGHT - PIKAHEIGHT:
                self.v = -JUMP_VELOCITY

    def gravity(self):#down = positive; up = negative
        if self.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            self.v += GRAVITY
    '''   
    def gravityw(self):#down = positive; up = negative
        if self.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            self.v += GRAVITY
    '''
    def velocity(self):
        if self.v != 0 or self.rect.x != SCREENHEIGHT - PIKAHEIGHT: 
            self.rect.move_ip( 0 , self.v ) 
            if self.rect.y > SCREENHEIGHT - PIKAHEIGHT:
                self.rect.y = SCREENHEIGHT - PIKAHEIGHT

    def velocityw(self):
        if self.v != 0: 
            self.rect.move_ip( 0 , self.v ) 
            if self.rect.y > SCREENHEIGHT - PIKAHEIGHT:
                self.rect.y = SCREENHEIGHT - PIKAHEIGHT

    def gravity_ball(self):#gravity for ball; downward = positive
        if self.rect.y < SCREENHEIGHT - BALLRADIUS:
            self.v += GRAVITY 

    def velocity_ball(self):
        if self.v != 0:
            self.rect.move_ip( 0 , self.v ) 
            if self.rect.y > SCREENHEIGHT - PIKAHEIGHT:#ball is underground
                self.rect.y = SCREENHEIGHT - PIKAHEIGHT#move to surface


    def set_position(self,*coordinate):
        self.rect.center = coordinate

    def smash_from_left(self,ballbody):
        if pygame.key.get_pressed()[K_z]:
            if pymunk.Vec2d.get_distance(ballbody.position,pymunk.Vec2d(\
                    self.rect.x + PIKAWIDTH / 2 ,\
                    self.rect.y +PIKAHEIGHT / 2)) < BALLRADIUS+25:
                shortsmash = True
                angle = None
                if pygame.key.get_pressed()[K_d] or\
                        pygame.key.get_pressed()[K_a]:
                    shortsmash = False
                    if pygame.key.get_pressed()[K_w]:
                        angle = 45
                    elif pygame.key.get_pressed()[K_s]:
                        angle = 315
                    else:
                        angle = 0
                elif pygame.key.get_pressed()[K_s]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_w]:
                        angle = 270
                elif pygame.key.get_pressed()[K_w]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_s]:
                        angle = 90
                elif shortsmash == True:
                    angle = 0
                degree_angle = angle * math.pi / 180
                if shortsmash == True:
                    pass
                    #ballbody.velocity = pymunk.Vec2d(\
                    #200+1.03 * ballbody.velocity.__abs__() * 0.7,0)
                    #short smash removed                           
                if shortsmash == False:
                    ballbody.velocity = pymunk.Vec2d(\
                        200+1.1 * ballbody.velocity.__abs__() \
                        * math.cos(degree_angle),\
                        -1.1 * ballbody.velocity.__abs__() \
                        * math.sin(degree_angle))
                
    def smash_from_right(self,ballbody):
        if pygame.key.get_pressed()[K_RETURN]:
            if pymunk.Vec2d.get_distance(\
                    ballbody.position,pymunk.Vec2d(\
                    self.rect.x + PIKAWIDTH / 2 ,\
                    self.rect.y +PIKAHEIGHT / 2)) < BALLRADIUS+25:
                shortsmash = True
                angle = None
                if pygame.key.get_pressed()[K_LEFT] or\
                        pygame.key.get_pressed()[K_RIGHT]:
                    shortsmash = False
                    if pygame.key.get_pressed()[K_UP]:
                        angle = 135

                    elif pygame.key.get_pressed()[K_DOWN]:
                        angle = 225

                    else:
                        angle = 180
                elif pygame.key.get_pressed()[K_DOWN]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_UP]:
                        angle = 270
                elif pygame.key.get_pressed()[K_UP]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_DOWN]:
                        angle = 90
                elif shortsmash == True:
                    angle = 180
                degree_angle = angle * math.pi / 180
                if shortsmash == True:
                    pass
                    #ballbody.velocity = pymunk.Vec2d(\
                    #-200+1.03 * ballbody.velocity.__abs__() * 0.7,0)
                    #shortsmash removed
                if shortsmash == False:
                    ballbody.velocity = pymunk.Vec2d(\
                        -200+1.1 * ballbody.velocity.__abs__() \
                        * math.cos(degree_angle),\
                        -1.1 * ballbody.velocity.__abs__() \
                        * math.sin(degree_angle))

def ball_velocity_limit(maxv,ballbody):
    if ballbody.velocity.__abs__() > maxv:
        ballbody.velocity = pymunk.Vec2d(\
            ballbody.velocity.x/ballbody.velocity.__abs__()*maxv,\
            ballbody.velocity.y/ballbody.velocity.__abs__()*maxv)

MINBALLENERGY = -150000
MAXBALLVELOCITY = 1400
JUMP_VELOCITY = 12
HORIZONTAL_SPEED = 5
GRAVITY = 0.15
SCREENWIDTH = 1250
SCREENHEIGHT = 750
NETHEIGHT = 250
NETWIDTH = 17
PIKAWIDTH = 150
PIKAHEIGHT = 150
BALLRADIUS = 120

scoreboard = [0,0]

def main():
    def ball_spawn_left():#ball spawn
        ball_body.position = ( 60 , 60 )
        ball_body.velocity = (0,0)

    def ball_spawn_right():
        ball_body.position = ( SCREENWIDTH - 60 , 60 )
        ball_body.velocity = (0,0)

    def score_point():#point counter
        if ball_body.position.y >= SCREENHEIGHT - BALLRADIUS / 2 + 10:
            if ball_body.position.x > SCREENWIDTH / 2:
                scoreboard[0] += 1
                ball_spawn_right()
                player_left.setrect((PIKAWIDTH / 2 ,\
                    SCREENHEIGHT - PIKAHEIGHT / 2))
                player_right.setrect((SCREENWIDTH - PIKAWIDTH / 2 ,\
                    SCREENHEIGHT - PIKAHEIGHT / 2))
                player_left.v = 0
                player_right.v = 0
                
            elif ball_body.position.x <= SCREENWIDTH / 2:
                scoreboard[1] += 1
                ball_spawn_left()
                player_left.setrect((PIKAWIDTH / 2 ,\
                    SCREENHEIGHT - PIKAHEIGHT / 2))
                player_right.setrect((SCREENWIDTH - PIKAWIDTH / 2 ,\
                    SCREENHEIGHT - PIKAHEIGHT / 2))
                player_left.v = 0
                player_right.v = 0
            time.sleep(0.3)

    def ball_energy_limit(mine,ballbody):
        if 0.5*ballbody.velocity.__abs__()**2-800*ballbody.position.y < mine\
                and pymunk.Vec2d.get_distance(ballbody.position,pymunk.Vec2d\
                (player_right.rect.x + PIKAWIDTH / 2 , player_right.rect.y +\
                PIKAHEIGHT / 2)) > BALLRADIUS+10 \
                and pymunk.Vec2d.get_distance(ballbody.position,pymunk.Vec2d\
                (player_left.rect.x + PIKAWIDTH / 2 , player_left.rect.y +\
                PIKAHEIGHT / 2)) > BALLRADIUS+10:
            ballbody.velocity = pymunk.Vec2d(\
                ballbody.velocity.x/ballbody.velocity.__abs__()*math.sqrt(\
                2*(mine+800*ballbody.position.y)),\
                ballbody.velocity.y/ballbody.velocity.__abs__()*math.sqrt(\
                2*(mine+800*ballbody.position.y)))
                
    pygame.init()
    FPS = 130
    framespersec = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pygame.display.set_caption("pikaball")
    running = True

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = 0, 800
    
    pts = [(-100,-100),(1350,-100),(1350,850),(-100,850)]#set corner coords
    segment = pymunk.Segment(space.static_body,(SCREENWIDTH / 2 ,\
        (SCREENHEIGHT - NETHEIGHT)*1.03),(SCREENWIDTH / 2 , SCREENHEIGHT),\
        NETWIDTH / 2)#網子
    segment.elasticity = 1
    segment.color = (0,0,0,0)

    for i in range(4):#create a box 
        seg = pymunk.Segment(space.static_body, pts[i], pts[(i+1)%4], 100)
        seg.elasticity = 1
        seg.color = (0,0,0,0)
        space.add(seg)

    right_pika_hit_box_body = pymunk.Body(body_type = 1)
        #attach segment to pika as hitbox
    right_pika_hit_box = pymunk.Segment(right_pika_hit_box_body,\
        (SCREENWIDTH - PIKAWIDTH / 2 ,SCREENHEIGHT - PIKAWIDTH / 2.6),\
        (SCREENWIDTH - PIKAWIDTH / 2, SCREENHEIGHT*1.1 - PIKAHEIGHT*1.1),\
        PIKAWIDTH / 2.6)
    right_pika_hit_box.elasticity = 0.8
        #kinemetic body type is used for pika(body_type = 1)
    right_pika_hit_box.color = (0,0,0,256)
    
    left_pika_hit_box_body = pymunk.Body(body_type = 1)
    left_pika_hit_box = pymunk.Segment(left_pika_hit_box_body,\
        (SCREENWIDTH - PIKAWIDTH / 2 ,SCREENHEIGHT - PIKAWIDTH / 2.6),\
        (SCREENWIDTH - PIKAWIDTH / 2, SCREENHEIGHT*1.1 - PIKAHEIGHT*1.1),\
        PIKAWIDTH / 2.6)
    left_pika_hit_box.elasticity = 0.8
    left_pika_hit_box.color = (0,0,0,256)

    ball_body = pymunk.Body(mass = 10000,moment = 0.0000001)
    ball_body.position = (SCREENWIDTH / 2 , 60 )
    circle = pymunk.Circle(ball_body, radius = 50)
    circle.elasticity = 1
    space.add(ball_body, circle,segment,right_pika_hit_box,\
        right_pika_hit_box_body,left_pika_hit_box,left_pika_hit_box_body)
    
    font = pygame.font.Font(None, 30)
    score_font = pygame.font.Font(None, 100)

    bg_image = pygame.image.load('bg.jpeg').convert()
    bg_image = pygame.transform.scale(bg_image,(SCREENWIDTH,SCREENHEIGHT))

    net = pygame.image.load('net.jpeg').convert()
    net = pygame.transform.scale(net,(NETWIDTH,NETHEIGHT))

    screen.blit(bg_image,(0,0))
    screen.blit(net,(SCREENWIDTH / 2 - NETWIDTH / 2 ,\
        SCREENHEIGHT - NETHEIGHT))
    pygame.display.flip()

    ball = Player()
    ball.setsurf(BALLRADIUS,BALLRADIUS)
    ball.setrect((SCREENWIDTH / 2,0))
    ball.add_image_ball('ball.png')
    
    player_left = Player()
    player_right = Player()

    player_left.setsurf(PIKAWIDTH,PIKAHEIGHT)
    player_right.setsurf(PIKAWIDTH,PIKAHEIGHT)

    player_left.setrect((PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))
    player_right.setrect((SCREENWIDTH - PIKAWIDTH / 2 ,\
        SCREENHEIGHT - PIKAHEIGHT / 2))

    player_left.add_image('leftpika.png')
    player_right.add_image('rightpika.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
        screen.blit(bg_image,(0,0))
        
        player_right.draw(screen)
        player_left.draw(screen)

        player_left.movewasd()
        player_right.move()

        if player_left.v != 0 or pygame.key.get_pressed()[K_w] or\
                player_left.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            player_left.jumpw()
            player_left.gravity()
            player_left.velocityw()
        if player_right.v != 0 or pygame.key.get_pressed()[K_UP] or\
                player_right.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            player_right.jump()
            player_right.gravity()
            player_right.velocity()
        space.debug_draw(draw_options)

        ball.set_position((ball_body.position[0],ball_body.position[1]))
        
        screen.blit(net,(SCREENWIDTH / 2 - NETWIDTH / 2 ,\
            SCREENHEIGHT - NETHEIGHT))

        right_pika_hit_box_body.position = pymunk.Vec2d(\
            player_right.rect.x -1130, player_right.rect.y -600)
        left_pika_hit_box_body.position = pymunk.Vec2d(\
            player_left.rect.x - 1070, player_left.rect.y -600)

        fps = font.render("FPS:"+str(int(framespersec.get_fps())),\
            True, pygame.Color('white'))#displayfps
        left_score = score_font.render(str(scoreboard[0]),\
            True, pygame.Color('white'))
        right_score = score_font.render(str(scoreboard[1]),\
            True, pygame.Color('white'))
        screen.blit(left_score,(50,50))
        screen.blit(right_score,(SCREENWIDTH-50,50))
        screen.blit(fps, (200, 10))
        
        player_left.smash_from_left(ball_body)
        player_right.smash_from_right(ball_body)

        ball_velocity_limit(MAXBALLVELOCITY,ball_body)
        ball_energy_limit(MINBALLENERGY,ball_body)

        score_point()

        ball.draw(screen)
        pygame.display.update()
        space.step(0.01)
        framespersec.tick(FPS)
    #print(scoreboard)
    pygame.quit()
    sys.exit()   
    
if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.argv[0]))#change working directory
    main()
