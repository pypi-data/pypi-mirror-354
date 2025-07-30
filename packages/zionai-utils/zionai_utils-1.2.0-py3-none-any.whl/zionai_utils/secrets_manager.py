"""
Google Secret Manager Client

A simplified client for managing secrets in Google Cloud Secret Manager
with smart defaults and easy-to-use methods.
"""

from google.cloud import secretmanager
from google.oauth2 import service_account
from typing import Optional, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class SecretsManager:
    """Simplified Google Cloud Secret Manager client"""
    
    def __init__(self, project_id: Optional[str] = None, credentials_path: Optional[str] = None):
        """
        Initialize Secrets Manager client with smart defaults
        
        Args:
            project_id: GCP project ID (can be auto-detected)
            credentials_path: Path to service account JSON file (optional if using ADC)
        """
        # Handle credentials in order of preference
        self.credentials = None
        
        if credentials_path:
            # 1. Explicit credentials file
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            # 2. Environment variable pointing to credentials
            cred_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
            if os.path.exists(cred_path):
                self.credentials = service_account.Credentials.from_service_account_file(cred_path)
        # 3. Application Default Credentials (ADC) - handled automatically by client
        
        # Initialize client
        try:
            if self.credentials:
                self.client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
            else:
                # Use Application Default Credentials (works on GCP, with gcloud, etc.)
                self.client = secretmanager.SecretManagerServiceClient()
        except Exception as e:
            raise Exception(f"Failed to initialize Secrets Manager client: {e}")
        
        # Handle project_id in order of preference
        self.project_id = project_id
        
        if not self.project_id:
            # Try to auto-detect project_id
            if self.credentials and hasattr(self.credentials, 'project_id'):
                self.project_id = self.credentials.project_id
            elif credentials_path and os.path.exists(credentials_path):
                # Read from service account file
                try:
                    import json
                    with open(credentials_path, 'r') as f:
                        cred_data = json.load(f)
                        self.project_id = cred_data.get('project_id')
                except:
                    pass
            elif 'GOOGLE_CLOUD_PROJECT' in os.environ:
                # Standard environment variable
                self.project_id = os.environ['GOOGLE_CLOUD_PROJECT']
            elif 'GCP_PROJECT' in os.environ:
                # Alternative environment variable
                self.project_id = os.environ['GCP_PROJECT']
        
        if not self.project_id:
            raise ValueError(
                "Project ID is required. Provide it as parameter, set GOOGLE_CLOUD_PROJECT "
                "environment variable, or include it in the service account file."
            )
        
        logger.info(f"Initialized Secrets Manager for project: {self.project_id}")
    
    def get_secret(self, secret_name: str, version: str = "latest", default: Optional[str] = None) -> Optional[str]:
        """
        Get a secret value from Google Secret Manager
        
        Args:
            secret_name: Name of the secret in Secret Manager
            version: Version of the secret (default: "latest")
            default: Default value to return if secret is not found
            
        Returns:
            Secret value as string, or default value if not found
        """
        try:
            secret_path = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version}"
            response = self.client.access_secret_version(request={"name": secret_path})
            value = response.payload.data.decode("UTF-8")
            
            if not value.strip():
                logger.warning(f"Secret '{secret_name}' is empty")
                return default
                
            return value.strip()
            
        except Exception as e:
            logger.warning(f"Could not retrieve secret '{secret_name}': {e}")
            return default
    
    def get_secrets(self, secret_names: Dict[str, str]) -> Dict[str, Optional[str]]:
        """
        Get multiple secrets at once
        
        Args:
            secret_names: Dictionary mapping local_name -> secret_name
                         Example: {"db_host": "db-internal-host", "db_port": "db-port"}
            
        Returns:
            Dictionary with local_name -> secret_value mappings
        """
        results = {}
        for local_name, secret_name in secret_names.items():
            results[local_name] = self.get_secret(secret_name)
        return results
    
    def get_config(self, config_mapping: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get configuration with secrets and defaults
        
        Args:
            config_mapping: Dictionary with config structure
                          Example: {
                              "database": {
                                  "host": {"secret": "db-internal-host", "default": "localhost"},
                                  "port": {"secret": "db-port", "default": "5432"}
                              }
                          }
        
        Returns:
            Resolved configuration dictionary
        """
        def resolve_value(item):
            if isinstance(item, dict):
                if "secret" in item:
                    return self.get_secret(item["secret"], default=item.get("default"))
                else:
                    return {k: resolve_value(v) for k, v in item.items()}
            else:
                return item
        
        return {k: resolve_value(v) for k, v in config_mapping.items()}
    
    def create_secret(self, secret_name: str, secret_value: str) -> bool:
        """
        Create a new secret in Secret Manager
        
        Args:
            secret_name: Name for the new secret
            secret_value: Value to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            parent = f"projects/{self.project_id}"
            
            # Create the secret
            secret = self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_name,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            
            # Add the secret version
            self.client.add_secret_version(
                request={
                    "parent": secret.name,
                    "payload": {"data": secret_value.encode("UTF-8")},
                }
            )
            
            logger.info(f"Created secret: {secret_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating secret '{secret_name}': {e}")
            return False
    
    def update_secret(self, secret_name: str, secret_value: str) -> bool:
        """
        Update an existing secret with a new value
        
        Args:
            secret_name: Name of the existing secret
            secret_value: New value to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            parent = f"projects/{self.project_id}/secrets/{secret_name}"
            
            # Add new secret version
            self.client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {"data": secret_value.encode("UTF-8")},
                }
            )
            
            logger.info(f"Updated secret: {secret_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating secret '{secret_name}': {e}")
            return False
    
    def delete_secret(self, secret_name: str) -> bool:
        """
        Delete a secret completely
        
        Args:
            secret_name: Name of the secret to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            secret_path = f"projects/{self.project_id}/secrets/{secret_name}"
            self.client.delete_secret(request={"name": secret_path})
            
            logger.info(f"Deleted secret: {secret_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting secret '{secret_name}': {e}")
            return False
    
    def list_secrets(self) -> list:
        """
        List all secrets in the project
        
        Returns:
            List of secret names
        """
        try:
            parent = f"projects/{self.project_id}"
            secrets = self.client.list_secrets(request={"parent": parent})
            
            return [secret.name.split('/')[-1] for secret in secrets]
            
        except Exception as e:
            logger.error(f"Error listing secrets: {e}")
            return []
    
    def secret_exists(self, secret_name: str) -> bool:
        """
        Check if a secret exists
        
        Args:
            secret_name: Name of the secret to check
            
        Returns:
            True if secret exists, False otherwise
        """
        try:
            secret_path = f"projects/{self.project_id}/secrets/{secret_name}"
            self.client.get_secret(request={"name": secret_path})
            return True
        except:
            return False
    
    def get_secret_info(self, secret_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a secret
        
        Args:
            secret_name: Name of the secret
            
        Returns:
            Dictionary with secret metadata or None if not found
        """
        try:
            secret_path = f"projects/{self.project_id}/secrets/{secret_name}"
            secret = self.client.get_secret(request={"name": secret_path})
            
            return {
                "name": secret.name.split('/')[-1],
                "create_time": secret.create_time,
                "replication": str(secret.replication),
                "labels": dict(secret.labels) if secret.labels else {}
            }
        except Exception as e:
            logger.error(f"Error getting secret info for '{secret_name}': {e}")
            return None