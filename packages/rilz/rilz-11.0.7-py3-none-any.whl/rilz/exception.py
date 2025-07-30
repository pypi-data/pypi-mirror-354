"""Rilz Exception Module"""

class RilzException(Exception):
    def __init__(self, message, code = 0, type = None, response = None):
        self.message = message
        self.code = code
        self.type = type
        self.response = response
        super().__init__(self.message)

class VaultNotFound(RilzException):
    """Vault not found exception."""
    def __init__(self, message="Vault not found. Please create a database named 'vault'.", code=404, type='vault_not_found', response=None):
        super().__init__(message, code, type, response)

class VaultValueNotFound(RilzException):
    """Vault value not found exception."""
    def __init__(self, name, kwargs=None, message=None, code=404, type='vault_value_not_found', response=None):
        if message is None:
            message = f"Vault value with name '{name}' and parameters {kwargs} not found."
        super().__init__(message, code, type, response)
        self.name = name
        self.kwargs = kwargs