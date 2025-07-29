from pydantic import BaseModel


class IModel(BaseModel):
    """
    Base class for domain models.
    All domain models should inherit from this class.
    This can be used to define common fields or methods for all domain models.
    """

    pass
