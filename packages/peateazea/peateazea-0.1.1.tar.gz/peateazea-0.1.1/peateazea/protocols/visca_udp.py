from .base import CameraControl
from visca_over_ip import Camera

class ViscaUDP(CameraControl):
    def __init__(self, ip_address, port=5678):
        super().__init__(ip_address, port)
        self._camera = None
    
    @property
    def camera(self):
        if self._camera is None:
            self._camera = Camera(self.ip_address, self.port)

        return self._camera
    
    def close(self):
        if self._camera is not None:
            self._camera.close_connection()
            self._camera = None
    
    def pantilt(self, pan_speed, tilt_speed):
        self.camera.pantilt(pan_speed, tilt_speed, relative=True)

    def zoom(self, zoom_speed):
        self.camera.zoom(zoom_speed)

    def home(self):
        self.camera.home()

    def recall_preset(self, preset_number):
        self.camera.recall_preset(preset_number)

    def save_preset(self, preset_number):
        self.camera.save_preset(preset_number)

    