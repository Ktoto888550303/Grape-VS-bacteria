from dataclasses import dataclass, field
import protocols as proto
from vector import Vector2
from animations import Animations
import arcade
from health import Health
from time import time

ENEMY_RADIUS = 50
COOLDOWN = 0.5
DAMAGE_TIME = 0.2
FORCE = 800
REPULSION_RADIUS = 120
MIN_DISTANCE = 80


@dataclass
class Enemy(proto.Enemy):
    _enemy_body: proto.RigidBody
    _target_player: proto.Player
    _speed: float

    _walk_animation: Animations = field(init=False, default=None)
    _damage_texture: arcade.Texture = field(init=False, default=None)

    _health: Health = field(init=False, default=None)
    _damage: float
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

    def update(self, dt: float, other_enemies: list["Enemy"] = None) -> None:
        current_time = time()

        if self._is_showing_damage and current_time - self._last_damage_time >= DAMAGE_TIME:
            self._is_showing_damage = False

        direction = self._target_player.rigid_body.position - self._enemy_body.position
        distance = direction.length

        repul_vector = Vector2.zero()

        if other_enemies:
            for current in other_enemies:
                if current.health and current.health.is_alive:
                    to_other = current.rigid_body.position - self._enemy_body.position
                    distance_to_other = to_other.length
                    if 0 < distance_to_other < REPULSION_RADIUS:
                        if distance_to_other > 0:
                            normal_dir = to_other.normalize
                        else:
                            normal_dir = Vector2.right()
                        force = FORCE * (1 - distance_to_other / REPULSION_RADIUS)
                        repul_vector -= normal_dir * force

        if distance < ENEMY_RADIUS:
            if current_time - self._last_attack_time >= COOLDOWN:
                if self._target_player.health:
                    self._target_player.health.take_damage(self._damage)
                self._last_attack_time = current_time
            if repul_vector.length > 0:
                final_velocity = repul_vector
                self._enemy_body.set_velocity(final_velocity)
                self._enemy_body.update(Vector2.zero(), dt)
            else:
                self._enemy_body.set_velocity(Vector2.zero())
                self._enemy_body.update(Vector2.zero(), dt)
        else:
            if direction.length > 0:
                direction = direction.normalize

            to_player = direction * self._speed

            final_velocity = to_player + repul_vector
            max_speed = self._speed * 2.0
            if final_velocity.length > max_speed:
                final_velocity = final_velocity.normalize * max_speed
            self._enemy_body.set_velocity(final_velocity)
            self._enemy_body.update(Vector2.zero(), dt)

        if self._walk_animation:
            if not self._walk_animation.is_playing:
                self._walk_animation.play()
            self._walk_animation.update()