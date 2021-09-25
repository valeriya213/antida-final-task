class BaseServiceError(Exception):
    pass


class ClientError(BaseServiceError):
    pass


class ServerError(BaseServiceError):
    pass


class EntityConflictError(ClientError):
    pass


class EntiyDoesNotExistError(ClientError):
    pass


class EntiyUnprocessableError(ClientError):
    pass
