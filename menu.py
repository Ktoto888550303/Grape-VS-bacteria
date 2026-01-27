from dataclasses import dataclass
import arcade
from vector import Vector2


@dataclass
class Button:
    texture: arcade.Texture
    center: Vector2
    size: Vector2

    def is_clicked(self, click_pos: Vector2) -> bool:
        half_size = self.size * 0.5
        min_corner = self.center - half_size
        max_corner = self.center + half_size

        return (min_corner.x <= click_pos.x <= max_corner.x and
                min_corner.y <= click_pos.y <= max_corner.y)

    def draw(self) -> None:
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(*self.center.tuple, self.size.x, self.size.y)
        )


@dataclass
class Menu:
    background: arcade.Texture
    buttons: dict[str, Button]  # name -> button

    def draw(self) -> None:
        screen = arcade.get_window()
        screen_width, screen_height = screen.width, screen.height

        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(screen_width / 2, screen_height / 2, screen_width, screen_height)
        )

        for button in self.buttons.values():
            button.draw()

    def click(self, x: float, y: float) -> str:
        click_pos = Vector2(x, y)

        for name, button in self.buttons.items():
            if button.is_clicked(click_pos):
                return name