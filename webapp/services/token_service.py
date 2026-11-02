import base64
import os


class TokenService:
    def generate(self, length: int = 20) -> str:
        return base64.b64encode(os.urandom(64))[:length].decode('utf-8')
