from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Hashable, Any
from pydantic import BaseModel

from ..domain.entity import IEntity
from ..domain.model import IModel


class RepositoryError(Exception):
    """Base exception for repository operations."""

    pass


class RecordNotFoundError(RepositoryError):
    """Raised when a record is not found."""

    pass


class DuplicateRecordError(RepositoryError):
    """Raised when trying to create a duplicate record."""

    pass


class ICreateSchema(BaseModel):
    """
    Schema for create operations.
    This can be used to specify fields required for creating a new record.
    """

    pass


class IReadSchema(BaseModel):
    """
    Schema for read operations.
    This can be used to specify fields that can be retrieved.
    Schemas should focus on data structure definition only.

    Note: Each ReadSchema should have a corresponding Entity (1:1 relationship).
    """

    pass


class IReadAggregateSchema(BaseModel):
    """
    Schema for read aggregate operations.
    This can be used to specify fields that can be aggregated or summarized.
    Schemas should focus on data structure definition only.

    Note: Each ReadAggregateSchema should have a corresponding Model (1:1 relationship).
    The schema may be built from multiple database tables, but represents one domain model.
    """

    pass


class IUpdateSchema(BaseModel):
    """
    Schema for update operations.
    This can be used to specify fields that can be updated.
    """

    pass


TEntity = TypeVar("TEntity", bound=IEntity)
TModel = TypeVar("TModel", bound=IModel)
TCreateSchema = TypeVar("TCreateSchema", bound=ICreateSchema)
TReadSchema = TypeVar("TReadSchema", bound=IReadSchema)
TReadAggregateSchema = TypeVar("TReadAggregateSchema", bound=IReadAggregateSchema)
TUpdateSchema = TypeVar("TUpdateSchema", bound=IUpdateSchema)


class ICrudRepository(
    ABC,
    Generic[TEntity, TCreateSchema, TReadSchema, TUpdateSchema],
):
    """
    Base interface for CRUD repositories.
    All repositories should implement the basic CRUD operations.
    This repository works with single entities without relationships.
    """

    @abstractmethod
    async def create(self, schema: TCreateSchema) -> TEntity:
        """
        Create a new record.
        """
        raise NotImplementedError

    @abstractmethod
    async def read(self, id: Hashable) -> TEntity:
        """
        Read a record by its ID.
        The ID type should match the entity's TEntityId type parameter.
        Raises RecordNotFoundError if record doesn't exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def read_optional(self, id: Hashable) -> Optional[TEntity]:
        """
        Read a record by its ID, returning None if not found.
        The ID type should match the entity's TEntityId type parameter.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: Hashable, schema: TUpdateSchema) -> TEntity:
        """
        Update a record by its schema.
        The ID type should match the entity's TEntityId type parameter.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: Hashable) -> bool:
        """
        Delete a record by its ID.
        The ID type should match the entity's TEntityId type parameter.
        Returns True if deletion was successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def select(
        self, limit: Optional[int] = None, offset: Optional[int] = None, **filters: Any
    ) -> list[TEntity]:
        """
        Select multiple records with optional pagination and filtering.

        Args:
            limit: Maximum number of records to return. If None, returns all matching records.
            offset: Number of records to skip before returning results.
            **filters: Additional filtering criteria.
        """
        raise NotImplementedError


class IReadRepository(ABC, Generic[TEntity, TReadSchema]):
    """
    Base interface for read-only repositories.
    This repository works with single entities without relationships.
    Use this for simple read operations that return entities.
    """

    @abstractmethod
    async def read(self, id: Hashable) -> TEntity:
        """
        Read an entity by its ID.
        The ID type should match the entity's TEntityId type parameter.
        Raises RecordNotFoundError if entity doesn't exist.

        Returns:
            Single entity without relationships
        """
        raise NotImplementedError

    @abstractmethod
    async def read_optional(self, id: Hashable) -> Optional[TEntity]:
        """
        Read an entity by its ID, returning None if not found.
        The ID type should match the entity's TEntityId type parameter.

        Returns:
            Single entity without relationships, or None if not found
        """
        raise NotImplementedError

    @abstractmethod
    async def select(
        self, limit: Optional[int] = None, offset: Optional[int] = None, **filters: Any
    ) -> list[TEntity]:
        """
        Select multiple entities with optional pagination and filtering.

        Args:
            limit: Maximum number of entities to return. If None, returns all matching entities.
            offset: Number of entities to skip before returning results.
            **filters: Additional filtering criteria.

        Returns:
            List of entities without relationships
        """
        raise NotImplementedError

    def _schema_to_entity(self, schema: TReadSchema) -> TEntity:
        """
        Convert a read schema to an entity.
        This method is recommended to be implemented by concrete repositories to provide
        the conversion logic from schema to entity.

        Args:
            schema: The read schema to convert

        Returns:
            An entity instance converted from the schema

        Note:
            This method is called internally by read operations.
            The typical flow: DB → ReadSchema → Entity → Domain Service

            This method is not abstract to maintain backward compatibility,
            but it's strongly recommended to implement it for consistency
            across different repository implementations.
        """
        raise NotImplementedError(
            "Repository should implement _schema_to_entity method for consistency. "
            "This method provides a standardized way to convert schemas to entities."
        )


class IReadAggregateRepository(ABC, Generic[TModel, TReadAggregateSchema]):
    """
    Base interface for read aggregate repositories.
    This repository works with models that include relationships and aggregated data.
    Use this for complex read operations that return models with relationships.
    """

    @abstractmethod
    async def read(self, id: Hashable) -> TModel:
        """
        Read an aggregate model by its ID.
        The ID type should match the related entity's TEntityId type parameter.
        Raises RecordNotFoundError if model doesn't exist.

        Returns:
            Model with relationships and aggregated data
        """
        raise NotImplementedError

    @abstractmethod
    async def read_optional(self, id: Hashable) -> Optional[TModel]:
        """
        Read an aggregate model by its ID, returning None if not found.
        The ID type should match the related entity's TEntityId type parameter.

        Returns:
            Model with relationships and aggregated data, or None if not found
        """
        raise NotImplementedError

    @abstractmethod
    async def select(
        self, limit: Optional[int] = None, offset: Optional[int] = None, **filters: Any
    ) -> list[TModel]:
        """
        Select multiple aggregate models with optional pagination and filtering.

        Args:
            limit: Maximum number of models to return. If None, returns all matching models.
            offset: Number of models to skip before returning results.
            **filters: Additional filtering criteria.

        Returns:
            List of models with relationships and aggregated data
        """
        raise NotImplementedError

    def _schema_to_model(self, schema: TReadAggregateSchema) -> TModel:
        """
        Convert a read aggregate schema to a model.
        This method is recommended to be implemented by concrete repositories to provide
        the conversion logic from schema to model.

        Args:
            schema: The read aggregate schema to convert

        Returns:
            A model instance converted from the schema

        Note:
            This method is called internally by read operations.
            The typical flow: DB → ReadAggregateSchema → Model → Domain Service

            This method is not abstract to maintain backward compatibility,
            but it's strongly recommended to implement it for consistency
            across different repository implementations.
        """
        raise NotImplementedError(
            "Repository should implement _schema_to_model method for consistency. "
            "This method provides a standardized way to convert schemas to models."
        )
