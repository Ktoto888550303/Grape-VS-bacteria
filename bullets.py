from dataclasses import dataclass, field
from typing import Callable

import protocols as proto
from vector import Vector2
from bullet import Bullet

BULLET_SPEED = 350
BULLET_MAX_DISTANCE = 1000


@dataclass(frozen=True)
class Bullets(proto.Bullets):
    _player_pos: Callable[[], Vector2]
    _bullets: list[proto.Bullet] = field(init=False, default_factory=list)

    @property
    def all_bullets(self) -> list[proto.Bullet]:
        return list(self._bullets)

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
        player_pos = self._player_pos()
        for bullet in self._bullets:
            bullet.update(dt)
            if self._is_bullet_out_of_screen(bullet, player_pos):
                self.kill(bullet)

    def _is_bullet_out_of_screen(self, bullet: proto.Bullet, player_pos: Vector2) -> bool:
        position = bullet.position
        distance = (position - player_pos).length
        return distance > BULLET_MAX_DISTANCE
