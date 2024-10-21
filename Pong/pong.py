import pygame



# Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0      # Delta time, i.e. time ellapsed since the last frame, in seconds.


class Player:
    def __init__(self, name : str, pos : tuple[float, float], size : tuple[float, float] = (40, 120),
                 color : tuple[float] | str = "white", speed : float = 200, k_move_up : int = pygame.K_UP,
                 k_move_down : int = pygame.K_DOWN) -> None:
        self.name = name
        self.pos = pos
        self.size = size
        self.color = color
        self.speed = speed
        self.k_move_up = k_move_up
        self.k_move_down = k_move_down

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, val : str) -> None:
        if not isinstance(val, str):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'str'")
        self.__name = val

    @property
    def pos(self) -> tuple[float, float]:
        return tuple(self.__pos)
    
    @pos.setter
    def pos(self, val : tuple[float, float]) -> None:
        if not isinstance(val, (tuple, list)):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'tuple[float, float]'")
        if len(val) != 2:
            raise ValueError(f"'val' must contain 2 elements")
        if not all([isinstance(e, (float, int)) for e in val]):
            raise ValueError(f"'val' must contain only values of type 'float'")
        self.__pos = [float(val[0]), float(val[1])]

    @property
    def x(self) -> float:
        return self.__pos[0]
    
    @x.setter
    def x(self, val : float) -> None:
        if not isinstance(val, (float, int)):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'float'")
        self.__pos[0] = val

    @property
    def y(self) -> float:
        return self.__pos[1]
    
    @y.setter
    def y(self, val : float) -> None:
        if not isinstance(val, (float, int)):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'float'")
        self.__pos[1] = val

    @property
    def size(self) -> tuple[float, float]:
        return tuple(self.__size)
    
    @size.setter
    def size(self, val : tuple[float, float]) -> None:
        if not isinstance(val, (tuple, list)):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'tuple[float, float]'")
        if len(val) != 2:
            raise ValueError(f"'val' must contain 2 elements")
        if not all([isinstance(e, (float, int)) for e in val]):
            raise ValueError(f"'val' must contain only values of type 'float'")
        self.__size = [float(val[0]), float(val[1])]

    @property
    def w(self) -> float:
        return self.__size[0]
    
    @w.setter
    def w(self, val : float) -> None:
        if not isinstance(val, (float, int)):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'float'")
        self.__size[0] = val

    @property
    def h(self) -> float:
        return self.__size[1]
    
    @h.setter
    def h(self, val : float) -> None:
        if not isinstance(val, (float, int)):
            raise TypeError(f"'val' is of type '{type(val).__name__}'; must be 'float'")
        self.__size[1] = val

    @property
    def rect(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.w, self.h)


    def render(self, window : pygame.Surface):
        pygame.draw.rect(window, self.color, pygame.rect.Rect(self.pos, self.size))

    def check_key_pressed(self, keys : pygame.key.ScancodeWrapper):
        if keys[self.k_move_up]:
            self.y -= self.speed*dt
        if keys[self.k_move_down]:
            self.y += self.speed*dt

    def check_collision(self, other_rect : tuple[float, float, float, float]) -> bool:
        if self.x <= other_rect[0] + other_rect[2] and other_rect[0] <= self.x + self.w and \
           self.y <= other_rect[1] + other_rect[3] and other_rect[1] <= self.y + self.h:
            return True
        return False


player1 = Player("Isak", pygame.Vector2(100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    window.fill("black")

    keys = pygame.key.get_pressed()
    player1.check_key_pressed(keys)
    player1.render(window)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(10)/1000

pygame.quit()