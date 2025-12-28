from abc import ABC, abstractmethod
from typing import Callable

from vector import Vector2


class Bullet(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector2:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Bullets(ABC):
    @abstractmethod
    def spawn(self, position: Vector2, velocity: Vector2) -> None:
        ...

    @abstractmethod
    def kill(self, bullet: Bullet) -> None:
        ...

    @abstractmethod
    def apply(self, function: Callable[[Bullet], None]) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class RigidBody(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector2:
        ...

    @property
    @abstractmethod
    def velocity(self) -> Vector2:
        ...

    @abstractmethod
    def set_velocity(self, velocity: Vector2) -> None:
        ...

    @abstractmethod
    def set_position(self, position: Vector2) -> None:
        ...

    @abstractmethod
    def update(self, acceleration: Vector2, dt: float) -> None:
        ...


class Player(ABC):
    @property
    @abstractmethod
    def rigid_body(self) -> RigidBody:
        ...

    @property
    @abstractmethod
    def can_shoot(self) -> bool:
        ...

    @abstractmethod
    def at_shot_was_made(self) -> None:
        ...

    @abstractmethod
    def set_direction(self, direction: Vector2) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


