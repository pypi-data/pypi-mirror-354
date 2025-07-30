from .vault import Vault
from .models import Secret

vault:Vault = Vault()

__all__ = [
    "vault",
    "Secret",
    ]