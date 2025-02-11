# this file will be responsible for plate map

import random
from noise import pnoise2

map_data = {"settings":{},"blocks":{},"plates":{}}

# populate with cells

width = 800
height = 800

map_data["settings"]["width"] = width
map_data["settings"]["height"]  = height

from utility import *

for x in range(width):
    for y in range(height):
        id = index(map_data,x,y)
        map_data["blocks"][id] = {"plate_id":-1}
        pass
    pass

# add random plate nodes

nodes = []
for i in range(15):
    nodes.append((random.randint(0,width),
                  random.randint(0,height)))
    pass

def noise_vector(x, y, scale=200.0, octaves=2):
        noise_value = pnoise2(x / scale, y / scale, octaves=octaves)
    
        angle = noise_value * 2 * math.pi

        vector = angle_vector(angle)
        
        return vector

def node_dists(node,nodes,noise_factor=200):
    dist_table = []
    for i,nodek in enumerate(nodes):
        x,y = node
        dist = distance((x,y),nodek)
        
        noise = (pnoise2((x-nodek[0]) / width * 10,(y-nodek[1]) / height * 10,octaves=4)+1)/2
        
        dist += noise * noise_factor
        
        dist_table.append((i,dist))
        pass
    return dist_table

# redistribute plate nodes

iterations = 10
# how strongly do plates get pushed from border
center_factor = 15
# how much the nodes repel each other
repel_factor = 20
# [0,1]
brownian_factor = 40
# how much the "mantle" vector field affects the node
drift_factor = 40

for n in range(iterations):
    
    print(f"n:{n}")
    for i,node in enumerate(nodes):
        drift_dir = noise_vector(node[0],node[1])
        force = (0,0)
        # drift
        drift_force = mut_tuple(drift_dir, drift_factor)
        brownian_force = mut_tuple(angle_vector(random.random()*2*math.pi), brownian_factor)
        center = (width//2,height//2)
        center_force = mut_tuple(norm_tuple(sub_tuple(center,node)),center_factor)
        dist_table = node_dists(node, [n for n in nodes if n != node], noise_factor=0)
        dist_table.sort(key=lambda x:x[1])
        nearest_node = nodes[dist_table[0][0]]
        repel_force = mut_tuple(norm_tuple(sub_tuple(node,nearest_node)),repel_factor)
        
        force = add_tuple(force,drift_force)
        force = add_tuple(force,brownian_force)
        force = add_tuple(force,center_force)
        force = add_tuple(force,repel_force)
        
        #node = add_tuple(node,mut_tuple(noise_vector(node[0],node[1]),drift_factor))
        # brownian motion
        #node = lerp(node,(random.randint(0,width-1),random.randint(0,height-1)), random_factor)
        # repell from border
        #if border_dist(map_data,node[0],node[1]) < 100:
            #node = lerp(node,(width//2,height//2), center_factor)
        # repell from other
        #for j,other in enumerate(nodes):
            #if i == j:
                #continue
            #node = lerp(node,other,repel_factor/distance(node,other))
        node = add_tuple(node,force)
        nodes[i] = node
        map_data["plates"][i] = {"center":node,"direction":drift_dir}

    # assign block to the nearest plate node

    for x in range(width):
        for y in range(height):
            id = index(map_data,x,y)
            dist_table = node_dists((x,y), nodes, noise_factor=200)
            
            dist_table.sort(key=lambda x:x[1])
            
            map_data["blocks"][id]["plate_id"] = dist_table[0][0]
            
            pass
        pass
    
    # save map data

    save_map(f"plate{n}",map_data)