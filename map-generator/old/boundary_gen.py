from utility import *
import random

map_data = load_map("plate0")

width = map_data["settings"]["width"]
height = map_data["settings"]["height"]

for x in range(width):
    for y in range(height):
        id = index(map_data,x,y)
        block = map_data["blocks"][id]
        plate = map_data["plates"][str(block["plate_id"])]
        direction = plate["direction"]
        size = 5
        
        convergence = 0
        divergence = 0
        shear = 0
        
        for dx in range(size):
            dx -= size//2
            for dy in range(size):
                dy -= size //2
                dist = dx**2+dy**2
                if dist == 0:
                    continue
                if not in_map(map_data,x+dx,y+dy):
                    continue
                other_id = index(map_data,x+dx,y+dy)
                
                other_plate_id = str(map_data["blocks"][other_id]["plate_id"])
                other_direction = map_data["plates"][other_plate_id]["direction"]
                
                opposed = max(dot_tuple(direction,neg_tuple(other_direction)),0)
                convergence += dot_tuple((dx,dy), direction) * opposed
                divergence += dot_tuple((dx,dy), other_direction) * opposed
                
                pass
            pass
        
        noise = pnoise2(x / width * 5,y / height * 5, octaves=3)
        
        map_data["blocks"][id]["convergence"] = convergence * (1+noise/3)
        map_data["blocks"][id]["divergence"] = divergence * (1+noise/2)
        
        pass
    pass

iterations = 3
for n in range(iterations):
    for x in range(width):
        for y in range(height):
            id = index(map_data,x,y)
            block = map_data["blocks"][id]
            convergence = block["convergence"]
            
            dx = random.randint(-20,20)
            dy = random.randint(-20,20)
            if dx + dy == 0:
                continue
            if not in_map(map_data,x+dx,y+dy):
                continue
            share_probs = 0
            other_id = index(map_data,x+dx,y+dy)
            other_convergence = map_data["blocks"][other_id]["convergence"]
            if convergence == 0:
                continue
            if other_convergence > convergence:
                continue
            share_probibility = (1-other_convergence/convergence) * ((dx**2+dy**2)/20**2)
            if random.random() < share_probibility:
                map_data["blocks"][index(map_data,x+dx,y+dy)]["convergence"] = convergence / 2

save_map("boundary",map_data)
                