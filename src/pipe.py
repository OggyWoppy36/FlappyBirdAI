import pygame
import random as rand
from settings import PIPE_WIDTH,PIPE_GAP as GAP,WIDTH,HEIGHT,PIPE_SPEED as SPEED,PIPE_RANGE as RANGE

class Pipe:
    def __init__(self):
        self.x = WIDTH + 200
        self.y = RANGE[0] + rand.random()*(RANGE[1]-RANGE[0])
        self.w = PIPE_WIDTH
        self.top = pygame.Rect(self.x-self.w,0,self.w,self.y-GAP/2)
        self.bottom = pygame.Rect(self.x-self.w,self.y+GAP/2,self.w,HEIGHT-(self.y+GAP/2))

        self.bottom_image = self._make_pipe_stamp(self.bottom.width, self.bottom.height)
        self.top_image = pygame.transform.flip(
            self._make_pipe_stamp(self.top.width, self.top.height), False, True
        )

        self.scored = False


    def show(self, screen):
        #pygame.draw.rect(screen, "green", self.top)
        #pygame.draw.rect(screen, "green", self.bottom)
        screen.blit(self.top_image, self.top.topleft)
        screen.blit(self.bottom_image, self.bottom.topleft)

    def update(self):
        self.x -= SPEED
        self.top.move_ip(-SPEED,0)
        self.bottom.move_ip(-SPEED,0)

    def _make_pipe_stamp(self, width, height):
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        base = (0,200,0)
        light = (67,250,67)
        dark = (0,150,0)

        pygame.draw.rect(surf,dark,(5,0,width-10,height))
        pygame.draw.rect(surf,base,(20,0,width-25,height-0))
        pygame.draw.rect(surf,light, (-5, 0, width+10, 20))
        return surf

    def score(self):
        self.scored = True