from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, FastAPI

from src.core.metrics import MetricsSettings, instrument_app
from src.core.storage.mongo_storage import (
    MongoSettings,
    MongoStorage,
    get_mongo_storage,
)


class Mvp:
    __instance__: Optional[Mvp] = None

    def __init__(
        self,
        fastapi_app: FastAPI,
        mongo_storage: Optional[MongoStorage] = None,
    ) -> None:
        self.__fastapi_app = fastapi_app  # pylint: disable=unused-private-member
        self.__mongo_storage = mongo_storage

    def mongo(self) -> MongoStorage:
        if self.__mongo_storage is None:
            err = "Provide mongo settings to Mvp.setup() to use MongoDB."
            raise RuntimeError(err)

        return self.__mongo_storage

    @classmethod
    def setup(
        cls,
        app: FastAPI,
        mongo: Optional[MongoSettings] = None,
        metrics: Optional[MetricsSettings] = None,
    ) -> None:
        mongo_storage = get_mongo_storage(mongo) if mongo else None

        if metrics:
            instrument_app(app, metrics)

        cls.__instance__ = cls(
            fastapi_app=app,
            mongo_storage=mongo_storage,
        )


def get_mvp() -> Mvp:
    if Mvp.__instance__ is None:
        err = "MVP is not set up, call Mvp.setup() after FastAPI app is initialized."
        raise RuntimeError(err)
    return Mvp.__instance__


MvpDep = Annotated[Mvp, Depends(get_mvp)]
