import tingbot
from tingbot import *
from collections import namedtuple
import time

class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'Vector({self.x}, {self.y})'.format(self=self)
    
    def as_tuple(self):
        return (self.x, self.y)

class Paddle(object):
    def __init__(self, position):
        self.position = position
        self.size = Vector(5, 60)
        self.miss = False
    
    def ball_collides(self, ball_position, ball_velocity):
        # is the ball vertically aligned with the paddle?
        top_y = self.position.y - self.size.y/2
        bottom_y = self.position.y + self.size.y/2
        
        if top_y < ball_position.y < bottom_y:
            # does the ball pass through the paddle?
            ball_is_left_of_paddle_before = ball_position.x < self.position.x
            ball_x_after = ball_position.x + ball_velocity.x
            ball_is_left_of_paddle_after = ball_x_after < self.position.x
        
            if ball_is_left_of_paddle_before != ball_is_left_of_paddle_after:
                # collision!
                return True
        
        return False
    
    def react_to_ball(self, ball_position, ball_velocity):
        ball_is_left_of_paddle = ball_position.x < self.position.x
        ball_is_moving_right = ball_velocity.x < 0
        
        if ball_is_left_of_paddle == ball_is_moving_right:
            # do nothing, as it's not heading towards me
            return
        
        if self.miss:
            # do nothing, as I'm supposed to let this one through
            return
                
        delta = ball_position.y - self.position.y
        
        if delta > 3:
            delta = 3
        if delta < -3:
            delta = -3
        
        self.position.y += delta

ball_position = Vector(160, 120)
ball_velocity = Vector(2.5, 2.5)

left_paddle = Paddle(Vector(10, 120))
right_paddle = Paddle(Vector(310, 120))

paddles = (left_paddle, right_paddle)

left_score = time.localtime().tm_hour
right_score = time.localtime().tm_min

def loop():
    global left_score, right_score
    
    minutes = time.localtime().tm_hour
    seconds = time.localtime().tm_min
    
    if left_score != minutes:
        left_paddle.miss = True
    else:
        left_paddle.miss = False
    
    if right_score != seconds:
        right_paddle.miss = True
    else:
        right_paddle.miss = False
    
    if ball_position.y < 0 or ball_position.y > 240:
        ball_velocity.y = -ball_velocity.y

    if any(p.ball_collides(ball_position, ball_velocity) for p in paddles):
        ball_velocity.x = -ball_velocity.x        
    
    if ball_position.x < 0:
        left_score += 1
        if left_score > 23:
            left_score = 0
            
        ball_position.x = 160
        ball_position.y = 120
    if ball_position.x > 320:
        right_score += 1
        if right_score > 59:
            right_score = 0
            
        ball_position.x = 160
        ball_position.y = 120

    ball_position.x += ball_velocity.x
    ball_position.y += ball_velocity.y
    
    screen.fill(
        color='black'
    )
    
    screen.text(
        left_score,
        xy=(150, 20),
        font_size=40,
        color='white',
        align='right',
    )
    screen.text(
        right_score,
        xy=(170, 20),
        font_size=40,
        color='white',
        align='left',
    )
    
    screen.rectangle(
        xy=ball_position.as_tuple(), 
        size=(5, 5),
        color='white'
    )
    
    for paddle in paddles:
        screen.rectangle(
            xy=paddle.position.as_tuple(),
            size=paddle.size.as_tuple(),
            color='white',
        )
    
    for paddle in paddles:
        paddle.react_to_ball(ball_position, ball_velocity)
    
# run the app
tingbot.run(loop)
