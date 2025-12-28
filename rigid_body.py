from attrs import define
from vector import Vector2

@define
class RigidBody:
    _position: Vector2
    _velocity: Vector2

    @property
    def position(self) -> Vector2:
        return self._position

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    def set_velocity(self, velocity: Vector2) -> None:
        self._velocity = velocity

    def set_position(self, position: Vector2) -> None:
        self._position = position

    def update(self, acceleration: Vector2, dt: float) -> None:
        delta_position = self._velocity * dt + (acceleration * dt**2) * .5
        delta_velocity =  acceleration * dt
        self._position += delta_position
        self._velocity += delta_velocity

