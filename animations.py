from dataclasses import dataclass, field
from time import time
import arcade
import protocols as proto


@dataclass
class Animations(proto.Animations):
    textures: list[arcade.Texture]
    frame_duration: float
    _last_update_time: float = field(init=False, default_factory=time)
    _current_frame_idx: int = field(init=False, default=0)
    _is_playing: bool = field(init=False, default=True)

    @property
    def current_texture(self) -> arcade.Texture:
        return self.textures[self._current_frame_idx]

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    def update(self) -> None:
        current_time = time()
        if current_time - self._last_update_time >= self.frame_duration:
            self._last_update_time = current_time
            self._current_frame_idx += 1
            if self._current_frame_idx >= len(self.textures):
                self._current_frame_idx = 0


    def play(self, restart: bool = True) -> None:
        self._is_playing = True
        if restart:
            self._current_frame_idx = 0
        self._last_update_time = time()
