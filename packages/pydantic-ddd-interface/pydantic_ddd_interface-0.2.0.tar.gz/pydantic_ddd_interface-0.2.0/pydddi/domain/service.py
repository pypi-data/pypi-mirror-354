from abc import ABC, abstractmethod
from typing import Any, Optional


class IDomainService(ABC):
    """
    Abstract base class for domain services.

    Domain services encapsulate domain logic that doesn't naturally fit
    within an entity or value object. They are stateless and express
    domain concepts that span multiple entities.
    """

    pass
