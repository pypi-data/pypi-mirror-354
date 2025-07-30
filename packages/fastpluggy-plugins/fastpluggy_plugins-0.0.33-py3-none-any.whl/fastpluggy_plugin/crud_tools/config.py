from typing import Optional

from fastpluggy.core.config import BaseDatabaseSettings


class CrudConfig(BaseDatabaseSettings):
    require_authentication = True

    base_sqlalchemy_model : Optional[str] = None