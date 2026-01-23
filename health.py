from typing import Callable
import protocols as proto


class Health(proto.Health):
    def __init__(self, max_hp: float,
        on_damage: Callable[[float], None], on_death: Callable[[], None]) -> None:
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.on_damage = on_damage
        self.on_death = on_death

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: float) -> bool:
        if not self.is_alive:
            return False
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        if self.on_damage:
            self.on_damage(damage)
        if not self.is_alive and self.on_death:
            self.on_death()
        return True