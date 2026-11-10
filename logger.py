from datetime import datetime


class GestureLogger:
    def __init__(self, filename="messages.txt"):
        self.filename = filename
        self.last_message = None

    def log(self, message):
        """Write the message to the file only if it changed."""
        if message == self.last_message:
            return
        self.last_message = message
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{time}] {message}\n")
