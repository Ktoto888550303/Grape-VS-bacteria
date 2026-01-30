import arcade
from animations import Animations


ENEMY_FRAME_TIME = 0.8

def load_player_attack_texture() -> arcade.Texture:
    return arcade.load_texture("data/player/gun/grape2.png")


def load_player_idle_texture() -> arcade.Texture:
    return arcade.load_texture("data/player/gun/grape1.png")


def load_enemy_walk_animation(enemy: str) -> Animations:
    textures = []
    if enemy == "base":
        for i in range(1, 4):
            texture_path = f"data/enemy/enemy{i}.png"
            texture = arcade.load_texture(texture_path)
            textures.append(texture)
    elif enemy == "speed":
        for i in range(1, 4):
            texture_path = f"data/enemy/small_enemy{i}.png"
            texture = arcade.load_texture(texture_path)
            textures.append(texture)

    return Animations(
        textures=textures,
        frame_duration=ENEMY_FRAME_TIME,
    )

def load_enemy_damage_texture(enemy: str) -> arcade.Texture:
    if enemy == "base":
        return arcade.load_texture("data/enemy/damage.png")
    elif enemy == "speed":
        return arcade.load_texture("data/enemy/damage2.png")