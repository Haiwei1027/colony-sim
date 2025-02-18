from pygame.math import Vector2
from pygame.rect import Rect
from utility import *
class Map:
    
    def __init__(self : 'Map', name:str = "base",size:Vector2 = Vector2(1024,1024)):
        self.name = name
        self.size = size
        self.grid = {x:{y:{} for y in range(int(size.y))} for x in range(int(size.x))}
        pass
    
    def to_dict(self:'Map') -> dict:
        return {
            "name":self.name,
            "size":(self.size.x,self.size.y),
            "grid":self.grid
        }
    @classmethod
    def from_dict(cls:'Map', data:dict):
        map = Map(data["name"],Vector2(data["size"]))
        map.grid = data["grid"]
        return map
    
    def save(self:'Map') -> None:
        save_map(self.to_dict(),self.name)
        pass
    @classmethod
    def load(cls:'Map', name:str) -> 'Map':
        return Map.from_dict(load_map(name))
    
    def point_in_bound(self:'Map', point:Vector2):
        if point.x < 0:
            return False
        if point.y < 0:
            return False
        if point.x >= self.size.x:
            return False
        if point.y >= self.size.y:
            return False
        return True
    
    def rect_in_bound(self:'Map', rect:Rect):
        top_left:Vector2 = Vector2(rect.topleft)
        bottom_right:Vector2 = Vector2(rect.bottomright)
        return self.point_in_bound(top_left) and self.point_in_bound(bottom_right)
    pass

if __name__ == "__main__":
    map = Map()
    map.save()
    pass