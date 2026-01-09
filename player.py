from dataclasses import dataclass, field
from time import time

import protocols as proto
from vector import Vector2

SHOOT_FREQUENCY = 10
MAX_SPEED = 250
ACCELERATION = 950
DRAG = 2

@dataclass
class Player(proto.Player):
    _rigid_body: proto.RigidBody
    _direction: Vector2 = field(init=False, default=Vector2.zero())

    # Ерундистика
    _last_shot_time: float = field(init=False, default_factory=time)

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._rigid_body

    # Ерундистика
    @property
    def can_shoot(self) -> bool:
        return time() - self._last_shot_time >= 1 / SHOOT_FREQUENCY

    # Ерундистика
    def at_shot_was_made(self) -> None:
        self._last_shot_time = time()

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