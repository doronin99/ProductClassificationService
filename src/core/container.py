from dependency_injector import containers, providers

from src.core.config import configs
from src.core.database import Database
from src.repository import *
from src.services import *


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.endpoints.auth",
            "core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)

