from litestar import Litestar
from dishka.integrations.litestar import setup_dishka

from src.api.v1.controllers import TaskController
from src.di.container import container


def get_litestar_app() -> Litestar:
    app = Litestar(route_handlers=[TaskController])
    setup_dishka(app=app, container=container)
    return app
