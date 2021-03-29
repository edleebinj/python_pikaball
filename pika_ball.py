import pygame
import sys
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import time
import random
import math
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()   
        #self.surf = pygame.Surface((PIKAWIDTH,PIKAHEIGHT))
        self.v = 0
    def setsurf(self,*size):
        self.surf = pygame.Surface(size)
    def setrect(self,position):
        self.rect = self.surf.get_rect(center = position)
    def add_image_ball(self,directory):
        self.image = pygame.image.load(directory).convert_alpha()
        self.image = pygame.transform.scale(self.image,(BALLRADIUS,BALLRADIUS))
    def add_image(self,directory):
        self.image = pygame.image.load(directory).convert_alpha()
        self.image = pygame.transform.scale(self.image,(PIKAWIDTH,PIKAHEIGHT))
    #def set_rect(self,position):
    #    self.rect.move(position)
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self):
        if pygame.key.get_pressed()[K_RIGHT]:
            if self.rect.x < SCREENWIDTH - PIKAWIDTH:
                self.rect.move_ip(HORIZONTAL_SPEED,0)
        if pygame.key.get_pressed()[K_LEFT]:
            if self.rect.x > SCREENWIDTH / 2 + NETWIDTH / 2:
                self.rect.move_ip(-HORIZONTAL_SPEED,0)
    def movewasd(self):
        if pygame.key.get_pressed()[K_a]:
            if self.rect.x > 0:
                self.rect.move_ip(-HORIZONTAL_SPEED,0)
        if pygame.key.get_pressed()[K_d]:
            if self.rect.x < SCREENWIDTH / 2 - NETWIDTH / 2 - PIKAWIDTH:
                self.rect.move_ip(HORIZONTAL_SPEED,0)
    def jump(self):
        if pygame.key.get_pressed()[K_UP]:
            if self.rect.y >= SCREENHEIGHT - PIKAHEIGHT:
                self.v = -JUMP_VELOCITY

    def jumpw(self):
        if pygame.key.get_pressed()[K_w]:
            if self.rect.y >= SCREENHEIGHT - PIKAHEIGHT:
                self.v = -JUMP_VELOCITY

    def gravity(self):#down = positive; up = negative
        if self.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            self.v += GRAVITY

        #elif self.rect.y >= SCREENHEIGHT - PIKAHEIGHT and not pygame.key.get_pressed()[K_UP]:
        #    self.v = 0
    
        
    def gravityw(self):#down = positive; up = negative
        if self.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            self.v += GRAVITY
        #elif self.rect.y >= SCREENHEIGHT - PIKAHEIGHT and not pygame.key.get_pressed()[K_w]:
        #    self.v = 0
    
    def velocity(self):
        #if self.rect.y >= SCREENHEIGHT - PIKAHEIGHT and not pygame.key.get_pressed()[K_UP]:
        #    self.v = 0
        if self.v != 0 or self.rect.x != SCREENHEIGHT - PIKAHEIGHT: #and self.rect.y < SCREENHEIGHT - PIKAHEIGHT :
            self.rect.move_ip( 0 , self.v ) 
            if self.rect.y > SCREENHEIGHT - PIKAHEIGHT:
                self.rect.y = SCREENHEIGHT - PIKAHEIGHT

    def velocityw(self):
        #if self.rect.y >= SCREENHEIGHT - PIKAHEIGHT and not pygame.key.get_pressed()[K_w]:
        #    self.v = 0
        if self.v != 0: #and self.rect.y < SCREENHEIGHT - PIKAHEIGHT :
            self.rect.move_ip( 0 , self.v ) 
            if self.rect.y > SCREENHEIGHT - PIKAHEIGHT:
                self.rect.y = SCREENHEIGHT - PIKAHEIGHT
    def gravity_ball(self):#down = positive; up = negative
        if self.rect.y < SCREENHEIGHT - BALLRADIUS:
            self.v += GRAVITY 
    def velocity_ball(self):
        if self.v != 0:
            self.rect.move_ip( 0 , self.v ) 
            if self.rect.y > SCREENHEIGHT - PIKAHEIGHT:
                self.rect.y = SCREENHEIGHT - PIKAHEIGHT
    def set_position(self,*coordinate):
        self.rect.center = coordinate
    def smash_from_left(self,ballbody):
        if pygame.key.get_pressed()[K_z]:
            if pymunk.Vec2d.get_distance(ballbody.position,pymunk.Vec2d(self.rect.x + PIKAWIDTH / 2 , self.rect.y +PIKAHEIGHT / 2)) < BALLRADIUS+30:
                shortsmash = True
                angle = None
                if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_a]:
                    shortsmash = False
                    if pygame.key.get_pressed()[K_w]:
                        angle = 45
                        #smash = True
                        #print('upright')
                    elif pygame.key.get_pressed()[K_s]:
                        angle = 315
                        #smash = True
                        #print('downright')
                    else:
                        angle = 0
                        #print('flat')
                elif pygame.key.get_pressed()[K_s]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_w]:
                        angle = 270
                        #print('down')
                elif pygame.key.get_pressed()[K_w]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_s]:
                        angle = 90
                        #print('up')
                elif shortsmash == True:
                    angle = 0
                    #print('short')
                #print(random.randint(1,5))
                degree_angle = angle * math.pi / 180
                #print(math.cos(degree_angle))
                #print(math.sin(degree_angle))
                #print(random.randint(1,5))
                ballbody.velocity = pymunk.Vec2d(200+1.03 * ballbody.velocity.__abs__() * math.cos(degree_angle),-1 * ballbody.velocity.__abs__() * math.sin(degree_angle))
    def smash_from_right(self,ballbody):
        if pygame.key.get_pressed()[K_RETURN]:
            if pymunk.Vec2d.get_distance(ballbody.position,pymunk.Vec2d(self.rect.x + PIKAWIDTH / 2 , self.rect.y +PIKAHEIGHT / 2)) < BALLRADIUS+30:
                shortsmash = True
                angle = None
                if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_RIGHT]:
                    shortsmash = False
                    if pygame.key.get_pressed()[K_UP]:
                        angle = 135
                        #smash = True
                        #print('upright')
                    elif pygame.key.get_pressed()[K_DOWN]:
                        angle = 225
                        #smash = True
                        #print('downright')
                    else:
                        angle = 180
                        #print('flat')
                elif pygame.key.get_pressed()[K_DOWN]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_UP]:
                        angle = 270
                        #print('down')
                elif pygame.key.get_pressed()[K_UP]:
                    shortsmash = False
                    if not pygame.key.get_pressed()[K_DOWN]:
                        angle = 90
                        #print('up')
                elif shortsmash == True:
                    angle = 180
                    #print('short')
                #print(random.randint(1,5))
                degree_angle = angle * math.pi / 180
                #print(math.cos(degree_angle))
                #print(math.sin(degree_angle))
                #print(random.randint(1,5))
                ballbody.velocity = pymunk.Vec2d(-200+1.03 * ballbody.velocity.__abs__() * math.cos(degree_angle),-1 * ballbody.velocity.__abs__() * math.sin(degree_angle))
                
pymunk.CollisionHandler
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
    
    def ball_spawn_left():
        ball_body.position = ( 60 , 60 )
        ball_body.velocity = (0,0)


    def ball_spawn_right():
        ball_body.position = ( SCREENWIDTH - 60 , 60 )
        ball_body.velocity = (0,0)



    def score_point():
        if ball_body.position.y >= SCREENHEIGHT - BALLRADIUS / 2 + 10:
            if ball_body.position.x > SCREENWIDTH / 2:
                scoreboard[0] += 1
                ball_spawn_right()
                player_left.setrect((PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))
                player_right.setrect((SCREENWIDTH - PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))
                player_left.v = 0
                player_right.v = 0
                
            elif ball_body.position.x <= SCREENWIDTH / 2:
                scoreboard[1] += 1
                ball_spawn_left()
                player_left.setrect((PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))
                player_right.setrect((SCREENWIDTH - PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))
                player_left.v = 0
                player_right.v = 0
            time.sleep(0.3)
    pygame.init()
    FPS = 130
    framespersec = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pygame.display.set_caption("pikaball")
    running = True

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = 0, 800
    #attach a segment to pika as hitbox
    pts = [(-100,-100),(1350,-100),(1350,850),(-100,850)]
    segment = pymunk.Segment(space.static_body,(SCREENWIDTH / 2 ,(SCREENHEIGHT - NETHEIGHT)*1.03),(SCREENWIDTH / 2 , SCREENHEIGHT), NETWIDTH / 2)#網子
    segment.elasticity = 1
    segment.color = (0,0,0,0)
    for i in range(4):
        seg = pymunk.Segment(space.static_body, pts[i], pts[(i+1)%4], 100)
        seg.elasticity = 1
        seg.color = (0,0,0,0)#(kine)metic body type is used for pika
        space.add(seg)
    right_pika_hit_box_body = pymunk.Body(body_type = 1)
    right_pika_hit_box = pymunk.Segment(right_pika_hit_box_body,(SCREENWIDTH - PIKAWIDTH / 2 , SCREENHEIGHT - PIKAWIDTH / 2.6),(SCREENWIDTH - PIKAWIDTH / 2, SCREENHEIGHT*1.1 - PIKAHEIGHT*1.1),PIKAWIDTH / 2.6)
    right_pika_hit_box.elasticity = 0.9
    right_pika_hit_box.color = (0,0,0,256)
    
    left_pika_hit_box_body = pymunk.Body(body_type = 1)
    left_pika_hit_box = pymunk.Segment(left_pika_hit_box_body,(SCREENWIDTH - PIKAWIDTH / 2 , SCREENHEIGHT - PIKAWIDTH / 2.6),(SCREENWIDTH - PIKAWIDTH / 2, SCREENHEIGHT*1.1 - PIKAHEIGHT*1.1),PIKAWIDTH / 2.6)
    left_pika_hit_box.elasticity = 0.9
    left_pika_hit_box.color = (0,0,0,256)

    ball_body = pymunk.Body(mass = 10000,moment = 0.0000001)
    ball_body.position = (SCREENWIDTH / 2 , 60 )
    circle = pymunk.Circle(ball_body, radius = 50)
    circle.elasticity = 1
    space.add(ball_body, circle,segment,right_pika_hit_box,right_pika_hit_box_body,left_pika_hit_box,left_pika_hit_box_body)
    


    font = pygame.font.Font(None, 30)
    score_font = pygame.font.Font(None, 100)

    #screen.fill((0,0,0))
    bg_image = pygame.image.load('/Users/mac/Desktop/pythonlearning/pikaball/bg.jpeg').convert()
    bg_image = pygame.transform.scale(bg_image,(SCREENWIDTH,SCREENHEIGHT))

    net = pygame.image.load('/Users/mac/Desktop/pythonlearning/pikaball/net.jpeg').convert()
    net = pygame.transform.scale(net,(NETWIDTH,NETHEIGHT))

    screen.blit(bg_image,(0,0))
    screen.blit(net,(SCREENWIDTH / 2 - NETWIDTH / 2 , SCREENHEIGHT - NETHEIGHT))
    pygame.display.flip()#removable?

    ball = Player()
    ball.setsurf(BALLRADIUS,BALLRADIUS)
    ball.setrect((SCREENWIDTH / 2,0))
    ball.add_image_ball('/Users/mac/Desktop/pythonlearning/pikaball/ball.png')
    

    player_left = Player()
    player_right = Player()

    player_left.setsurf(PIKAWIDTH,PIKAHEIGHT)
    player_right.setsurf(PIKAWIDTH,PIKAHEIGHT)

    player_left.setrect((PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))
    player_right.setrect((SCREENWIDTH - PIKAWIDTH / 2 , SCREENHEIGHT - PIKAHEIGHT / 2))

    player_left.add_image('/Users/mac/Desktop/pythonlearning/pikaball/leftpika.png')
    player_right.add_image('/Users/mac/Desktop/pythonlearning/pikaball/rightpika.png')

    #player_left.rect.move_ip((100,100))

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
        #ball.draw(screen)

        player_left.movewasd()
        player_right.move()
        #ball.gravity_ball()
        #ball.velocity_ball()
        if player_left.v != 0 or pygame.key.get_pressed()[K_w] or player_left.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            player_left.jumpw()
            player_left.gravityw()
            player_left.velocityw()
        if player_right.v != 0 or pygame.key.get_pressed()[K_UP] or player_right.rect.y < SCREENHEIGHT - PIKAHEIGHT:
            player_right.jump()
            player_right.gravity()
            player_right.velocity()
        space.debug_draw(draw_options)
        #print(body.position[0])
        ball.set_position((ball_body.position[0],ball_body.position[1]))
        
        screen.blit(net,(SCREENWIDTH / 2 - NETWIDTH / 2 , SCREENHEIGHT - NETHEIGHT))
        #print(player_left.v) 

        #print(player_right.rect.x)

        right_pika_hit_box_body.position = pymunk.Vec2d(player_right.rect.x -1130, player_right.rect.y -600)
        left_pika_hit_box_body.position = pymunk.Vec2d(player_left.rect.x - 1070, player_left.rect.y -600)
        #print (left_pika_hit_box_body.position)
        fps = font.render("FPS:"+str(int(framespersec.get_fps())), True, pygame.Color('white'))#displayfps
        left_score = score_font.render(str(scoreboard[0]),True, pygame.Color('white'))
        right_score = score_font.render(str(scoreboard[1]), True, pygame.Color('white'))
        screen.blit(left_score,(50,50))
        screen.blit(right_score,(SCREENWIDTH-50,50))
        screen.blit(fps, (200, 10))
        
        #print(body.angle)
        
        player_left.smash_from_left(ball_body)
        player_right.smash_from_right(ball_body)

        #print(pymunk.Vec2d.get_distance(ball_body.position,pymunk.Vec2d(player_left.rect.x + PIKAWIDTH / 2,player_left.rect.y +PIKAHEIGHT / 2)))


        score_point()

        # print(ball_body.position[0],ball_body.position[1])
        
        ball.draw(screen)
        pygame.display.update()
        space.step(0.01)
        framespersec.tick(FPS)
    print(scoreboard)
    pygame.quit()
    sys.exit()   
    
    
if __name__ == '__main__':
    main()