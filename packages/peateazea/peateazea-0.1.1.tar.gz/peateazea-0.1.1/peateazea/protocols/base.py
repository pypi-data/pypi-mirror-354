class CameraControl:
    def __init__(self, ip_address, port):
        """Initialize camera connection"""
        self.ip_address = ip_address
        self.port = port

    def connect(self):
        """Establish connection to camera. This should be automatically called by individual methods to keep and maintain connection."""
        raise NotImplementedError("Subclass must implement connect()")

    def send_command(self, command):
        """Send command to camera"""
        raise NotImplementedError("Subclass must implement send_command()")

    # Pan/Tilt Control Methods
    def pantilt(self, pan_speed, tilt_speed):
        """Control pan/tilt movement"""
        raise NotImplementedError("Subclass must implement pan_tilt()")

    def stop(self):
        """Stop all camera movement"""
        self.pantilt(0, 0)
        self.zoom(0)

    # Power Control Methods
    @property
    def power(self):
        """Get camera power state"""
        raise NotImplementedError("Subclass must implement power()")
    
    @power.setter
    def power(self, state):
        """Control camera power state"""
        raise NotImplementedError("Subclass must implement power()")

    # Zoom Control Methods
    def zoom(self, speed):
        """Control zoom"""
        raise NotImplementedError("Subclass must implement zoom()")

    # Preset Methods
    def save_preset(self, preset_num):
        """Save current position as preset"""
        raise NotImplementedError("Subclass must implement set_preset()")

    def recall_preset(self, preset_num):
        """Move camera to saved preset position"""
        raise NotImplementedError("Subclass must implement recall_preset()")

    def home(self):
        """Move camera to home position"""
        raise NotImplementedError("Subclass must implement home()")
    
    def close(self):
        """Close connection to camera"""
        raise NotImplementedError("Subclass must implement close()")

    def __del__(self):
        """Clean up connection"""
        self.close()
