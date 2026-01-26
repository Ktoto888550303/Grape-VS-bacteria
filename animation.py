import arcade
from animations import Animations


def load_player_attack_texture() -> arcade.Texture:  # лучшая функция №1 (я потом переделаю для разных игроков)
    return arcade.load_texture("data/player/gun/grape2.png")


def load_player_idle_texture() -> arcade.Texture:  # лучшая функция №2
    return arcade.load_texture("data/player/gun/grape1.png")


def load_enemy_walk_animation() -> Animations:
    textures = []
    for i in range(1, 4):
        texture_path = f"data/enemy/enemy{i}.png"
        texture = arcade.load_texture(texture_path)
        textures.append(texture)

    return Animations(
        textures=textures,
        frame_duration=0.8,
    )

def load_enemy_damage_texture() -> arcade.Texture:
    return arcade.load_texture("data/enemy/damage.png")