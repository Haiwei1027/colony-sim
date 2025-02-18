from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect

from typing import Self
from typing import Callable
import pickle
import random
from noise import snoise3,pnoise3
import math
from multiprocessing import Process

def vec_tuple(vector:Vector2) -> tuple[int,int]:
    return (int(vector.x),int(vector.y))

def clamp(x,low,high):
    return max(min(x,high), low)