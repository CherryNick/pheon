from dataclasses import dataclass

from src.app_config import Config
from src.extensions.access_token import AccessToken


@dataclass(slots=True)
class BaseController:
    config: Config

@dataclass(slots=True)
class BaseAuthController(BaseController):
    token: AccessToken
