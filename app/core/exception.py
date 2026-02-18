class AppError(Exception):
    def __init__(
        self,
        *,
        code: str,
        user_message: str,
        dev_message: str | None = None,
        status_code: int,
    ):
        self.code = code
        self.user_message = user_message
        self.dev_message = dev_message
        self.status_code = status_code
        super().__init__(dev_message or user_message)


class AuthError(AppError):
    def __init__(self, *, code, user_message, dev_message=None):
        super().__init__(
            code=code,
            user_message=user_message,
            dev_message=dev_message,
            status_code=401,
        )


class BusinessError(AppError):
    def __init__(self, *, code, user_message, dev_message=None, status_code=400):
        super().__init__(
            code=code,
            user_message=user_message,
            dev_message=dev_message,
            status_code=status_code,
        )