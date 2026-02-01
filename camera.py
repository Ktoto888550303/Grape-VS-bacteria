from attrs import frozen
import arcade
import protocols as proto
from vector import Vector2

MAX_DISTANT_TO_PLAYER = 10


@frozen
class Camera:
    _camera: arcade.camera.Camera2D
    _player: proto.Player

    @property
    def camera(self) -> arcade.camera.Camera2D:
        return self._camera

    def update(self, dt: float) -> None:
        camera_pos = Vector2(*self._camera.position)
        delta = self._player.rigid_body.position - camera_pos
        if delta.length < 0.001:
            return
        speed = delta.length**2 / MAX_DISTANT_TO_PLAYER
        delta_position = delta.normalize * speed * dt
        self._camera.position = (camera_pos + delta_position).tuple