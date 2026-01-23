from abc import ABC, abstractmethod
from typing import Callable
import arcade
from vector import Vector2


class Bullet(ABC):
    @property
    @abstractmethod
    def position(self) -> Vector2:
        ...

    @property
    @abstractmethod
    def damage(self) -> float:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Bullets(ABC):
    @property
    @abstractmethod
    def all_bullets(self) -> list[Bullet]:
        ...

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

    def _is_bullet_out_of_screen(self, bullet: Bullet, player_pos: Vector2) -> bool:
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
    def weapon(self) -> "Gun":
        ...

    @property
    @abstractmethod
    def current_texture(self) -> arcade.Texture:
        ...

    @property
    @abstractmethod
    def health(self) -> "Health":
        ...

    @abstractmethod
    def set_weapon(self, weapon) -> None:
        ...

    @abstractmethod
    def set_direction(self, direction: Vector2) -> None:
        ...

    def set_animations(self, idle_texture: arcade.Texture, attack_animation: "Animations") -> None:
        ...

    @abstractmethod
    def set_health(self, health: "Health") -> None:
        ...

    @abstractmethod
    def start_attack(self) -> None:
        ...

    @abstractmethod
    def take_damage(self) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Camera(ABC):
    @property
    @abstractmethod
    def camera(self) -> arcade.camera.Camera2D:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Enemy(ABC):
    @property
    @abstractmethod
    def rigid_body(self) -> RigidBody:
        ...

    @property
    @abstractmethod
    def current_texture(self) -> arcade.Texture:
        ...

    @property
    @abstractmethod
    def health(self) -> "Health":
        ...

    @abstractmethod
    def set_walk_animation(self, animation: "Animations") -> None:
        ...

    @abstractmethod
    def set_health(self, health: "Health") -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class Gun(ABC):
    @property
    @abstractmethod
    def can_shoot(self) -> bool:
        ...

    @abstractmethod
    def shoot(self, direction: Vector2) -> None:
        ...



class Animations(ABC):
    @property
    @abstractmethod
    def current_texture(self) -> arcade.Texture:
        ...

    @property
    @abstractmethod
    def is_playing(self) -> bool:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def play(self, restart: bool = True) -> None:
        ...


class Health(ABC):
    def __init__(self, max_hp: float,
        on_damage: Callable[[float], None], on_death: Callable[[], None]) -> None:
        ...

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        ...

    @abstractmethod
    def take_damage(self, damage: float) -> bool:
        ...