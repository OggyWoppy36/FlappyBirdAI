import pygame
from settings import GRAV,BIRD_SIZE,BIRD_COL,JUMP_STRENGTH,HEIGHT,PIPE_SPEED,START_X,START_Y,WIDTH
from neuralnet import NeuralNetwork

def clamp(a, low, high):
    return max(low, min(a, high))


class Bird:
    def __init__(self,x=START_X,y=START_Y, brain=None):
        self.x = x
        self.y = y
        self.velY = 0
        self.r = BIRD_SIZE
        self.col = BIRD_COL
        self.dead = False

        self.fitness = 0
        self.score = 0

        if (brain):
            self.brain = brain
        else:
            self.brain = NeuralNetwork()
        
    def think(self, target_pipe):
        if not target_pipe or self.dead:
            return

        pipe_front = target_pipe.x - target_pipe.w
        pipe_dist = max(0, pipe_front - self.x)
        norm_dist = pipe_dist / (WIDTH - START_X)
        inputs = [
            self.y / HEIGHT,
            (self.y-target_pipe.y) / HEIGHT,
            self.velY / (JUMP_STRENGTH*2.0),
            norm_dist,
        ]

        output = self.brain.predict(inputs)
        if (output > 0.5):
            self.jump()



    def update(self, target_pipe=None):
        if (self.dead):
            self.x -= PIPE_SPEED
            return
        self.fitness += 1

        if target_pipe:
            dist = abs(self.y - target_pipe.y)
            self.fitness += max(0, (100 - dist)/100)
        self.velY += GRAV
        self.y += self.velY

    def show(self, screen):
        pygame.draw.circle(screen,"black",(self.x,self.y),self.r)
        pygame.draw.circle(screen,self.col,(self.x,self.y),self.r-7.5)
        

    def jump(self):
        self.velY = -JUMP_STRENGTH

    def _check_collision(self,pipe):
        if (pipe.right < self.x - self.r or pipe.left > self.x + self.r):
            return False
        closeX = clamp(self.x, pipe.left, pipe.right)
        closeY = clamp(self.y, pipe.top, pipe.bottom)
        dx = self.x - closeX
        dy = self.y - closeY
        distSq = dx*dx + dy*dy
        return (distSq < self.r * self.r)

    def check_lose(self,pipes):
        if (self.y + self.r >= HEIGHT or self.y - self.r <= 0):
            self.dead = True
            return True
        for pipe in pipes:
            p = pipe.top
            if (self.y > pipe.y):
                p = pipe.bottom
            if (self._check_collision(p)):
                self.dead = True
                return True
        return False