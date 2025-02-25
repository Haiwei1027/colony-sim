from utility import *

import pygame

map_data = load_map("wind")

width = map_data["settings"]["width"]
height = map_data["settings"]["height"]

pygame.init()

screen = pygame.display.set_mode((width,height))

@map_block
def draw_pressure(pos,block):
    x,y = pos
    color = (max(block["pressure"]*200,0),0,max(block["pressure"]*-200,0))
    pygame.draw.rect(screen,color,(x,y,1,1))
    pass

draw_pressure(map_data)
active = 1
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = 0
    pygame.display.update()