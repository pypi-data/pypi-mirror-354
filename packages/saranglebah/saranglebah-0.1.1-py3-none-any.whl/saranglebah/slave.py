import json
import socket
from pynput.keyboard import Controller, Key
from .logger import get_logger

def run_slave(port: int = 5050) -> None:
    logger = get_logger("saranglebah.slave")
    logger.info("Starting slave. Listening on port %d", port)

    keyboard = Controller()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))

    while True:
        try:
            data, _ = sock.recvfrom(1024)
            message = json.loads(data.decode())
            key_str = message["key"]

            if len(key_str) == 1:
                keyboard.press(key_str)
                keyboard.release(key_str)
            elif key_str.startswith("Key."):
                key_name = key_str.replace("Key.", "")
                key_attr = getattr(Key, key_name, None)
                if key_attr:
                    keyboard.press(key_attr)
                    keyboard.release(key_attr)
            logger.debug("Simulated %s", key_str)
        except Exception as e:
            logger.error("Error processing packet: %s", e)
