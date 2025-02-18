from utility import *
class Map:
    
    def __init__(self:Self, name:str = "base",size:Vector2 = Vector2(1024,1024)):
        self.name = name
        self.size = size
        self.grid = {x:{y:{} for y in range(int(size.y))} for x in range(int(size.x))}
        pass
    
    def save(self:Self) -> None:
        with open(f"output/{self.name}.map","wb+") as file:
            pickle.dump(self, file)
            pass
        pass
    @classmethod
    def load(cls:Self, name:str) -> Self:
        with open(f"output/{name}.map", "rb") as file:
            return pickle.load(file)
    
    def point_in_bound(self:Self, point:Vector2):
        if point.x < 0:
            return False
        if point.y < 0:
            return False
        if point.x >= self.size.x:
            return False
        if point.y >= self.size.y:
            return False
        return True
    
    def rect_in_bound(self:Self, rect:Rect):
        top_left:Vector2 = Vector2(rect.topleft)
        bottom_right:Vector2 = Vector2(rect.bottomright)
        return self.point_in_bound(top_left) and self.point_in_bound(bottom_right)
    
    def foreach(self:Self,func:Callable[[tuple[int,int],dict],None]):
        for x in range(int(self.size.x)):
            for y in range(int(self.size.y)):
                func((x,y), self.grid[x][y])
                pass
            pass
        pass
    
    pass

if __name__ == "__main__":
    map = Map()
    map.save()
    pass