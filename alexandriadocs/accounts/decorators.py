from accounts.register import access_checker_register


def access_checker(model_class):
    def wrapped(checker_class):
        access_checker_register.register(model_class, checker_class)
        return checker_class
    return wrapped
