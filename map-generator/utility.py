from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect

from typing import Self
from typing import Callable
import pickle