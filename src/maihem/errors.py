class ChatFunctionError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AgentTargetCreateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AgentTargetGetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TestCreateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
