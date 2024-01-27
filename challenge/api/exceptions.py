class Exception(BaseException):
    """
        Base exception for all custom exceptions in this project.

        Attributes:
            status_code (str): HTTP code representing the error.
            msg (int): Coloquial message of error.
            es_msg (str, optional): Mensaje coloquial que describe el error.
    """

    def __init__(
        self,
        status_code: int,
        msg: str,
        es_msg: str = ''
    ):
        """
            Args:
                status_code (str): HTTP code representing the error.
                msg (int): Coloquial message of error.
                es_msg (str, optional): Mensaje coloquial que describe el error.
        """
        super().__init__()
        self.status_code = status_code
        self.msg = msg
        self.es_msg = es_msg


class UserAlreadyExistsException(Exception):
    """
        Exception used when a user already exists

        Attributes:
            status_code (str): HTTP code representing the error.
            msg (int): Coloquial message of error.
            es_msg (str, optional): Mensaje coloquial que describe el error.
    """

    def __init__(self):
        super().__init__(
            400,
            'User already exists.',
            'El usuario ya existe.'
        )


class PasswordsDoNotMatchException(Exception):
    """
        Exception used when passwords do not match

        Attributes:
            status_code (str): HTTP code representing the error.
            msg (int): Coloquial message of error.
            es_msg (str, optional): Mensaje coloquial que describe el error.
    """

    def __init__(self):
        super().__init__(
            400,
            'Passwords do not match.',
            'Las contraseñas no coinciden.'
        )


class UsernameOrPasswordIncorrectException(Exception):
    """
        Exception used when username or password are incorrect

        Attributes:
            status_code (str): HTTP code representing the error.
            msg (int): Coloquial message of error.
            es_msg (str, optional): Mensaje coloquial que describe el error.
    """

    def __init__(self):
        super().__init__(
            400,
            'Username or password incorrect.',
            'Usuario o contraseña incorrectos.'
        )
