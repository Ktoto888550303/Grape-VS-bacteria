from dataclasses import dataclass

import arcade
from pathlib import Path
import protocols as proto


ENEMY_RADIUS = 150
ENEMY_COLOR = arcade.color.GREEN
PLAYER_RADIUS = 100
PLAYER_COLOR = arcade.color.GRAPE
BULLET_IMG = arcade.load_texture(Path("data") / "player" / "gun" / "bullet.png")


@dataclass
class Draw:
    def bullet(self, bullet: proto.Bullet) -> None:
            position = bullet.position.tuple
            arcade.draw_texture_rect(BULLET_IMG, arcade.rect.XYWH(*position, 20, 20))

    def bullets(self, bullets: proto.Bullets) -> None:
        bullets.apply(self.bullet)

    def player(self, player: proto.Player) -> None:
        position = player.rigid_body.position.tuple
        arcade.draw_texture_rect(player.current_texture,
                                 arcade.rect.XYWH(*position, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))

    def enemy(self, enemy: proto.Enemy) -> None:
        position = enemy.rigid_body.position.tuple
        arcade.draw_texture_rect(enemy.current_texture,
            arcade.rect.XYWH(*position, ENEMY_RADIUS * 2, ENEMY_RADIUS * 2))

    def enemies(self, enemies: list[proto.Enemy]) -> None:
        for enemy in enemies:
            self.enemy(enemy)