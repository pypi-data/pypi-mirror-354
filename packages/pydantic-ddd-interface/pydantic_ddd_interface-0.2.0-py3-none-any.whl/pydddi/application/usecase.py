from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Optional
from pydantic import BaseModel


class UseCaseError(Exception):
    """
    Base exception for use case operations.
    This can be used to indicate general errors in use case execution.
    """

    pass


class UseCaseCommandError(UseCaseError):
    """
    Exception raised when there is an error in the use case command.
    This can be used to indicate validation errors or other issues with the command.
    """

    pass


class UseCaseResultError(UseCaseError):
    """
    Exception raised when there is an error in the use case result.
    This can be used to indicate validation errors or other issues with the result.
    """

    pass


class UseCaseExecutionError(UseCaseError):
    """
    Exception raised when there is an error during the execution of a use case.
    This can be used to indicate that the use case could not be executed successfully.
    """

    pass


class IUseCaseCommand(BaseModel):
    """
    Base class for use case commands.
    All use case commands should inherit from this class.

    Raises:
        UseCaseCommandError: If there is an error in the command data
    """

    pass


class IUseCaseResult(BaseModel):
    """
    Base class for use case results.
    All use case results should inherit from this class.

    Raises:
        UseCaseResultError: If there is an error in the result data
    """

    pass


# 型変数を定義
TCommand = TypeVar("TCommand", bound=IUseCaseCommand)
TResult = TypeVar("TResult", bound=IUseCaseResult)


class IUseCase(ABC, Generic[TCommand, TResult]):
    """
    Base interface for use cases.
    All use cases should implement the execute method.
    """

    @abstractmethod
    async def execute(self, command: TCommand) -> TResult:
        """
        Execute the use case with the given command.

        Args:
            command: The command containing input data for the use case

        Raises:
            UseCaseExecutionError: If there is an error during execution

        Returns:
            The result of the use case execution
        """
        raise NotImplementedError("Use case must implement the execute method.")
