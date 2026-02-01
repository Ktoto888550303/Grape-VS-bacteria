from dataclasses import dataclass
import random
import arcade
import protocols as proto
from vector import Vector2
from rigid_body import RigidBody
from enemy import Enemy
from health import Health

ENEMY_SPEED = 200
ENEMY_RADIUS = 30
ENEMY_DAMAGE = 20
ENEMY_HEALTH = 100

FAST_ENEMY_SPEED = 270
FAST_ENEMY_DAMAGE = 10
FAST_ENEMY_HEALTH = 50

SPAWN_AREA_MIN = Vector2(100, 100)
SPAWN_AREA_MAX = Vector2(1500, 800)
DISTANCE_FROM_PLAYER = 200
FAST_ENEMY_CHANCE = 0.3


@dataclass
class EnemySpawner:
    _player: proto.Player
    _walk_animation: proto.Animations
    _damage_texture: arcade.Texture
    _fast_walk_animation: proto.Animations
    _fast_damage_texture: arcade.Texture

    def _spawn_single_enemy(self) -> proto.Enemy:
        fast_enemy = random.random() < FAST_ENEMY_CHANCE

        if fast_enemy:
            return self._create_enemy("fast")
        else:
            return self._create_enemy("base")

    def _create_enemy(self, name: str) -> proto.Enemy:
        position = self._get_valid_spawn_position()
        enemy_body = RigidBody(position, Vector2.zero())

        if name == "base":
            enemy = Enemy(enemy_body, self._player, _speed=ENEMY_SPEED, _damage=ENEMY_DAMAGE)
            enemy.set_walk_animation(self._walk_animation)
            enemy.set_damage_texture(self._damage_texture)
            enemy_health = Health(max_hp=ENEMY_HEALTH)
            enemy.set_health(enemy_health)
            return enemy
        elif name == "fast":
            enemy = Enemy(enemy_body, self._player, _speed=FAST_ENEMY_SPEED, _damage=FAST_ENEMY_DAMAGE)
            enemy.set_walk_animation(self._fast_walk_animation)
            enemy.set_damage_texture(self._fast_damage_texture)
            enemy_health = Health(max_hp=FAST_ENEMY_HEALTH)
            enemy.set_health(enemy_health)
            return enemy

    def _get_valid_spawn_position(self) -> Vector2:
        attempts = 0
        max_attempts = 100

        while attempts < max_attempts:
            random_x = random.uniform(SPAWN_AREA_MIN.x, SPAWN_AREA_MAX.x)
            random_y = random.uniform(SPAWN_AREA_MIN.y, SPAWN_AREA_MAX.y)
            position = Vector2(random_x, random_y)

            if self._is_position_valid(position):
                return position

            attempts += 1
        random_x = random.uniform(SPAWN_AREA_MIN.x, SPAWN_AREA_MAX.x)
        random_y = random.uniform(SPAWN_AREA_MIN.y, SPAWN_AREA_MAX.y)
        return Vector2(random_x, random_y)

    def _is_position_valid(self, position: Vector2) -> bool:
        player_position = self._player.rigid_body.position
        distance = (position - player_position).length

        return distance >= DISTANCE_FROM_PLAYER

    def spawn_enemies(self, count: int) -> list[proto.Enemy]:
        enemies = []
        for i in range(count):
            enemy = self._spawn_single_enemy()
            enemies.append(enemy)

        return enemies

