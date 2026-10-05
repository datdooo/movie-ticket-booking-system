class AppError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class ConflictError(AppError):
    pass


class ForbiddenError(AppError):
    pass


class NotFoundError(AppError):
    pass


class RuleViolationError(AppError):
    pass


class UnauthorizedError(AppError):
    pass


class FeatureNotReadyError(AppError):
    pass
