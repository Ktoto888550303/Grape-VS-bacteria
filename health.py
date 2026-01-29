import protocols as proto
from observer import Event


class Health(proto.Health):
    def __init__(self, max_hp: float) -> None:
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.damaged = Event[float]()
        self.died = Event()

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: float) -> bool:
        if not self.is_alive:
            return False
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

        self.damaged.invoke(damage)

        if not self.is_alive:
            self.died.invoke()
        return True