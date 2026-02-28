import logging

from file_uploader.settings import Settings

logger = logging.getLogger()
settings = Settings()

"""
# Example:

class ExampleService:
    def __init__(self):
        self.client = SomeHTTPClient()

    async def do_something(self, info: str):
        await self.client.send_info(info)
"""
