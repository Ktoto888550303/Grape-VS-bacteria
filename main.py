import arcade

from bullets import Bullets
from player import Player
from draw import Draw
from vector import Vector2Int, Vector2
from game_engine import GameEngine
from rigid_body import RigidBody
from enemy import Enemy
from gun import Gun
from animation import (load_player_attack_texture, load_player_idle_texture, load_enemy_walk_animation,
                       load_enemy_damage_texture)
from health import Health

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
    enemy_positions = [Vector2(100, 100), Vector2(500, 500), Vector2(800, 300)]
    enemy_walk_animation = load_enemy_walk_animation()
    enemy_damage_texture = load_enemy_damage_texture()

    engine = GameEngine(TITLE, SCREEN_SHAPE, Draw(), bullets, player, enemies)
    player_health = Health(
        max_hp=100,
        on_damage=lambda damage: player.take_damage(),
        on_death=lambda: setattr(engine, '_game_over', True)
    )
    player.set_health(player_health)
    for position in enemy_positions:
        enemy_body = RigidBody(position, Vector2.zero())
        enemy = Enemy(enemy_body, player)
        enemy.set_walk_animation(enemy_walk_animation)
        enemy.set_damage_texture(enemy_damage_texture)
        enemy_health = Health(
            max_hp=50,
            on_damage=lambda d, e=enemy: e.take_damage(),
            on_death=lambda e=enemy: enemies.remove(e) if e in enemies else None
        )
        enemy.set_health(enemy_health)
        enemies.append(enemy)

    engine.mouse_clicked.subscribe(lambda position: _on_mouse_click(position, player))
    engine.keyboard_state_changed.subscribe(lambda keys: player.set_direction(_keys_to_player_direction(keys)))

    engine.run()


def _on_mouse_click(position: Vector2, player: Player) -> None:
    if player.weapon.can_shoot:
        direction = (position - player.rigid_body.position).normalize
        player.weapon.shoot(direction)
        player.start_attack()


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