# Peateazea

A Python package for controlling PTZ (Pan-Tilt-Zoom) cameras through various protocols. Currently supports Avkans cameras, VISCA, and VISCA over UDP.

## Features

- Multi-protocol support:
  - Avkans cameras
  - VISCA (TCP)
  - VISCA over UDP
- Basic PTZ controls (pan, tilt, zoom)
- Preset position recall
- Home position support
- Simple, unified API across different protocols

## Installation

Install using pip:

```bash
pip install peateazea
```

Or install from source:

```bash
git clone https://github.com/benbaptist/peateazea.git
cd peateazea
pip install -e .
```

## Requirements

- Python 3.9 or higher
- `requests`
- `visca-over-ip`

## Usage

### Basic Example

```python
from peateazea import Avkans, Visca, ViscaUDP

# For Avkans cameras
camera = Avkans("192.168.1.100", 80, username="admin", password="password")

# For VISCA over TCP
camera = Visca("192.168.1.100", 1259)

# For VISCA over UDP
camera = ViscaUDP("192.168.1.100", 52381)

# Basic controls
camera.pantilt(-12, 0)  # Pan left
camera.pantilt(12, 0)   # Pan right
camera.pantilt(0, -12)  # Tilt up
camera.pantilt(0, 12)   # Tilt down

camera.zoom(7)    # Zoom in
camera.zoom(-7)   # Zoom out

camera.stop()     # Stop all movement
camera.home()     # Return to home position

# Recall preset position
camera.recall_preset(1)
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.