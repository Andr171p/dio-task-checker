import logging

from src.api.app import get_litestar_app


logging.basicConfig(level=logging.INFO)

app = get_litestar_app()
