# Python Keylogger

A simple keylogger implementation in Python that captures keyboard inputs and clipboard changes.

## Features

- Keyboard input monitoring
- Clipboard monitoring
- Windows persistence
- Silent background operation
- Error handling and logging
- Clean shutdown with Ctrl+C

## Prerequisites

- Python 3.7 or higher
- Windows operating system

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yusufdalbudak/keylogger.git
cd keylogger
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the keylogger:
```bash
python main.py
```

The program will:
- Start running silently in the background
- Create a `keylog.txt` file in the same directory
- Log all keyboard inputs and clipboard changes
- Press ESC to stop the keylogger

## Log File Format

Each entry in `keylog.txt` follows this format:
```
YYYY-MM-DD HH:MM:SS - Key pressed: [key]
YYYY-MM-DD HH:MM:SS - Special key pressed: [special_key]
YYYY-MM-DD HH:MM:SS - Clipboard changed: [clipboard_content]
```

## Security Note

This tool is for educational purposes only. Use responsibly and ethically.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 