class APIKeyWarning(UserWarning):
    pass


class NoResponseData(UserWarning):
    pass


class ExceptionAPI(Exception):
    pass


class ExceptionChatFunction(Exception):
    pass