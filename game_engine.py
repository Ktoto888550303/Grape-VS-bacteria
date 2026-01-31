import arcade
from arcade.gui import UIManager, UILabel
import protocols as proto
from draw import Draw
from vector import Vector2Int, Vector2
from observer import Event, OnEventSubscriber
from camera import Camera
from menu import Menu, Button
from pathlib import Path
from video import Video


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

        self._game_over = False
        self._in_menu = True
        self._playing_video = False

        self._draw = draw
        self._bullets = bullets
        self._player = player
        self._enemies = enemies

        map_name = Path("data") / "map" / "map_for_game.tmx"
        self._tile_map = arcade.load_tilemap(map_name, scaling=2.5)

        self._camera_mover = Camera(arcade.Camera2D(), self._player)
        self._camera_mover.camera.position = self._player.rigid_body.position.tuple

        self._ui_manager = UIManager()
        self._ui_manager.enable()

        self._health_label = UILabel(text=f"Health: {self._player.health.current_hp if self._player.health else 0}",
                                     font_size=40, text_color=arcade.color.WHITE, x=20, y=self.height - 100)
        self._ui_manager.add(self._health_label)
        self._menu_game()

        self.pressed_keys = set[int]()

        self._mouse_clicked_left = Event[Vector2, None]()
        self._keyboard_state_changed = Event[set[int], None]()

        self._video = Video()

    @property
    def mouse_clicked(self) -> OnEventSubscriber[Vector2, None]:
        return self._mouse_clicked_left.subscriber

    @property
    def keyboard_state_changed(self) -> OnEventSubscriber[set[int], None]:
        return self._keyboard_state_changed.subscriber

    def _update_health_label(self) -> None:
        if self._player.health:
            self._health_label.text = f"Health: {self._player.health.current_hp}"

    def _menu_game(self) -> None:
        background_menu = arcade.load_texture(Path("data") / "scene" / "menu.jpg")
        exit_button = arcade.load_texture(Path("data") / "scene" / "exit.png")
        continue_button = arcade.load_texture(Path("data") / "scene" / "contine.png")
        new_game = arcade.load_texture(Path("data") / "scene" / "new_game.png")

        button_width = 400
        button_height = 100
        button_size = Vector2(button_width, button_height)

        spacing = 120
        start_y = 250

        buttons = {
            "exit": Button(exit_button, Vector2(100 + button_width / 2, start_y), button_size),
            "continue": Button(continue_button, Vector2(100 + button_width / 2, start_y + spacing), button_size),
            "new_game": Button(new_game, Vector2(100 + button_width / 2, start_y + spacing * 2), button_size)
        }

        self._menu = Menu(background_menu, buttons)

    def player_dead(self) -> None:
        self._game_over = True

    def enemy_dead(self, enemy) -> None:
        if enemy in self._enemies:
            self._enemies.remove(enemy)

    def on_fixed_update(self, delta_time: float) -> None:
        if self._playing_video:
            self._video.update()
            if self._video.is_finished:
                self._playing_video = False
            return
        if self._in_menu or self._game_over:
            return

        self._player.update(delta_time)

        bullets_to_remove = []
        for bullet in self._bullets.all_bullets:
            for enemies in self._enemies:
                if enemies.health and enemies.health.is_alive:
                    distance = (bullet.position - enemies.rigid_body.position).length
                    if distance < 50:
                        enemies.health.take_damage(bullet.damage)
                        bullets_to_remove.append(bullet)
                        break
        for bullet in bullets_to_remove:
            if bullet in self._bullets.all_bullets:
                self._bullets.kill(bullet)

        for enemies in self._enemies:
            other_enemies = [enemy for enemy in self._enemies if enemy.health and enemy.health.is_alive]
            enemies.update(delta_time, other_enemies)

        self._enemies = [enemy for enemy in self._enemies
                         if enemy.health and enemy.health.is_alive]

        self._bullets.update(delta_time)
        self._camera_mover.update(delta_time)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self._in_menu:
            clicked_button = self._menu.click(x, y)
            if clicked_button == 'exit':
                self.close()
            elif clicked_button == 'continue':
                ...
            elif clicked_button == 'new_game':
                self._in_menu = False
                self._playing_video = True
                self._video.start()
                self._update_health_label()
        else:
            world_pos = self._camera_mover.camera.unproject((x, y))
            self._mouse_clicked_left.invoke(Vector2(world_pos[0], world_pos[1]))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.set_fullscreen(False)
        if not self._in_menu:
            self.pressed_keys.add(symbol)
            self._keyboard_state_changed.invoke(self.pressed_keys)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if not self._in_menu:
            self.pressed_keys.discard(symbol)
            self._keyboard_state_changed.invoke(self.pressed_keys)

    def on_draw(self) -> None:
        self.clear()
        if self._playing_video:
            self._video.draw(self.width / 2, self.height / 2, self.width, self.height)
        elif self._in_menu:
            self._menu.draw()
        else:
            self._tile_map.sprite_lists["down1"].draw()
            self._tile_map.sprite_lists["down2"].draw()
            self._tile_map.sprite_lists["water"].draw()
            self._camera_mover.camera.use()
            self._draw.bullets(self._bullets)
            self._draw.player(self._player)
            self._draw.enemies(self._enemies)
            self._tile_map.sprite_lists["Big_tree"].draw()
            self._tile_map.sprite_lists["border"].draw()
            self._ui_manager.draw()