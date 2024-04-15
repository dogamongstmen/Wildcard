


from application.routes.api.responsetypes.base import SerializableResponse


class BaseErrorResponse(SerializableResponse):
    error: str


class MalformedRequestErrorResponse(BaseErrorResponse):
    def __init__(self) -> None:
        super().__init__()
        self.error = "Malformed request body."


class FieldErrorResponse(BaseErrorResponse):
    def __init__(self, field_name: str) -> None:
        super().__init__()
        self.error = f"Request body must contain a(n) `{field_name}` field."


class InternalServerErrorResponse(BaseErrorResponse):
    def __init__(self) -> None:
        super().__init__()
        self.error = "Internal server error."


class NotFoundErrorResponse(BaseErrorResponse):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.error = msg
