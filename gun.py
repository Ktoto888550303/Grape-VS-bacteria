from time import time
from dataclasses import dataclass, field
import protocols as proto
from vector import Vector2
from typing import Callable


@dataclass
class Gun(proto.Gun):
    _bullets: proto.Bullets
    _position_provider: Callable[[], Vector2]
    _shoot_frequency: float = field(default=15)
    _last_shot_time: float = field(init=False, default_factory=time)

    @property
    def can_shoot(self) -> bool:
        return time() - self._last_shot_time >= 1 / self._shoot_frequency

    def shoot(self, direction: Vector2) -> None:
        if not self.can_shoot:
            return
        position = self._position_provider()
        self._bullets.spawn(position, direction)
        self._last_shot_time = time()