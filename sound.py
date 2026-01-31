import arcade
from pathlib import Path


class Sound:
    def __init__(self) -> None:
        self.hit_enemy_sound = arcade.load_sound(Path("data") / "sound" / "hit_enemy.mp3")
        self.hit_player_sound = arcade.load_sound(Path("data") / "sound" / "hit_player.mp3")
        self.player_dead_sound = arcade.load_sound(Path("data") / "sound" / "player_death.mp3")
        self.background_music = arcade.load_sound(Path("data") / "sound" / "background_music.mp3")
        self.attack = arcade.load_sound(Path("data") / "sound" / "attack.mp3")
        self.background_volume = 0.3
        self.other_volume = 0.6
        self.dead = 1
        self.background_music_player = None

    def play_background_music(self) -> None:
        self.background_music_player = self.background_music.play(volume=self.background_volume)

    def stop_background_music(self) -> None:
        if self.background_music_player and self.background_music_player.playing:
            self.background_music_player.pause()

    def play_attack(self) -> None:
        self.attack.play(volume=self.other_volume)

    def play_hit_enemy(self) -> None:
        self.hit_enemy_sound.play(volume=self.other_volume, speed=2)

    def play_hit_player(self) -> None:
        self.hit_player_sound.play(volume=self.other_volume)

    def play_player_dead(self) -> None:
        self.player_dead_sound.play(volume=self.dead)
