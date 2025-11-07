# Docker Scraper

A lightweight systemd service that monitors Docker container creation events and logs their metadata. Designed for ingestion into Splunk or other log management systems.

## Overview

Docker Scraper listens to the Docker daemon for container creation events and extracts comprehensive metadata about each new container. The service runs continuously in the background as a systemd service, making it ideal for system monitoring and security auditing.

## Features

- **Real-time Monitoring**: Listens for Docker container creation events in real-time
- **Comprehensive Metadata**: Captures detailed container information including:
  - Container ID, name, and image details
  - Labels and environment variables
  - Command, entrypoint, and working directory
  - Hostname and platform information
  - Creation timestamp
- **Systemd Integration**: Runs as a system service with automatic restart on failure
- **Structured Logging**: Outputs to systemd journal for easy log aggregation
- **Debian Package**: Easy installation and removal via dpkg

## Requirements

- **Operating System**: Debian/Ubuntu-based Linux distribution
- **Python**: Python 3.8 or higher
- **Docker**: Docker Engine (docker.io or docker-ce)
- **Systemd**: For service management

## Installation

### From .deb Package

1. Download or build the package:
   ```bash
   ./build-deb.sh
   ```

2. Install the package:
   ```bash
   sudo dpkg -i docker-scraper_1.0.0_all.deb
   ```

3. Start the service:
   ```bash
   sudo systemctl start docker-scraper
   sudo systemctl enable docker-scraper
   ```

### Manual Installation

If you prefer to install manually without the package:

1. Copy files to `/opt/docker-scraper/`
2. Create a Python virtual environment:
   ```bash
   cd /opt/docker-scraper
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Copy the systemd service file:
   ```bash
   sudo cp debian-package/etc/systemd/system/docker-scraper.service /etc/systemd/system/
   sudo systemctl daemon-reload
   ```

4. Start the service:
   ```bash
   sudo systemctl start docker-scraper
   sudo systemctl enable docker-scraper
   ```

## Usage

### Service Management

Check service status:
```bash
sudo systemctl status docker-scraper
```

View logs:
```bash
sudo journalctl -u docker-scraper -f
```

Stop the service:
```bash
sudo systemctl stop docker-scraper
```

Restart the service:
```bash
sudo systemctl restart docker-scraper
```

### Viewing Container Events

The service logs all detected container creation events to the systemd journal. View them with:

```bash
# Follow logs in real-time
sudo journalctl -u docker-scraper -f

# View recent logs
sudo journalctl -u docker-scraper -n 100

# View logs from specific time
sudo journalctl -u docker-scraper --since "1 hour ago"
```

### Example Output

When a container is created, you'll see log entries like:

```
Nov 06 12:34:56 hostname docker-scraper[1234]: 2025-11-06 12:34:56,789 - INFO - Connected to Docker daemon
Nov 06 12:34:56 hostname docker-scraper[1234]: 2025-11-06 12:34:56,790 - INFO - Listening for container creation events
Nov 06 12:35:10 hostname docker-scraper[1234]: 2025-11-06 12:35:10,123 - INFO - Detected new container creation: a1b2c3d4e5f6
```

## Building the Debian Package

The project includes a build script for creating the .deb package:

```bash
./build-deb.sh
```

This will:
- Create a properly structured Debian package
- Set correct file permissions
- Fix line endings for WSL/Windows compatibility
- Build `docker-scraper_1.0.0_all.deb`

### Package Information

- **Package Name**: docker-scraper
- **Version**: 1.0.0
- **Architecture**: all
- **Section**: admin
- **Priority**: optional

## Uninstallation

To remove the package:

```bash
sudo dpkg -r docker-scraper
```

This will:
- Stop and disable the systemd service
- Remove the virtual environment
- Remove all package files

## Architecture

### Components

- **main.py**: Core Python script that connects to Docker daemon and monitors events
- **systemd service**: Ensures the scraper runs continuously and restarts on failure
- **Virtual environment**: Isolated Python environment with required dependencies

### File Locations

- **Installation directory**: `/opt/docker-scraper/`
- **Service file**: `/etc/systemd/system/docker-scraper.service`
- **Logs**: Systemd journal (view with `journalctl`)

## Security Considerations

The service includes security settings in the systemd unit:
- `NoNewPrivileges=true`: Prevents privilege escalation
- `PrivateTmp=true`: Uses private /tmp directory
- Runs as root (required for Docker socket access)

**Note**: The service requires root access to communicate with the Docker daemon. Ensure your Docker installation follows security best practices.

## Troubleshooting

### Service won't start

Check if Docker is running:
```bash
sudo systemctl status docker
```

Verify Docker socket permissions:
```bash
ls -la /var/run/docker.sock
```

### No events being logged

Test Docker events manually:
```bash
docker events --filter event=create
```

Then create a test container:
```bash
docker run --rm hello-world
```

### Permission errors

Ensure the service has access to the Docker socket. The service runs as root by default, which should have access. Check Docker group membership if needed:
```bash
groups
```

## Development

### Project Structure

```
docker-scraper/
├── build-deb.sh              # Package build script
├── README.md                 # This file
└── debian-package/
    ├── DEBIAN/
    │   ├── control          # Package metadata
    │   ├── postinst         # Post-installation script
    │   └── prerm            # Pre-removal script
    ├── etc/
    │   └── systemd/
    │       └── system/
    │           └── docker-scraper.service
    └── opt/
        └── docker-scraper/
            ├── main.py
            ├── requirements.txt
            ├── LICENSE.md
            └── README.md
```

### Dependencies

- `docker>=7.0.0`: Docker SDK for Python

### Contributing

1. Make changes to the source files in `debian-package/opt/docker-scraper/`
2. Update version in `debian-package/DEBIAN/control` and `build-deb.sh`
3. Test changes
4. Build and test the package

## License

See LICENSE.md for details.

## Author

Andrew Spence

## Changelog

### Version 1.0.0
- Initial release
- Real-time Docker container creation monitoring
- Systemd service integration
- Debian package support
