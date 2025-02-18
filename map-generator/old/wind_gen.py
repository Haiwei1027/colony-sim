from utility import *

map_data =  load_map("plate0")

width = map_data["settings"]["width"]
height = map_data["settings"]["height"]

for x in range(width):
    for y in range(height):
        id = index(map_data,x,y)
        block = map_data["blocks"][id]
        latitude = (y-height//2)/(height//2) * 90
        block["pressure"] = math.cos(latitude/180*2*math.pi*2)
        pass
    pass

save_map("wind",map_data)