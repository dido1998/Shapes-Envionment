import cairo
import itertools
import logging
import logging.config
import numpy as np
import yaml

SHAPE_CIRCLE = 0
SHAPE_SQUARE = 1
SHAPE_TRIANGLE = 2
N_SHAPES = SHAPE_TRIANGLE + 1
SHAPE_STR = {0: "circle", 1: "square", 2: "triangle"}

SIZE_SMALL = 0
SIZE_BIG = 1
N_SIZES = SIZE_BIG + 1
SIZE_STR = {0: "small", 1: "big"}

COLOR_RED = 0
COLOR_GREEN = 1
COLOR_BLUE = 2
N_COLORS = COLOR_BLUE + 1
COLOR_STR = {0: "red", 1: "green", 2: "blue"}

BOOL_STR = {True: "true", False: "false"}

WIDTH = 30
HEIGHT = 30

N_CELLS = 3

CELL_WIDTH = WIDTH / N_CELLS
CELL_HEIGHT = HEIGHT / N_CELLS

BIG_RADIUS = CELL_WIDTH * .75 / 2
SMALL_RADIUS = CELL_WIDTH * .5 / 2

def draw(shape, color, size, left, top, ctx, config):
    center_x = (left + .5) * config.CELL_WIDTH
    center_y = (top + .5) * config.CELL_HEIGHT

    radius = SMALL_RADIUS if size == SIZE_SMALL else BIG_RADIUS
    radius *= (.9 + np.random.random() * .2)

    if color == COLOR_RED:
        rgb = np.asarray([1., 0., 0.])
    elif color == COLOR_GREEN:
        rgb = np.asarray([0., 1., 0.])
    else:
        rgb = np.asarray([0., 0., 1.])
    rgb += (np.random.random(size=(3,)) * .4 - .2)
    rgb = np.clip(rgb, 0., 1.)

    #rgb = np.asarray([1., 1., 1.])

    if shape == SHAPE_CIRCLE:
        ctx.arc(center_x, center_y, radius, 0, 2*np.pi)
    elif shape == SHAPE_SQUARE:
        ctx.new_path()
        ctx.move_to(center_x - radius, center_y - radius)
        ctx.line_to(center_x + radius, center_y - radius)
        ctx.line_to(center_x + radius, center_y + radius)
        ctx.line_to(center_x - radius, center_y + radius)
    else:
        ctx.new_path()
        ctx.move_to(center_x - radius, center_y + radius)
        ctx.line_to(center_x, center_y - radius)
        ctx.line_to(center_x + radius, center_y + radius)
    ctx.set_source_rgb(*rgb)
    ctx.fill()

class Image:
    def __init__(self, shapes, colors, sizes, data, state, cheat_data = None):
        self.shapes = shapes
        self.colors = colors
        self.sizes = sizes 
        self.data = data
        self.state = state
        self.cheat_data = cheat_data

def sample_image(config):
    
    
    all_colors_represented = False
    while not all_colors_represented:
        data = np.zeros((config.WIDTH, config.HEIGHT, 4), dtype=np.uint8)
        state = np.zeros((config.WIDTH, config.HEIGHT), dtype = np.float32)
        state.fill(-1)
        cheat_data = np.zeros((6, config.N_CELLS, config.N_CELLS))
        surf = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, config.WIDTH, config.HEIGHT)
        ctx = cairo.Context(surf)
        ctx.set_source_rgb(0., 0., 0.)
        ctx.paint()

        shapes = [[None for c in range(config.N_CELLS)] for r in range(config.N_CELLS)]
        colors = [[None for c in range(config.N_CELLS)] for r in range(config.N_CELLS)]
        sizes = [[None for c in range(config.N_CELLS)] for r in range(config.N_CELLS)]
        colors_rep = [0, 0, 0]
        for r in range(config.N_CELLS):
            for c in range(config.N_CELLS):
                if np.random.random() < 0.2:
                    continue
                shape = np.random.randint(N_SHAPES)
                color = np.random.randint(N_COLORS)
                size = np.random.randint(N_SIZES)
                colors_rep[color]+=1
                draw(shape, color, size, c, r, ctx, config)
                shapes[r][c] = shape
                colors[r][c] = color
                for i in range(10):
                    for j in range(10):
                        state[r*10 + i, c*10 + j] = color
                sizes[r][c] = size
                cheat_data[shape][r][c] = 1
                cheat_data[N_SHAPES + color][r][c] = 1
        all_colors_represented = True
        for c in colors_rep:
            if c == 0:
                all_colors_represented = False
                break

    return Image(shapes, colors, sizes, data, state, cheat_data)
