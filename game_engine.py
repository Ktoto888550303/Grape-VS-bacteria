import arcade
from pyglet.window.mouse import buttons_string

import protocols as proto
from draw import Draw
from vector import Vector2Int, Vector2
from observer import Event, OnEventSubscriber
from camera import Camera


class GameEngine(arcade.Window):
    def __init__(self,
                 title: str,
                 screen_shape: Vector2Int,
                 draw: Draw,
                 bullets: proto.Bullets,
                 player: proto.Player,
                 enemies: list[proto.Enemy]) -> None:
        super().__init__(screen_shape.x, screen_shape.y, title, vsync=True, fullscreen=True)
        self.background_color = (23, 8, 1)

        self._draw = draw
        self._bullets = bullets
        self._player = player
        self._enemies = enemies

        map_name = "data/map/map_for_game.tmx"
        self._tile_map = arcade.load_tilemap(map_name, scaling=2.5)

        self._camera_mover = Camera(arcade.Camera2D(), self._player)
        self._camera_mover.camera.position = self._player.rigid_body.position.tuple

        self.pressed_keys = set[int]()

        self._mouse_clicked_left = Event[Vector2, None]()
        self._keyboard_state_changed = Event[set[int], None]()

    @property
    def mouse_clicked(self) -> OnEventSubscriber[Vector2, None]:
        return self._mouse_clicked_left.subscriber

    @property
    def keyboard_state_changed(self) -> OnEventSubscriber[set[int], None]:
        return self._keyboard_state_changed.subscriber

    def on_fixed_update(self, delta_time: float) -> None:
        self._bullets.update(delta_time)
        self._player.update(delta_time)
        for enemy in self._enemies:
            enemy.update(delta_time)
        self._camera_mover.update(delta_time)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        self._mouse_clicked_left.invoke(Vector2(x, y))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.set_fullscreen(False)
        self.pressed_keys.add(symbol)
        self._keyboard_state_changed.invoke(self.pressed_keys)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.pressed_keys.discard(symbol)
        self._keyboard_state_changed.invoke(self.pressed_keys)

    def on_draw(self) -> None:
        self.clear()
        self._tile_map.sprite_lists["down1"].draw()
        self._tile_map.sprite_lists["down2"].draw()
        self._tile_map.sprite_lists["water"].draw()
        self._camera_mover.camera.use()
        self._draw.bullets(self._bullets)
        self._draw.player(self._player)
        self._draw.enemies(self._enemies)
        self._tile_map.sprite_lists["Big_tree"].draw()
        self._tile_map.sprite_lists["border"].draw()

