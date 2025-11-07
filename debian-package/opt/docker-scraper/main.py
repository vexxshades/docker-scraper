#!/opt/docker-scraper/venv/bin/python3
import docker
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

OUTPUT_FILE = Path("container_events.json")


def get_container_metadata(container):
    try:
        container.reload()  
        attrs = container.attrs
        
        metadata = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "container_created",
            "container_id": container.id,
            "container_name": container.name,
            "short_id": container.short_id,
            "image": attrs.get("Config", {}).get("Image"),
            "image_id": attrs.get("Image"),
            "created": attrs.get("Created"),
            "labels": attrs.get("Config", {}).get("Labels", {}),
            "environment": attrs.get("Config", {}).get("Env", []),
            "command": attrs.get("Config", {}).get("Cmd"),
            "entrypoint": attrs.get("Config", {}).get("Entrypoint"),
            "working_dir": attrs.get("Config", {}).get("WorkingDir"),
            "hostname": attrs.get("Config", {}).get("Hostname"),
            "platform": attrs.get("Platform"),
        }
        
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata for container {container.id}: {e}")
        return None

def listen_for_container_events():
    """
    Listen for Docker container creation events and log metadata.
    """
    try:
        client = docker.from_env()
        logger.info("Connected to Docker daemon")
        logger.info(f"Listening for container creation events. Logging to: {OUTPUT_FILE.absolute()}")

        for event in client.events(decode=True, filters={"type": "container", "event": "create"}):
            try:
                container_id = event.get("id")
                logger.info(f"Detected new container creation: {container_id[:12]}")
                container = client.containers.get(container_id)
                metadata = get_container_metadata(container)
                    
            except docker.errors.NotFound:
                logger.warning(f"Container {container_id[:12]} not found (may have been removed)")
            except Exception as e:
                logger.error(f"Error processing event: {e}")
                
    except docker.errors.DockerException as e:
        logger.error(f"Docker error: {e}")
        logger.error("Make sure Docker is running and accessible")
    except KeyboardInterrupt:
        logger.info("\nStopping event listener...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    listen_for_container_events()
