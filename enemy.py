from dataclasses import dataclass, field
import protocols as proto
from vector import Vector2
from animations import Animations
import arcade
from health import Health
from time import time

ENEMY_SPEED = 150
ENEMY_RADIUS = 30
ENEMY_DAMAGE = 20
COOLDOWN = 0.5
DAMAGE_TIME = 0.2

@dataclass
class Enemy(proto.Enemy):  # он тоже разросся, но не так сильно как игрок
    _enemy_body: proto.RigidBody
    _target_player: proto.Player
    _speed: float = field(default=ENEMY_SPEED)

    _walk_animation: Animations = field(init=False, default=None)
    _damage_texture: arcade.Texture = field(init=False, default=None)

    _health: Health = field(init=False, default=None)
    _damage: float = field(default=ENEMY_DAMAGE)
    _last_attack_time: float = field(init=False, default=0)
    _last_damage_time: float = field(init=False, default=0)
    _is_showing_damage: bool = field(init=False, default=False)

    @property
    def rigid_body(self) -> proto.RigidBody:
        return self._enemy_body

    @property
    def current_texture(self) -> arcade.Texture:
        current_time = time()
        if self._is_showing_damage and current_time - self._last_damage_time < DAMAGE_TIME:
            return self._damage_texture
        if self._walk_animation:
            return self._walk_animation.current_texture

    @property
    def health(self) -> Health:
        return self._health

    def set_walk_animation(self, animation: proto.Animations) -> None:
        self._walk_animation = animation
        if self._walk_animation:
            self._walk_animation.play()

    def set_damage_texture(self, texture: arcade.Texture) -> None:
        self._damage_texture = texture

    def set_health(self, health: Health) -> None:
        self._health = health

    def take_damage(self) -> None:
        self._last_damage_time = time()
        self._is_showing_damage = True

    def update(self, dt: float) -> None:
        current_time = time()

        if self._is_showing_damage and current_time - self._last_damage_time >= DAMAGE_TIME:
            self._is_showing_damage = False

        direction = self._target_player.rigid_body.position - self._enemy_body.position
        distance = direction.length
        if distance < ENEMY_RADIUS:
            if current_time - self._last_attack_time >= COOLDOWN:
                if self._target_player.health:
                    self._target_player.health.take_damage(self._damage)
                self._last_attack_time = current_time
            self._enemy_body.set_velocity(Vector2.zero())
            self._enemy_body.update(Vector2.zero(), dt)
        else:
            if direction.length > 0:
                direction = direction.normalize

            velocity = direction * self._speed
            self._enemy_body.set_velocity(velocity)
            self._enemy_body.update(Vector2.zero(), dt)

        if self._walk_animation:
            if not self._walk_animation.is_playing:
                self._walk_animation.play()
            self._walk_animation.update()