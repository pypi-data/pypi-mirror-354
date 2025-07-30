from pydantic import BaseModel, ValidationError
from pydantic import PrivateAttr
from .vault import vault
from rilz.logger import logger
from typing import Any, Dict, ClassVar
from pydantic import BaseModel

class Secret(BaseModel):
    """
    Base class for secrets stored in Vault.

    Subclasses should define the expected fields for the secret and
    set the class attribute `vault_path` to the corresponding Vault path.

    Secret values are fetched from Vault automatically when the model is instantiated.
    """
    # Class attributes
    vault_path: ClassVar[str | None] = None  # Define path in subclasses
    _secret_data_cache: ClassVar[Dict[str, Any] | None] = None  # Class-level cache
    
    # Instance-level private attribute to store loaded data
    _loaded_data: Dict[str, Any] = PrivateAttr(default_factory=dict)
    
    def __init__(self, **data):
        # First load secrets from vault
        
        secret_data = self._load_from_vault(type(self).model_fields.keys())        
        # Merge with any explicitly provided values
        merged_data = {**secret_data, **data}
        
        # Initialize the model with merged data        
        super().__init__(**merged_data)
        
    
    def _load_from_vault(self, fields_name:list) -> Dict[str, Any]:
        """Load secret data from vault"""
        cls = self.__class__
        
        # Check if vault_path is set in the class
        if cls.vault_path is None:
            raise ValueError(f"Vault `vault_path` must be set in the class {cls.__name__}.")
        
        # Use cached data if available
        if cls._secret_data_cache is not None:
            return cls._secret_data_cache
        
        # Otherwise load from vault
        try:
            # Ensure vault client is available
            if vault is None:
                logger.warning(f"Vault client is not initialized for {cls.__name__}.")
                return {}
            
            secret_data = vault.get_secret(cls.vault_path, mount_point="secret")
            if secret_data is None:
                logger.warning(f"No secret data found at path '{cls.vault_path}' for {cls.__name__}.")
                cls._secret_data_cache = {}
            else:                
                cls._secret_data_cache = {key: secret_data[key] for key in fields_name if key in secret_data}
                logger.debug(f"Secret for {cls.__name__} fetched and cached successfully.")
            
            return cls._secret_data_cache
        except Exception as e:
            raise ValueError(f"Failed to fetch secret for {cls.__name__} from path '{cls.vault_path}': {e}") from e            
            
    
    @classmethod
    def clear_cache(cls):
        """Clears the cached secret data for this specific class."""
        logger.debug(f"Clearing cache for {cls.__name__}")
        cls._secret_data_cache = None
    
    class Config:
        # Ensure that the model is not allowed to be instantiated with
        # any extra fields not defined in the model
        extra = 'forbid'
