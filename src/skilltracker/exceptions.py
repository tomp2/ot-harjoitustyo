class LoginUserInputError(Exception):
    pass


class UserNotFoundError(LoginUserInputError):
    pass


class InvalidPasswordError(LoginUserInputError):
    pass


class UserInputValidationError(LoginUserInputError):
    pass


class UsernameTakenError(LoginUserInputError):
    pass
