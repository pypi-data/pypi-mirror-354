from dataclasses import dataclass, fields
from typing import Any

from typeguard import TypeCheckError, check_type
from typing_extensions import Dict, List, Optional, Self, Type, Union

from simba_sdk.config import Settings
from simba_sdk.core.requests.auth.token_store import InMemoryTokenStore
from simba_sdk.core.requests.client.base import Client


def process_type(value: Any, field_type: Type):
    """
    For any input, and the type of the Dataclass field you want to store that input in, attempt to cast input to type
    """
    if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
        field_types = field_type.__args__
    else:
        field_types = [field_type]
    for i, candidate_type in enumerate(field_types):
        try:
            try:
                # check_type acts like isinstance without freaking out about typing types
                # List == list etc.
                cast_value = check_type(value, candidate_type)
            except TypeCheckError:
                # check for fields that are also dataclasses
                if isinstance(value, dict):
                    # go through the dict and cast each item
                    if (
                        hasattr(candidate_type, "__origin__")
                        and candidate_type.__origin__ is dict
                    ):
                        cast_value = {}
                        for k, v in value.items():
                            key_type, val_type = (
                                candidate_type.__args__
                            )  # args of Dict[str, Base] are (str, Base)
                            cast_value[process_type(k, key_type)] = process_type(
                                v, val_type
                            )
                    else:
                        try:
                            if issubclass(candidate_type, Base):
                                cast_value = candidate_type.from_dict(value)
                        except TypeError:
                            raise TypeError(
                                f"Could not convert input of type {type(value)} to dataclass type {candidate_type}"
                            )
                elif isinstance(value, list):
                    if (
                        hasattr(candidate_type, "__origin__")
                        and candidate_type.__origin__ is list
                    ):
                        # go through the list and cast each item
                        cast_value = []
                        for v in value:
                            val_type = candidate_type.__args__[
                                0
                            ]  # args of List[str] is (str,)
                            cast_value.append(process_type(v, val_type))
                    else:
                        raise TypeError(
                            f"Could not convert input of type {type(value)} to dataclass type {(candidate_type)}"
                        )

                else:
                    # catch any primitives that have been input incorrectly, e.g. "1" -> 1
                    cast_value = candidate_type(value)
        except Exception:
            if i < len(field_types) - 1:
                continue
            raise TypeError(
                f"Could not convert input of type {type(value)} to dataclass type {(candidate_type)}"
            )
        break

    return cast_value


@dataclass
class Base:
    @classmethod
    def from_dict(cls, kwargs: Dict[str, str]):
        """
        Use this method instead of __init__ to ignore extra args
        """
        cls_dict = {}
        for field in fields(cls):
            if field.name not in kwargs:
                continue
            value = kwargs.get(field.name)
            cls_dict[field.name] = process_type(value, field.type)
        return cls(**cls_dict)


class BaseSession:
    def __init__(
        self,
        settings: Optional[Settings] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        **kwargs: str,
    ) -> None:
        if settings is None:
            self.client_id = client_id
            self.client_secret = client_secret
            if client_id:
                kwargs["client_id"] = client_id
            if client_secret:
                kwargs["client_secret"] = client_secret
            self.settings = Settings(**kwargs)
        else:
            self.settings = settings
        self._store = InMemoryTokenStore()
        self._clients: Dict[str, Union[Type[Client], Client]] = {}

    async def initialise_clients(self):
        for service, client in self._clients.items():
            self._clients[service] = client(
                name=service,
                settings=self.settings,
                token_store=self._store,
            )

    async def __aenter__(self) -> Self:
        self._registry: List[BaseSession] = []
        await self.initialise_clients()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._clients = None
        for child in self._registry:
            await child.__aexit__(exc_type, exc_val, exc_tb)
        self._registry = []
