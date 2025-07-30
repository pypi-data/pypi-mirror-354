"""
ZionAI Utils - Enterprise AI Utilities Library

A comprehensive Python utility library designed specifically for ZionClouds 
employees to simplify common AI, cloud, and data operations.

Author: Harshith Gundela
Email: harshith.gundela@zionclouds.com
Organization: ZionClouds
"""

from .client import GCSClient
from .secrets_manager import SecretsManager

__version__ = "1.2.0"
__author__ = "Harshith Gundela"
__email__ = "harshith.gundela@zionclouds.com"
__organization__ = "ZionClouds"

__all__ = ["GCSClient", "SecretsManager"]

# Quick start examples
__doc__ += """

Quick Start Examples:

1. Upload a file to Google Cloud Storage:
   ```python
   from zionai_utils import GCSClient
   
   client = GCSClient(project_id="your-project")
   success, uri = client.upload_file("bucket-name", "file.pdf")
   ```

2. Get secrets from Google Secret Manager:
   ```python
   from zionai_utils import SecretsManager
   
   secrets = SecretsManager(project_id="your-project")
   api_key = secrets.get_secret("api-key")
   ```

3. Combined usage:
   ```python
   from zionai_utils import SecretsManager, GCSClient
   
   secrets = SecretsManager("your-project")
   bucket = secrets.get_secret("bucket-name")
   
   client = GCSClient("your-project")
   success, uri = client.upload_file(bucket, "data.json")
   ```

For more examples, visit: https://pypi.org/project/zionai-utils/
"""