import pygame

from utility import *

map_data = load_map("boundary")

import hashlib

def plate_color(number):
    hash_object = hashlib.sha256(str(number).encode()).hexdigest()[:6]
    rgb = [int(hash_object[i:i+2], 16) for i in (0, 2, 4)]
    max_val = max(rgb)
    return tuple(min(255, int(c * 255 / max_val)) for c in rgb)

def render_boundary(data):
    pygame.init()
    
    width = data["settings"]["width"]
    height = data["settings"]["height"]
    
    screen = pygame.display.set_mode((width,height))
    
    # draw blocks coloured by plate id
    screen.fill(pygame.Color(0,0,0))
    
    for x in range(width):
        for y in range(height):
            id = index(data,x,y)
            block = data["blocks"][id]
            convergence = int(clamp(block["convergence"]*10,0,255))
            divergence = int(clamp(block["divergence"]*10,0,255))
            pygame.draw.rect(screen,pygame.Color(convergence,0,divergence), (x,y,1,1))
    
    # draw plate drift vectors
    
    for plate_id in data["plates"]:
        plate = data["plates"][plate_id]
        pygame.draw.line(screen,pygame.Color(0,0,0),plate["center"],
                         lerp(plate["center"], add_tuple(plate["center"],plate["direction"]),100))
    
    pygame.display.update()
    
    active = 1
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = 0
                break
            pass
        pass
    pygame.quit()
    pass

render_boundary(map_data)