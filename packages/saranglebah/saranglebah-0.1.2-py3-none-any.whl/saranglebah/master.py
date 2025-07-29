import json
import socket
from typing import List
from pynput import keyboard
from pynput.keyboard import Key
from .logger import get_logger

def run_master(slaves: List[str], port: int = 5050) -> None:
    logger = get_logger("saranglebah.master")
    logger.info("Starting master. Broadcasting to %s on port %d", slaves, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    pressed_keys = set()

    def on_press(key):
        pressed_keys.add(key)

        # Check for Ctrl + F12
        if (Key.ctrl_l in pressed_keys or Key.ctrl_r in pressed_keys) and key == Key.f12:
            print("Ctrl + F12 detected — exiting.")
            logger.info("Ctrl + F12 pressed. Exiting master.")
            return False  # This stops the listener

        try:
            payload = json.dumps({"key": key.char})
        except AttributeError:
            payload = json.dumps({"key": str(key)})

        for ip in slaves:
            try:
                sock.sendto(payload.encode(), (ip, port))
            except Exception as e:
                logger.error("Failed to send to %s: %s", ip, e)

    def on_release(key):
        pressed_keys.discard(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        logger.info("Listener ready. Press Ctrl+F12 to stop.")
        listener.join()
