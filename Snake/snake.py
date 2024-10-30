import pygame
import random
from enum import Enum
from typing import Literal



class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Tile:
    def __init__(self, x : int, y : int, w : float = 1, h : float = 1, offset : tuple[float] = (0, 0),
                 color : tuple[int] = (255, 255, 255, 255), tags : list[str] = []) -> None:
        """
        Args:
            `x`(int):
                X coordinate in grid.
            `y`(int):
                Y coordinate in grid.
            `w`(float):
                Width relative to tile width in grid.
            `h`(float):
                Height relative to tile height in grid.
            `offset`(tuple[float]):
                Offset from the grid tile pivot.
            `color`(tuple[int]):
                Fill color.
            `tags`(list[str]):
                Tag attributes to this tile.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.color = color
        self.tags = tags

    def set_coords(self, x : int, y : int) -> None:
        self.x = x
        self.y = y

    def copy(self) -> "Tile":
        return Tile(self.x, self.y, self.w, self.h, (self.offset_x, self.offset_y), self.color, self.tags)

    def render(self, renderer : pygame.Surface, grid : "TileGrid") -> None:
        x = grid.x_o + (self.x + self.offset_x - grid.tile_piv_x*self.w)*grid.tile_w
        y = grid.y_o + (self.y + self.offset_y - grid.tile_piv_y*self.h)*grid.tile_h
        w = grid.tile_w*self.w
        h = grid.tile_h*self.h
        pygame.draw.rect(renderer, self.color, (x, y, w, h))

    def has_tag(self, tag : str) -> bool:
        return tag in self.tags


class TileGrid:
    def __init__(self, x_o : int, y_o : int, tile_w : int, tile_h : int,
                 tile_pivot : tuple = (0.5, 0.5)) -> None:
        self.x_o = x_o
        self.y_o = y_o
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.tile_piv_x = tile_pivot[0]
        self.tile_piv_y = tile_pivot[1]
        self.coord_tiles : dict[tuple[int, int], list[Tile]] = {}

    def clear(self) -> None:
        self.coord_tiles = {}

    def add_tile(self, tile : Tile) -> None:
        if (tile.x, tile.y) not in self.coord_tiles.keys():
            self.coord_tiles[(tile.x, tile.y)] = []
        self.coord_tiles[(tile.x, tile.y)].append(tile)

    def get_tiles(self, x : int, y : int, tag : str = None) -> list[Tile]:
        if (x, y) not in self.coord_tiles.keys():
            return []
        if isinstance(tag, str):
            tiles = self.coord_tiles[(x, y)]
            return [t for t in tiles if t.has_tag(tag)]
        return self.coord_tiles[(x, y)]
    
    def pop_tiles(self, x : int, y : int, tag : str = None) -> list[Tile]:
        if (x, y) not in self.coord_tiles.keys():
            return []
        if isinstance(tag, str):
            tiles = []
            i = 0
            while i < len(self.coord_tiles[(x, y)]):
                if self.coord_tiles[(x, y)][i].has_tag(tag):
                    tiles.append(self.coord_tiles[(x, y)].pop(i))
                else:
                    i += 1
            return tiles
        return self.coord_tiles.pop((x, y), None)
    
    def pop_tile(self, x : int, y : int, tag : str = None) -> Tile:
        if (x, y) not in self.coord_tiles.keys():
            return None
        if isinstance(tag, str):
            ret_tile = None
            for i in range(len(self.coord_tiles[(x, y)])):
                if self.coord_tiles[(x, y)][i].has_tag(tag):
                    ret_tile = self.coord_tiles[(x, y)].pop(i)
                    if self.coord_tiles[(x, y)] == []:
                        self.coord_tiles.pop((x, y))
                    break
            return ret_tile
        ret_tile = self.coord_tiles[(x, y)].pop(0)
        if self.coord_tiles[(x, y)] == []:
            self.coord_tiles.pop((x, y))
        return self.coord_tiles.pop((x, y), None)
    
    def draw_grid(self, renderer : pygame.Surface, color : tuple[int] = (255, 255, 255, 255)) -> None:
        scr_w = renderer.get_width()
        scr_h = renderer.get_height()
        for dir in [-1, 1]:
            x = self.x_o + (min(dir, 0) - self.tile_piv_x)*self.tile_w
            while 0 <= x < scr_w:
                pygame.draw.line(renderer, color, (x, 0), (x, scr_h))
                x += dir*self.tile_w
            y = self.y_o + (min(dir, 0) - self.tile_piv_y)*self.tile_h
            while 0 <= y < scr_h:
                pygame.draw.line(renderer, color, (0, y), (scr_w, y))
                y += dir*self.tile_h

    def render_tiles(self, renderer : pygame.Surface):
        for tiles in self.coord_tiles.values():
            for tile in tiles:
                tile.render(renderer, self)


class Snake:
    def __init__(self, grid : TileGrid, x : int, y : int, bodypart_pre : Tile = Tile(0, 0, tags=["snake"]),
                 start_len : int = 3, speed : float = 2, k_up : int = pygame.K_UP, k_down : int = pygame.K_DOWN,
                 k_left : int = pygame.K_LEFT, k_right : int = pygame.K_RIGHT):
        """
        Args:
            `x`(int):
                X coordinate in grid.
            `y`(int):
                Y coordinate in grid.
            `tile_w`(int):
                Width of each snake tile.
            `tile_h`(int):
                Height of each snake tile.
            `color`(tuple[int]):
                Color of each snake tile.
            `start_len`(int):
                Initial length of the snake.
            `speed`(float):
                Movement speed of the snake in tiles/sec.
            `k_up`(int):
                Keyboard key used to make the snake move up.
            `k_down`(int):
                Keyboard key used to make the snake move down.
            `k_left`(int):
                Keyboard key used to make the snake move left.
            `k_right`(int):
                Keyboard key used to make the snake move right.
        """

        self.grid = grid
        self.x = x
        self.y = y
        self.bodypart_pre = bodypart_pre
        self.speed = speed
        self.k_up = k_up
        self.k_down = k_down
        self.k_left = k_left
        self.k_right = k_right
        self.move_clock = 0
        self.dir = Direction.UP
        self.prev_dir = Direction.UP
        self.part_coords = [(x, y) for _ in range(start_len)]
        self.bodypart_pre.set_coords(x, y)
        for _ in self.part_coords:
            grid.add_tile(self.bodypart_pre.copy())

    def increase_length(self, amount : int = 1) -> None:
        for _ in range(amount):
            self.part_coords.append(self.part_coords[-1])

    def move(self) -> None:
        tail = self.part_coords[-1]
        for i in range(1, len(self.part_coords)):
            self.part_coords[-i] = self.part_coords[-i - 1]
        if self.dir == Direction.UP:
            self.y -= 1
        elif self.dir == Direction.DOWN:
            self.y += 1
        elif self.dir == Direction.LEFT:
            self.x -= 1
        else:
            self.x += 1
        self.part_coords[0] = (self.x, self.y)
        self.prev_dir = self.dir
        self.grid.pop_tile(tail[0], tail[1], "snake")
        self.bodypart_pre.set_coords(self.x, self.y)
        self.grid.add_tile(self.bodypart_pre.copy())

    # - Called from main script -
    def update(self, dt : float) -> None:
        self.move_clock += dt
        move_delay_time = 1/self.speed
        if self.move_clock >= move_delay_time:
            self.move_clock -= move_delay_time
            self.move()
            if len(self.grid.get_tiles(self.x, self.y, "snake")) == 2:
                pass
            elif len(self.grid.get_tiles(self.x, self.y, "food")) == 1:
                self.increase_length()

    def check_key_pressed(self, keys : pygame.key.ScancodeWrapper) -> None:
        if self.prev_dir == Direction.UP or self.prev_dir == Direction.DOWN:
            if keys[self.k_left]:
                self.dir = Direction.LEFT
            elif keys[self.k_right]:
                self.dir = Direction.RIGHT
        else:
            if keys[self.k_up]:
                self.dir = Direction.UP
            elif keys[self.k_down]:
                self.dir = Direction.DOWN


# Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0      # Delta time, i.e. time ellapsed since the last frame, in seconds.
game_state : Literal["game", "gameover", "menu", "hiscore"] = "game"
running = True

TILE_WIDTH = 20
TILE_HEIGHT = 20
X_MIN = -SCREEN_WIDTH//TILE_WIDTH//2 + 1
X_MAX = SCREEN_WIDTH//TILE_WIDTH//2
Y_MIN = -SCREEN_HEIGHT//TILE_HEIGHT//2 + 1
Y_MAX = SCREEN_HEIGHT//TILE_HEIGHT//2
grid = TileGrid(SCREEN_WIDTH//2 - TILE_WIDTH//2, SCREEN_HEIGHT//2 - TILE_HEIGHT//2, TILE_WIDTH, TILE_HEIGHT)
player = Snake(grid, 0, 0, Tile(0, 0, 0.8, 0.8, color=(255, 100, 200), tags=["snake"]), 5, 10)
apple = Tile(random.randint(X_MIN, X_MAX), random.randint(Y_MIN, Y_MAX),
             0.8, 0.8, (0, 0), (255, 255, 0), ["food"])
grid.add_tile(apple)
move_delay_time = 0

# debugging
###

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    window.fill((10, 30, 10))
    keys = pygame.key.get_pressed()

    if game_state == "game":
        # if move_delay_time*player.speed >= 1:
        #     player.move()
        #     move_delay_time -= 1/player.speed
        if player.x == apple.x and player.y == apple.y:
            grid.pop_tile(apple.x, apple.y, "food")
            apple.x = random.randint(X_MIN, X_MAX)
            apple.y = random.randint(Y_MIN, Y_MAX)
            grid.add_tile(apple)
            #player.increase_length()
        elif (len(grid.get_tiles(player.x, player.y, "snake")) == 2 or
              player.x < X_MIN or player.x > X_MAX or player.y < Y_MIN or player.y > Y_MAX):
            game_state = "game_over"
            grid.clear()
        
        player.update(dt)
        player.check_key_pressed(keys)
        grid.render_tiles(window)
    elif game_state == "game_over":
        pass

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60)/1000
    move_delay_time += dt

pygame.quit()