from abc import ABC
from typing import Any, Hashable, Generic, TypeVar
from pydantic import BaseModel


TEntityId = TypeVar("TEntityId", bound=Hashable)


class IEntity(BaseModel, Generic[TEntityId], ABC):
    """
    Base class for entities.
    All entities should inherit from this class and define their identity field.

    Entities are objects that have a distinct identity that runs through time
    and different states. They are defined by their identity, not their attributes.
    """

    id: TEntityId

    def __eq__(self, other: Any) -> bool:
        """
        Compare entities based on their identity.
        Two entities are equal if they have the same type and ID.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Hash entities based on their identity.
        """
        return hash((self.__class__, self.id))
