import logging

from src.dio_task_checker.app import create_fastapi_app


logging.basicConfig(level=logging.INFO)

app = create_fastapi_app()
