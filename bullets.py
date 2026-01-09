from dataclasses import dataclass, field
from typing import Callable

import protocols as proto
from vector import Vector2, Vector2Int
from bullet import Bullet

BULLET_SPEED = 300


@dataclass(frozen=True)
class Bullets(proto.Bullets):
    _screen_shape: Vector2Int

    _bullets: list[proto.Bullet] = field(init=False, default_factory=list)

    def spawn(self, position: Vector2, direction: Vector2) -> None:
        assert direction.length <= 1.00001
        velocity = direction * BULLET_SPEED
        bullet = Bullet(position, velocity)
        self._bullets.append(bullet)

    def kill(self, bullet: proto.Bullet) -> None:
        assert bullet in self._bullets
        self._bullets.remove(bullet)

    def apply(self, function: Callable[[proto.Bullet], None]) -> None:
        for bullet in self._bullets:
            function(bullet)

    def update(self, dt: float) -> None:
        for bullet in self._bullets:
            bullet.update(dt)
            if self._is_bullet_out_of_screen(bullet):
                self.kill(bullet)

    def _is_bullet_out_of_screen(self, bullet: proto.Bullet) -> bool:
        position = bullet.position
        return not (0 <= position.x < self._screen_shape.x and
                    0 <= position.y < self._screen_shape.y)

