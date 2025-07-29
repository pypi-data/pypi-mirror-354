"""
Pydantic DDD Interface

A Python library providing interface definitions for Domain-Driven Design (DDD)
patterns using Pydantic for type safety and validation.
"""

from packaging.version import parse

__version__ = parse("0.2.0")

# Domain exports
from .domain.entity import IEntity
from .domain.model import IModel
from .domain.service import IDomainService

# Application exports
from .application.usecase import (
    IUseCase,
    IUseCaseCommand,
    IUseCaseResult,
    UseCaseError,
    UseCaseCommandError,
    UseCaseResultError,
    UseCaseExecutionError,
)

# Infrastructure exports
from .infrastructure.repository import (
    ICrudRepository,
    IReadRepository,
    IReadAggregateRepository,
    ICreateSchema,
    IReadSchema,
    IReadAggregateSchema,
    IUpdateSchema,
    RepositoryError,
    RecordNotFoundError,
    DuplicateRecordError,
)

__all__ = [
    # Domain
    "IEntity",
    "IModel",
    "IDomainService",
    # Application
    "IUseCase",
    "IUseCaseCommand",
    "IUseCaseResult",
    "UseCaseError",
    "UseCaseCommandError",
    "UseCaseResultError",
    "UseCaseExecutionError",
    # Infrastructure
    "ICrudRepository",
    "IReadRepository",
    "IReadAggregateRepository",
    "ICreateSchema",
    "IReadSchema",
    "IReadAggregateSchema",
    "IUpdateSchema",
    "RepositoryError",
    "RecordNotFoundError",
    "DuplicateRecordError",
]
