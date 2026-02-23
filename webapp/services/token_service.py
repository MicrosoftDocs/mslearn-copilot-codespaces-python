import os
import base64


class TokenService:
    def generate(self, length: int = 20) -> str:
        """Generate a pseudo-random base64-encoded token of the given length."""
        return base64.b64encode(os.urandom(64))[:length].decode('utf-8')
