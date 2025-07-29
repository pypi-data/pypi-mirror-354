from .base import CameraControl
import socket
import time

class Visca(CameraControl):
    def __init__(self, ip_address, port=5678):
        """Initialize TCP VISCA over IP connection"""
        super().__init__(ip_address, port)
        self.socket = None

    def connect(self):
        """Establish TCP connection to camera"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_address, self.port))
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.socket = None

    def send_command(self, command):
        """Send VISCA command and receive response"""
        if not self.socket:
            self.connect()

        # Print as ord values
        print("Bytes: ", end="")
        for byte in command:
            print(f"{byte}", end=" ")
        print(f" | Hex: {command.hex()}")
        
        try:
            self.socket.send(command)
            return True
        except Exception as e:
            self.socket = None
            return False
        
    @property
    def power(self):
        
        """Get camera power state"""
        return None
    
    @power.setter
    def power(self, state):
        """Control camera power state
        
        Args:
            state (bool): True to turn on, False to turn off
        """
        
        state = "02" if state else "03"

        command = bytes.fromhex(f'81 01 04 00 {state} FF')
        return self.send_command(command)

    def pantilt(self, pan_speed, tilt_speed):
        """Control pan/tilt movement. Speed range: -24 to 24"""
        pan_speed = max(-24, min(24, pan_speed))
        tilt_speed = max(-24, min(24, tilt_speed))
        
        # Convert speeds to hex values
        pan_hex = format(abs(pan_speed), '02x') if pan_speed >= 0 else format(abs(pan_speed), '02x')
        tilt_hex = format(abs(tilt_speed), '02x') if tilt_speed >= 0 else format(abs(tilt_speed), '02x')
        
        command = bytes.fromhex(f'81 01 06 03 {pan_hex} {tilt_hex} 00 00 00 00 00 00 00 00 FF')

        return self.send_command(command)
    
    def home(self):
        """Move camera to home position"""
        command = bytes.fromhex('81 01 06 04 FF')
        return self.send_command(command)

    def zoom(self, speed):
        """Control zoom. Speed range: -7 to 7"""
        speed = max(-7, min(7, speed))
        speed_hex = format(abs(speed), '02x') if speed >= 0 else format(abs(speed), '02x')
        
        command = bytes.fromhex(f'81 01 04 47 {speed_hex} 00 00 00 00 FF')
        return self.send_command(command)

    def stop(self):
        """Stop all camera movement"""
        command = bytes.fromhex('81 01 06 03 00 00 00 00 00 00 00 00 00 00 FF')
        return self.send_command(command)
    
    def reset(self):
        """Reset camera defaults"""
        command = bytes.fromhex('81 01 06 05 FF')
        return self.send_command(command)

    def save_preset(self, preset_num):
        """Save current position as preset"""
        if not 0 <= preset_num <= 127:
            return False
        
        preset_hex = format(preset_num, '02x')
        command = bytes.fromhex(f'81 01 04 3F 01 {preset_hex} FF')
        return self.send_command(command)

    def recall_preset(self, preset_num):
        """Move camera to saved preset position"""
        if not 0 <= preset_num <= 127:
            return False
            
        preset_hex = format(preset_num, '02x')
        command = bytes.fromhex(f'81 01 04 3F 02 {preset_hex} FF')
        return self.send_command(command)

    def __del__(self):
        """Clean up socket connection"""
        if self.socket:
            self.socket.close()