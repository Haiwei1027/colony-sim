from utility import *
from map import Map

if __name__ != "__main__":
    quit()
    exit()

_map:'Map' = Map.load("base")
_map.name = "plate"

width,height = vec_tuple(_map.size)

seed = 53631
size_scaler = (width//800) * (height//800)

nodes = []
for _ in range(15 * size_scaler):
    nodes.append(Vector2(random.randint(0,width), random.randint(0,height)))
    pass

def noise_vector(x, y, t, spatial_scale=600,temporal_scale=15, octaves=3):
    noise_value = snoise3(x/spatial_scale, y/spatial_scale, t/temporal_scale, octaves=octaves)
    angle = noise_value * 2 * math.pi
    return Vector2(1,0).rotate_rad(angle)

def node_dists(node:Vector2,nodes:list[Vector2],noise_factor:int=200):
    dist_table:list[int] = []
    for i,other in enumerate(nodes):
        x,y = node
        delta = node - other
        
        dist = delta.magnitude()
        
        noise = 0
        if noise_factor != 0:
            noise = (pnoise2(delta.x / width * 10 + seed,delta.y / height * 10 + seed,octaves=2)+1)/2
        dist += noise * noise_factor
        
        dist_table.append((i,dist))
        pass
    return dist_table

# redistribute plate nodes

iterations = 5
# how strongly do plates get pushed from border
center_factor = 15 * size_scaler
# how much the nodes repel each other
repel_factor = 20 * size_scaler
# [0,1]
brownian_factor = 40 * size_scaler
# how much the "mantle" vector field affects the node
drift_factor = 40 * size_scaler
_map.plates = {}
for n in range(iterations):
    _map.plates[n] = []
    print(f"n:{n}")
    for i,node in enumerate(nodes):
        node:Vector2
        drift_force = noise_vector(node.x,node.y,n)
        # drift
        drift_force *= drift_factor
        brownian_force = Vector2(1,0).rotate(random.randint(0,360)) * brownian_factor
        center = _map.size / 2
        center_force = (center - node).normalize() * center_factor
        dist_table = node_dists(node, [n for n in nodes if n != node], noise_factor=0)
        dist_table.sort(key=lambda x:x[1])
        nearest_node:Vector2 = nodes[dist_table[1][0]]
        repel_force = Vector2(0,0)
        if (node - nearest_node).magnitude() != 0:
            repel_force = (node - nearest_node).normalize() * repel_factor
        
        node += drift_force
        node += brownian_force
        node += center_force
        node += repel_force
        
        _map.plates[n].append({"center":node,"direction":drift_force})

    # assign block to the nearest plate node
    def assign_plate(pos, block):
        dist_table = node_dists(Vector2(pos), nodes, noise_factor=100)
        
        dist_table.sort(key=lambda x:x[1])
        if "plate_id" not in block:
            block["plate_id"] = {}
        block["plate_id"][n] = dist_table[0][0]
        
        pass
    _map.foreach(assign_plate)
            
    pass
# save map data
_map.save()
    
