# Base class for each entity put into a game space.

from pygame import sprite
from pygame.surface import Surface
from collider import Collider
from typing import Self


class Entity:
    """
    Parent class for each entity used in a game space.

    ---

    Attributes:
        _parent(Entity | None):
            The parent entity of this entity. Is *None* if this entity has no parent.
        _children(list[Entity]):
            The children entitys of this entity. Is an empty list if this entity has no children.
        _sprite(pygame.sprite.Sprite | None):  
            The sprite of this entity. Is *None* if no sprite should be implemented.
        _collider(Collider | None):  
            The collider of this entity. Is *None* if no collider should be implemented.
    """

    def __init__(self, position = (0.0, 0.0), rotation = 0.0, scale = (1.0, 1.0)):
        """
        Runs at the instanciation of an entity.

        - Must contain super().__init__() in the beginning of overwritten method.
        """

        self._parent : Entity | None = None
        self._children : list[Entity] = []
        self._position = position
        self._rotation = rotation
        self._scale = scale
        self._sprite : sprite.Sprite | None = None
        self._collider : Collider | None = None

    def update(self, dt : float) -> None:
        """
        Code in this method is run once every frame.
        
        - Should not be called by other scripts.

        ---

        Args:
            dt(float):
                Delta time; the time taken from previous frame to this frame.
            test(int):
                This is just to see the structure of this segment.
        """
        
        pass

    def copy(self) -> Self:
        """
        Creates and returns a copy of this entity.
        """
        
        pass

    def render(self, renderer: Surface) -> None:
        """
        If this entity contains a sprite, this method will render said sprite.

        - Should not be called by other scripts.
        - Should not be overwritten.

        ---

        Args:
            renderer(Surface):
                The renderer this entity's sprite will be rendered onto.
        """
        
        if self._sprite is not None:
            pass

    def when_collide(self, collider: Collider) -> None:
        """
        If this entity contains a collider, this method will run on the instance another collider
        collides with it. 
        """
        
        pass

    def while_collide(self, collider: Collider) -> None:
        pass

    def when_not_collide(self, collider: Collider) -> None:
        pass

    def while_not_collide(self, collider: Collider) -> None:
        pass

    def __repr__(self) -> str:
        return f"Entity<{self.__name__}, {id(self)}>"
    

class TestEntity(Entity):
    def __init__(self):
        super().__init__()

    def copy(self):
        return super().copy()