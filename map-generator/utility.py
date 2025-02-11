from noise import pnoise2
import math

def lerp(a,b,t):
    return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)

def index(map_data, x,y):
    return str(y * map_data["settings"]["width"] + x)

def deindex(map_data,id):
    id = int(id)
    x = id % map_data["settings"]["width"]
    y = id // map_data["settings"]["width"]
    return (x,y)

def add_tuple(a,b):
    return (a[0]+b[0],a[1]+b[1])

import json

def save_map(filename, map_data):
    with open(f"{filename}.map","w+") as file:
        file.write(json.dumps(map_data))
        pass
    pass

def load_map(filename):
    map_data = {}
    with open(f"{filename}.map","r") as file:
        map_data = json.loads(file.read())
        pass
    return map_data

def dot_tuple(a,b):
    return (a[0]*b[0]+a[1]+b[1])

def neg_tuple(a):
    return (-a[0],-a[1])

def sub_tuple(a,b):
    return add_tuple(a,neg_tuple(b))

def mut_tuple(a,t):
    return (a[0]*t,a[1]*t)

def in_map(map_data,x,y):
    return x>=0 and x < map_data["settings"]["width"] and y >=0 and y < map_data["settings"]["height"]

def clamp(x,low,high):
    return max(min(x,high), low)

def border_dist(map_data,x,y):
    if not in_map(map_data,x,y):
        return -1
    dist = min(x,map_data["settings"]["width"] - x,y,map_data["settings"]["width"] - y)
    return dist

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def angle_vector(angle):
    return (math.cos(angle),math.sin(angle))

def magnitude_tuple(a):
    return math.sqrt(a[0]**2+a[1]**2)

def norm_tuple(a):
    mag = magnitude_tuple(a)
    if mag == 0:
        return a
    return mut_tuple(a,1/mag)

def map_block(func):
    
    def wrapper(map_data):
        width = map_data["settings"]["width"]
        height = map_data["settings"]["height"]
        for x in range(width):
            for y in range(height):
                id = index(map_data,x,y)
                block = map_data["blocks"][id]
                func((x,y),block)
                pass
            pass
        pass
    
    return wrapper
    