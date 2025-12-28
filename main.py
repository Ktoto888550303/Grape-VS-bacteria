import arcade

from bullets import Bullets
from player import Player
from draw import Draw
from vector import Vector2Int, Vector2
from game_engine import GameEngine
from  rigid_body import RigidBody

TITLE = "Grapes VS bacteria"
SCREEN_SHAPE = Vector2Int(1080, 720)


def main() -> None:
    bullets = Bullets(SCREEN_SHAPE)
    player = Player(RigidBody(SCREEN_SHAPE.as_vector2 * .5, Vector2.zero()))

    engine = GameEngine(TITLE, SCREEN_SHAPE, Draw(), bullets, player)
    engine.mouse_clicked.subscribe(lambda position: _on_mouse_click(position, bullets, player))
    engine.keyboard_state_changed.subscribe(lambda keys: player.set_direction(_keys_to_player_direction(keys)))

    engine.run()


def _on_mouse_click(position: Vector2, bullets: Bullets, player: Player) -> None:
    if not player.can_shoot:
        return

    bullets.spawn(player.rigid_body.position, (position - player.rigid_body.position).normalize)
    player.at_shot_was_made()


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

