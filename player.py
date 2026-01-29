from dataclasses import dataclass, field
import protocols as proto
from vector import Vector2
import arcade
from time import time
from health import Health

MAX_SPEED = 250
ACCELERATION = 950
DRAG = 2
ATTACH_DURATION = 0.4
COOLDOWN_DAMAGE = 0.5

@dataclass
class Player(proto.Player):
    _rigid_body: proto.RigidBody
    _direction: Vector2 = field(init=False, default=Vector2.zero())
    _weapon: proto.Gun = field(init=False, default=None)
    _idle_texture: arcade.Texture = field(init=False, default=None)
    _attack_texture: arcade.Texture = field(init=False, default=None)
    _is_attacking: bool = field(init=False, default=False)  # я попозже разберу этот ужас, не проклинайте меня (((
    _current_texture: arcade.Texture = field(init=False, default=None)
    _attack_start_time: float = field(init=False, default=0)
    _health: Health = field(init=False, default=None)
    _damage_taken_time: float = field(init=False, default=0)
    _is_damaged: bool = field(init=False, default=False)

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._rigid_body

    @property
    def weapon(self) -> proto.Gun:
        return self._weapon

    @property
    def current_texture(self) -> arcade.Texture:
        return self._current_texture

    @property
    def health(self) -> Health:
        return self._health

    def set_weapon(self, weapon) -> None:
        self._weapon = weapon

    def set_direction(self, direction: Vector2) -> None:
        assert direction.length <= 1.00001
        self._direction = direction

    def set_animations(self, idle_texture: arcade.Texture, attack_texture: arcade.Texture) -> None:
        self._idle_texture = idle_texture
        self._attack_texture = attack_texture
        self._current_texture = idle_texture

    def set_health(self, health: Health) -> None:
        self._health = health

    def start_attack(self) -> None:
        if not self._is_attacking and self._attack_texture:
            self._is_attacking = True
            self._attack_start_time = time()
            self._current_texture = self._attack_texture

    def take_damage(self) -> None:
        self._is_damaged = True
        self._damage_taken_time = time()

    def update(self, dt: float) -> None:
        current_time = time()
        if self._is_damaged and current_time - self._damage_taken_time >= COOLDOWN_DAMAGE:
            self._is_damaged = False

        acceleration = self._direction * ACCELERATION
        acceleration -= self._rigid_body.velocity * DRAG
        self._rigid_body.update(acceleration, dt)
        velocity = self._rigid_body.velocity
        if velocity.length > MAX_SPEED:
            self._rigid_body.set_velocity(velocity.normalize * MAX_SPEED)

        if self._is_attacking:
            if current_time - self._attack_start_time >= ATTACH_DURATION:
                self._is_attacking = False
                self._current_texture = self._idle_texture
