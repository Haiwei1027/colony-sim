import noise
import numpy as np

from utility import *
from PIL import Image
import random


def gen_noise_map(width, height, scale, octaves, persistence, lacunarity, seed=random.random()):

    noise_mapa = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            noise_val = noise.pnoise3(x/scale, y/scale, seed*1000, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            noise_mapa[x][y] = noise_val
    return (noise_mapa + 1) / 2



# Given a completed .map file, where every block stores its history,
# returns recommended rock types as a bitmap

filename = "changemap"
basemap = load_map(filename)
width = basemap["settings"]["width"]
height = basemap["settings"]["height"]
history_map = {block_id: data["history"] for block_id, data in basemap["blocks"].items()}

# get the age range from any block
age_range = len(history_map["0"])

def get_age(history):
    last_value = history[-1]
    for age in range(len(history)-2, -1, -1):
        if history[age] != last_value:
            return len(history) - 1 - age
    return len(history)

age_map = {block_id: get_age(history) for block_id, history in history_map.items()}

# render age map

def render_age_map(age_map, basemap, filename):
    width = basemap["settings"]["width"]
    height = basemap["settings"]["height"]

    img = Image.new("RGB", (width, height))
    pixels = img.load()

    max_age = max(age_map.values()) or 1

    # draa
    for x in range(width):
        for y in range(height):
            block_id = index(basemap, x, y)
            age = age_map.get(block_id, 0)

            intensity = int((age / max_age) * 255)
            pixels[x, y] = (intensity, intensity, intensity)

    img.save(f"{filename}.png")
    print(f"Saved age map as {filename}.png")

# render_age_map(age_map, basemap, "age_map")
ROCK_COLORS = {
    0: (243, 67, 52), # Igneous red
    1: (147, 95, 161), # Metamorphic purple
    2: (162, 196, 110), # Cenozic green
    3: (189, 227, 246), # mesozoic cyan
    4: (255, 195, 19), # Late Palaeozoic orange
    5: (146, 127, 85), # Early Palaeozoic brown
    6: (254, 209, 167) # Proterozoic peach
}
def gen_binary_blop_map(seed = random.random()):
    big_noise = gen_noise_map(width, height, 50, 3, 0.2, 2)
    small_noise = gen_noise_map(width, height, 5, 20, 0.3, 2)

    mask = (big_noise > 0.55).astype(float)
    combined_noise = small_noise * mask

    binary_blobs = (combined_noise > 0.55)
    return binary_blobs

def classify_rock(age_map, age_range, basemap):
    # type boundaries
    # as in, rock aged up to this value is how old it is
    # for categorising and creating rock types
    new_rock_range = int(age_range * 0.15)
    rock_range_recent = int(age_range * 0.35)
    rock_range_semirecent = int(age_range * 0.4)
    rock_range_aged = int(age_range * 0.6)
    rock_range_old = int(age_range * 0.8)
    # anything else is ancient

    width = basemap["settings"]["width"]
    height = basemap["settings"]["height"]
    seed = random.random() # replace with basemap["settings"]["seed"] when implemented

    rock_type_map = {}

    # noise for rock sprinkling
    binary_blobs = gen_binary_blop_map(seed)
    # wider noise map for more generic replacement
    general_noise = gen_noise_map(width, height, 30, 8, 0.3, 2)

    for x in range(width):
        for y in range(height):
            block_id = index(basemap, x, y)
            age = age_map.get(block_id)

            if age <= new_rock_range:
                rock_type_map[block_id] = 0 if (binary_blobs[x,y] == False) else 1
            elif age <= rock_range_recent:
                rock_type_map[block_id] = 1 if (binary_blobs[x,y] == False) else 2
            elif age <= rock_range_semirecent:
                rock_type_map[block_id] = 2 if (general_noise[x,y] < 0.5) else 3
            elif age <= rock_range_aged:
                if general_noise[x,y] < 0.6:
                    rock_type_map[block_id] = 4
                elif not binary_blobs[x, y]:  # Independent check
                    rock_type_map[block_id] = 5
                else:  # Default for aged rocks when neither condition is met
                    rock_type_map[block_id] = 0
            elif age <= rock_range_old:
                rock_type_map[block_id] = (
                    5 if (binary_blobs[x,y]==False) else 0
                )
            else:
                rock_type_map[block_id] = 6
    return rock_type_map

def render_rock_map(rock_type_map, basemap, filename):
    width = basemap["settings"]["width"]
    height = basemap["settings"]["height"]
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    for x in range(width):
        for y in range(height):
            block_id = index(basemap, x, y)
            rock_type = rock_type_map.get(block_id, 0)
            pixels[x, y] = ROCK_COLORS[rock_type]
    img.save(f"{filename}.png")
    print(f"Saved rock map as {filename}.png")

rock_type_map = classify_rock(age_map, age_range, basemap)
render_rock_map(rock_type_map, basemap, "rock_map")