from dataclasses import dataclass
from vector import Vector2
import protocols as proto

DAMAGE = 15.0

@dataclass
class Bullet(proto.Bullet):
    _position: Vector2
    _velocity: Vector2

    @property
    def position(self) -> Vector2:
        return self._position

    @property
    def damage(self) -> float:
        return DAMAGE

    def update(self, dt: float) -> None:
        delta_position = self._velocity * dt
        self._position += delta_position

