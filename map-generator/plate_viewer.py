from utility import *
from viewer import Viewer
import hashlib

def plate_color(number):
    hash_object = hashlib.sha256(str(number).encode()).hexdigest()[:6]
    rgb = [int(hash_object[i:i+2], 16) for i in (0, 2, 4)]
    max_val = max(rgb)
    return tuple(min(255, int(c * 255 / max_val)) for c in rgb)

class PlateViewer(Viewer):
    
    def __init__(self, _map):
        super().__init__(_map)
        self.step = 0
    
    def draw_block(self:Self,pos:tuple[int,int], block:dict):
        x,y = pos
        self.surface.set_at(pos, plate_color(block["plate_id"][self.step]))
    
    def handle_key(self, key):
        super().handle_key(key)
        prev_step = self.step
        if pygame.K_RIGHT == key:
            self.step += 1
        if pygame.K_LEFT == key:
            self.step -= 1
        self.step = clamp(self.step,0,len(self.map.grid[0][0]["plate_id"])-1)
        if self.step != prev_step:
            self.render()
            print(self.step)
    
    pass

if __name__ == "__main__":
    viewer = PlateViewer.load("plate")
    viewer.start()
    pass