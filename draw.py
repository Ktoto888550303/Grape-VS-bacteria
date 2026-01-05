from dataclasses import dataclass

import arcade

import protocols as proto

BULLET_RADIUS = 10
BULLET_COLOR = arcade.color.BLACK

ENEMY_RADIUS = 30
ENEMY_COLOR = arcade.color.GREEN
PLAYER_RADIUS = 50
PLAYER_COLOR = arcade.color.GRAPE


@dataclass
class Draw:
    def bullet(self, bullet: proto.Bullet) -> None:
        arcade.draw_circle_filled(*bullet.position.tuple, BULLET_RADIUS, BULLET_COLOR)

    def bullets(self, bullets: proto.Bullets) -> None:
        bullets.apply(self.bullet)

    def player(self, player: proto.Player) -> None:
        arcade.draw_circle_filled(*player.rigid_body.position.tuple, PLAYER_RADIUS, PLAYER_COLOR)

    def enemy(self, enemy: proto.Enemy) -> None:
        arcade.draw_circle_filled(*enemy.rigid_body.position.tuple, ENEMY_RADIUS, ENEMY_COLOR)

    def enemies(self, enemies: list[proto.Enemy]) -> None:
        for enemy in enemies:
            self.enemy(enemy)