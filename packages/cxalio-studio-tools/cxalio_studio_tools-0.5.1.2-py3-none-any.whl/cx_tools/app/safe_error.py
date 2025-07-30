class SafeError(Exception):
    def __init__(self, message: str | None = None, style: str | None = None):
        super().__init__(message)
        self.message = message
        self.style = style
