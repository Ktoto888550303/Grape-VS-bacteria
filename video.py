from time import time
import arcade
from animation import load_video_frames

VIDEO_FPS = 4
FRAME_TIME = 0.25

class Video:
    def __init__(self) -> None:
        self.frames = load_video_frames()
        self.current_frame_idx = 0
        self.last_update_time = 0
        self.is_playing = False
        self.is_finished = False

    def start(self) -> None:
        self.current_frame_idx = 0
        self.last_update_time = time()
        self.is_playing = True
        self.is_finished = False

    def stop(self)  -> None:
        self.is_playing = False
        self.is_finished = True

    def update(self) -> None:
        if not self.is_playing or self.is_finished:
            return

        current_time = time()
        if current_time - self.last_update_time >= FRAME_TIME:
            self.last_update_time = current_time
            self.current_frame_idx += 1

            if self.current_frame_idx >= len(self.frames):
                self.is_finished = True
                self.is_playing = False

    @property
    def current_frame(self) -> arcade.Texture:
        if self.current_frame_idx < len(self.frames):
            return self.frames[self.current_frame_idx]
        return self.frames[-1] if self.frames else None

    def draw(self, center_x: float, center_y: float, width: float, height: float) -> None:
        frame = self.current_frame
        arcade.draw_texture_rect(frame, arcade.rect.XYWH(center_x, center_y, width, height))
