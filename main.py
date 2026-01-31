import arcade

from bullets import Bullets
from player import Player
from draw import Draw
from vector import Vector2Int, Vector2
from game_engine import GameEngine
from rigid_body import RigidBody
from enemy import Enemy
from enemy_spawner import EnemySpawner
from gun import Gun
from animation import (load_player_attack_texture, load_player_idle_texture, load_enemy_walk_animation,
                       load_enemy_damage_texture)
from health import Health
from sound import Sound

TITLE = "Grapes VS bacteria"
SCREEN_SHAPE = Vector2Int(1920, 1080)


def main() -> None:
    player = Player(RigidBody(SCREEN_SHAPE.as_vector2 * 1.5, Vector2.zero()))
    bullets = Bullets(lambda: player.rigid_body.position)

    gun = Gun(bullets, _position_provider=lambda: player.rigid_body.position)
    player.set_weapon(gun)

    player_idle_texture = load_player_idle_texture()
    player_attack_texture = load_player_attack_texture()
    player.set_animations(player_idle_texture, player_attack_texture)

    enemies = []

    enemy_walk = load_enemy_walk_animation("base")
    enemy_damage = load_enemy_damage_texture("base")

    fast_enemy_walk = load_enemy_walk_animation("speed")
    fast_enemy_damage = load_enemy_damage_texture("speed")
    spawner = EnemySpawner(player, enemy_walk, enemy_damage, fast_enemy_walk, fast_enemy_damage)

    engine = GameEngine(TITLE, SCREEN_SHAPE, Draw(), bullets, player, enemies)

    sound_manager = Sound()
    sound_manager.play_background_music()

    player_health = Health(max_hp=100)
    player.set_health(player_health)
    player_health.damaged.subscribe(lambda damage: player.take_damage())
    player_health.damaged.subscribe(lambda damage: sound_manager.play_hit_player())
    player_health.died.subscribe(lambda: engine.player_dead())
    player_health.died.subscribe(lambda: sound_manager.play_player_dead())
    player_health.died.subscribe(lambda: sound_manager.stop_background_music())

    enemies.extend(spawner.spawn_enemies(10))

    for enemy in enemies:
        _subscribe_enemy_events(enemy, engine, sound_manager)

    engine.mouse_clicked.subscribe(lambda position: _on_mouse_click(position, player))
    engine.keyboard_state_changed.subscribe(lambda keys: player.set_direction(_keys_to_player_direction(keys)))

    engine.run()


def _on_mouse_click(position: Vector2, player: Player) -> None:
    if player.weapon.can_shoot:
        direction = (position - player.rigid_body.position).normalize
        player.weapon.shoot(direction)
        player.start_attack()


def _subscribe_enemy_events(enemy: Enemy, engine: GameEngine, sound) -> None:
    if enemy.health:
        enemy.health.damaged.subscribe(lambda damage: enemy.take_damage())
        enemy.health.damaged.subscribe(lambda damage: sound.play_hit_enemy())
        enemy.health.died.subscribe(lambda: engine.enemy_dead(enemy))

def _keys_to_player_direction(keys: set[int]) -> Vector2:
    d_is_pressed = arcade.key.D in keys
    a_is_pressed = arcade.key.A in keys
    w_is_pressed = arcade.key.W in keys
    s_is_pressed = arcade.key.S in keys
    x = d_is_pressed - a_is_pressed
    y = w_is_pressed - s_is_pressed

    direction = Vector2(x, y)

    return direction.normalize if direction.length > 0 else direction


if __name__ == "__main__":
    main()