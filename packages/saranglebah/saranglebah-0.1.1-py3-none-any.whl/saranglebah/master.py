import json
import socket
from typing import List
from pynput import keyboard
from .logger import get_logger

def run_master(slaves: List[str], port: int = 5050) -> None:
    logger = get_logger("saranglebah.master")
    logger.info("Starting master. Broadcasting to %s on port %d", slaves, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def on_press(key):
        try:
            payload = json.dumps({"key": key.char})
        except AttributeError:
            payload = json.dumps({"key": str(key)})

        for ip in slaves:
            try:
                sock.sendto(payload.encode(), (ip, port))
            except Exception as e:
                logger.error("Failed to send to %s: %s", ip, e)

    with keyboard.Listener(on_press=on_press) as listener:
        logger.info("Listener ready. Press ESC to stop.")
        listener.join()
