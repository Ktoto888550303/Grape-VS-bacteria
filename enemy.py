from dataclasses import dataclass, field
import protocols as proto
from vector import Vector2

ENEMY_SPEED = 150
ENEMY_RADIUS = 30

@dataclass
class Enemy:
    _enemy_body: proto.RigidBody
    _target_player: proto.Player
    _speed: float = field(default=ENEMY_SPEED)

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._enemy_body

    def update(self, dt: float) -> None:
        direction = self._target_player.rigid_body.position - self._enemy_body.position
        if direction.length < 1:  # не забыть потом добавить урон игроку вместо остановки
            return
        if direction.length > 0:
            direction = direction.normalize

        velocity = direction * self._speed
        self._enemy_body.set_velocity(velocity)
        self._enemy_body.update(Vector2.zero(), dt)

