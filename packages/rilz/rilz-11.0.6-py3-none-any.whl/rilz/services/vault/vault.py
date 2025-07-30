import hvac
from hvac.exceptions import InvalidPath, Forbidden
import os
from . import exceptions
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, SecretStr, Secret

VAULT_URL= os.environ.get("VAULT_URL", None)
if VAULT_URL is None:
    raise ValueError("VAULT_URL environment variable must be set.")

@dataclass
class CredUserPass:
    """
    Class to handle user and password credentials.
    """
    username: str
    password: str

@dataclass
class CredToken:
    """
    Class to handle token credentials.
    """
    token: str
    

def get_auth() -> CredUserPass | CredToken:
    """
    Get the authentication method.
    """
    print("Getting authentication method...2")
    token = os.environ.get("VAULT_TOKEN")
    user, password = os.environ.get("VAULT_USER"), os.environ.get("VAULT_PASSWORD")
    if token:
        print("Using token authentication...3")
        return CredToken(token)
    elif user and password:
        print("Using user and password authentication...4")
        return CredUserPass(user, password)
    else:
        raise exceptions.VaultConnection("No valid authentication method found. Please set VAULT_TOKEN or VAULT_USER and VAULT_PASSWORD.")


class Vault:
    prod = os.environ.get("PROD", "False").lower() == "true"
    client:hvac.Client = hvac.Client(url=VAULT_URL)
    
    def __init__(self):
        
        auth = get_auth()
        
        if isinstance(auth, CredUserPass):
            self.client.auth.userpass.login(
                username=auth.username,
                password=auth.password
            )
        elif isinstance(auth, CredToken):
            self.client.token = auth.token
        assert self.client.is_authenticated(), exceptions.VaultAuthentication(
            "Vault authentication failed."
            )            

    def get_secret(self, path, **kwargs) -> dict:
        """
        Get a secret from Vault.
        """        
        try:
            mount_point = path.split("/")[0]
            path = "/".join(path.split("/")[1:])
            secret = self.client.secrets.kv.v2.read_secret_version(path, mount_point=mount_point)
        except Forbidden as e:
            raise exceptions.Forbidden(f"You do not have permission to access this secret: {path}")
        except InvalidPath:
            raise exceptions.InvalidSecretPath(f"Invalid secret path: {path}")
        
        return secret['data']['data']

vault = Vault()



