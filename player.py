from dataclasses import dataclass, field
import protocols as proto
from vector import Vector2


MAX_SPEED = 250
ACCELERATION = 950
DRAG = 2

@dataclass
class Player(proto.Player):
    _rigid_body: proto.RigidBody
    _direction: Vector2 = field(init=False, default=Vector2.zero())
    _weapon: proto.Gun = field(init=False, default=None)

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._rigid_body

    @property
    def weapon(self) -> proto.Gun:
        return self._weapon

    def set_weapon(self, weapon) -> None:
        self._weapon = weapon

    def set_direction(self, direction: Vector2) -> None:
        assert direction.length <= 1.00001
        self._direction = direction

    def update(self, dt: float) -> None:
        acceleration = self._direction * ACCELERATION
        acceleration -= self._rigid_body.velocity * DRAG
        self._rigid_body.update(acceleration, dt)
        velocity = self._rigid_body.velocity
        if velocity.length > MAX_SPEED:
            self._rigid_body.set_velocity(velocity.normalize * MAX_SPEED)