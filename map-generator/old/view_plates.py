import pygame

from utility import *

import hashlib

def plate_color(number):
    hash_object = hashlib.sha256(str(number).encode()).hexdigest()[:6]
    rgb = [int(hash_object[i:i+2], 16) for i in (0, 2, 4)]
    max_val = max(rgb)
    return tuple(min(255, int(c * 255 / max_val)) for c in rgb)

def render_plate_boundary(data,filename):
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
            pygame.draw.rect(screen,plate_color(block["plate_id"]), (x,y,1,1))
    
    # draw plate drift vectors
    
    for plate_id in data["plates"]:
        plate = data["plates"][plate_id]
        pygame.draw.circle(screen,(0,0,0),plate["center"],10)
        pygame.draw.line(screen,pygame.Color(0,0,0),plate["center"],
                         lerp(plate["center"], add_tuple(plate["center"],plate["direction"]),100))
    
    pygame.display.update()
    
    active = 1
    # while active:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             active = 0
    #             break
    #         pass
    #     pass
    pygame.image.save(screen, filename+'.png')
    pygame.quit()
    pass

def render_plate(data,filename):
    pygame.init()
    
    width = data["settings"]["width"]
    height = data["settings"]["height"]
    
    screen = pygame.display.set_mode((width,height))
    
    # draw blocks coloured by history
    screen.fill(pygame.Color(0,0,200))
    for x in range(width):
        for y in range(height):
            id = index(data,x,y)
            block = data["blocks"][id]
            if len(set(block["history"])) < 3:
                pygame.draw.rect(screen,pygame.Color(0,0,len(set(block["history"]))*20), (x,y,1,1))
            else:
                pygame.draw.rect(screen,pygame.Color(0,len(set(block["history"]))*20,0), (x,y,1,1))
    
    # draw plate drift vectors
    for plate_id in data["plates"]:
        plate = data["plates"][plate_id]
        pygame.draw.circle(screen,(0,0,0),plate["center"],10)
        pygame.draw.line(screen,pygame.Color(0,0,0),plate["center"],
                         lerp(plate["center"], add_tuple(plate["center"],plate["direction"]),100))
    
    pygame.display.update()
    active = 1
    # while active:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             active = 0
    #             break
    #         pass
    #     pass
    pygame.image.save(screen, filename+'.png')
    pygame.quit()
    pass

# main view loop
base_map = load_map(f"plate{0}")

for id in base_map["blocks"]:
    base_map["blocks"][id]["history"] = []

for n in range(1,10):
    new = load_map(f"plate{n}")
    for id in base_map["blocks"]:
        base_map["blocks"][id]["history"].append(base_map["blocks"][id]["plate_id"])
        base_map["blocks"][id]["plate_id"] = new["blocks"][id]["plate_id"]
    render_plate(base_map,f"plate{n}")
render_plate(base_map,f"plate_history")
save_map(f"changemap", base_map)