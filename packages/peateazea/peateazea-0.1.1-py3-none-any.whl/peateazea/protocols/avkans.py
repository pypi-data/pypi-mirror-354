from .base import CameraControl

import requests

class Avkans(CameraControl):
    """Avkans camera control through undocumented RESTful API"""
    def __init__(self, ip_address, port, username="admin", password="admin123"):
        super().__init__(ip_address, port)

        self._username = username
        self._password = password

        self._auth_token = None
        self._base_url = f"http://{ip_address}:{port}"
        self._headers = {
            "Content-Type": "application/json"
        }

    def connect(self):
        self.login()

    def login(self):
        """Login to camera and get auth token"""
        data = {
            "username": self._username,
            "password": self._password,
            "remember": True
        }

        response = self._post("/api/auth/login", data)

        self._auth_token = response["data"]["token"]
        self._headers["Authorization"] = f"Bearer {self._auth_token}"

    def recall_preset(self, preset_id, pan_speed=5, tilt_speed=0):
        """Recall a preset position"""
        if not self._auth_token:
            self.login()
            
        data = {
            "method": "recall",
            "id": preset_id,
            "pan_speed": pan_speed,
            "tilt_speed": tilt_speed
        }
        self._post("/api/pt/point", data)

    def pantilt_raw(self, pan_dir, tilt_dir, pan_speed, tilt_speed):
        """Move camera relatively in pan/tilt direction"""
        if not self._auth_token:
            self.login()

        data = {
            "pan_dir": pan_dir,
            "tilt_dir": tilt_dir,
            "pan_speed": pan_speed,
            "tilt_speed": tilt_speed
        }
        self._post("/api/pt/move-rel", data)

    def pantilt(self, pan_speed, tilt_speed):
        """Move camera relatively in pan/tilt direction"""
        if not self._auth_token:
            self.login()

        # Calculate pan and tilt directions
        pan_dir = 1 if pan_speed > 0 else -1
        tilt_dir = 1 if tilt_speed > 0 else -1

        if pan_speed == 0:
            pan_dir = 0
        if tilt_speed == 0:
            tilt_dir = 0

        # Ensure pan and tilt speeds are always positive
        pan_speed = abs(pan_speed)
        tilt_speed = abs(tilt_speed)
            
        data = {
            "pan_dir": pan_dir,
            "tilt_dir": tilt_dir,
            "pan_speed": pan_speed,
            "tilt_speed": tilt_speed
        }

        print(data)
        self._post("/api/pt/move-rel", data)

    def zoom(self, zoom_speed):
        """Zoom camera relatively"""
        assert zoom_speed < 8 and zoom_speed > -8, "Zoom speed must be between -7 and 7"

        if not self._auth_token:
            self.login()

        zoom_dir = 1 if zoom_speed > 0 else -1

        if zoom_speed == 0:
            zoom_dir = 0
            
        data = {
            "zoom_dir": zoom_dir,
            "zoom_speed": zoom_speed
        }

        print(data)

        self._post("/api/pt/zoom-rel", data)

    def home(self):
        """Move camera to home position"""
        self._post("/api/pt/point", {"method": "home"})

    def _post(self, endpoint, data):
        """Helper method to make POST requests"""
        url = self._base_url + endpoint
        response = requests.post(url, json=data, headers=self._headers)
        response.raise_for_status()
        return response.json()
    
    def __del__(self):
        pass