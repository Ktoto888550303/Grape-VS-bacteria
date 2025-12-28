from dataclasses import dataclass

from vector import Vector2
import protocols as proto


@dataclass
class Bullet(proto.Bullet):
    _position: Vector2
    _velocity: Vector2

    @property
    def position(self) -> Vector2:
        return self._position

    def update(self, dt: float) -> None:
        delta_position = self._velocity * dt
        self._position += delta_position

