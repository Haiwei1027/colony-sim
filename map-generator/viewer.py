from map import Map
import pygame
from pygame import Surface
from pygame import Rect
from pygame.math import Vector2
import time

class Viewer:
    
    def __init__(self:'Viewer', _map:'Map') -> None:
        self.map = _map
        self.surface:Surface = Surface(_map.size)
        self.viewing_area = Rect(0,0,100,100)
        pass
    
    @classmethod
    def load(cls:'Viewer',name:str) -> 'Viewer':
        return Viewer(Map.load(name))
    
    def render(self:'Viewer') -> None:
        for x in range(self.surface.get_width()):
            for y in range(self.surface.get_height()):
                self.draw_block(Vector2(x,y),self.map.grid[x][y])
                pass
            pass    
        pass
    
    def draw_block(self:'Viewer',pos:Vector2, block:dict):
        self.surface.set_at(pos,(pos.x%255,pos.y%255))
        pass
    
    def move_view(self:'Viewer', keys_held:set[int]) -> None:
        speed = 10
        new_rect = self.viewing_area.copy()
        if pygame.K_a in keys_held:
            new_rect.x -= speed
        if pygame.K_d in keys_held:
            new_rect.x += speed
        if pygame.K_w in keys_held:
            new_rect.y -= speed
        if pygame.K_s in keys_held:
            new_rect.y += speed
        if pygame.K_e in keys_held:
            new_rect.w = min(new_rect.w + 10, self.surface.get_width())
            new_rect.h = min(new_rect.h + 10, self.surface.get_height())
        if pygame.K_q in keys_held:
            new_rect.w = max(new_rect.w - 10, 10)
            new_rect.h = max(new_rect.h - 10, 10)
        if self.map.rect_in_bound(new_rect):
            self.viewing_area = new_rect
        pass
    
    def start(self:'Viewer') -> None:
        pygame.init()
        
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 800
        
        screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        
        self.render()
        
        keys_held = set()
        
        active = True
        while active:
            screen.fill((255,255,255))
            
            subsurface = self.surface.subsurface(self.viewing_area)
            subsurface = pygame.transform.scale(subsurface,(SCREEN_WIDTH,SCREEN_HEIGHT))
            
            screen.blit(subsurface,(0,0))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    break
                if event.type == pygame.KEYDOWN:
                    keys_held.add(event.key)
                if event.type == pygame.KEYUP:
                    if event.key in keys_held:
                        keys_held.remove(event.key)
                pass
            
            self.move_view(keys_held)
            
            time.sleep(1/60)
            pass
        pygame.quit()
        pass

if __name__ == "__main__":
    viewer = Viewer.load("base")
    viewer.start()
    pass