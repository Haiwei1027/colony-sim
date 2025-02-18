from utility import *
from map import Map

if __name__ != "__main__":
    quit()
    exit()

_map:'Map' = Map.load("base")
_map.name = "plate"

width,height = vec_tuple(_map.size)

seed = 536312
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
        
        noise = (pnoise3(delta.x / width * 10,delta.y / height * 10, seed,octaves=4)+1)/2
        
        dist += noise * noise_factor
        
        dist_table.append((i,dist))
        pass
    return dist_table

# redistribute plate nodes

iterations = 10
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
        force = Vector2(0,0)
        # drift
        drift_force *= drift_factor
        brownian_force = Vector2(1,0).rotate(random.randint(0,360)) * brownian_factor
        center = _map.size / 2
        center_force = (center - node).normalize() * center_factor
        dist_table = node_dists(node, [n for n in nodes if n != node], noise_factor=0)
        dist_table.sort(key=lambda x:x[1])
        nearest_node:Vector2 = nodes[dist_table[1][0]]
        repel_force = (node - nearest_node).normalize() * repel_factor
        
        force += drift_force
        force += brownian_force
        force += center_force
        force += repel_force
        
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
        node = node + force
        nodes[i] = node
        _map.plates[n].append({"center":node,"direction":drift_force})

    # assign block to the nearest plate node
        def assign_plate(pos, block):
            dist_table = node_dists(Vector2(pos), nodes, noise_factor=200)
            
            dist_table.sort(key=lambda x:x[1])
            if "plate_id" not in block:
                block["plate_id"] = {}
            block["plate_id"][n] = dist_table[0][0]
            
            pass
        _map.foreach(assign_plate)
            
        pass
    
    # save map data
_map.save()
    
