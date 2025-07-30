from google.cloud import storage
from typing import Optional, Tuple, Dict, Any, Union
import os
import mimetypes
from pathlib import Path

class GCSClient:
    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        """
        Initialize GCS client with credentials
        
        Args:
            credentials_path: Path to service account JSON file
            project_id: GCP project ID
        """
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        try:
            self.storage_client = storage.Client(project=project_id)
        except Exception as e:
            raise Exception(f"Failed to initialize GCS client: {e}")
    
    def upload_file(self, bucket_name: str, file_path: str, 
                   destination_name: Optional[str] = None,
                   meta_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        Upload a file from local path to Google Cloud Storage (simplified method)
        
        Args:
            bucket_name: GCS bucket name
            file_path: Local path to the file
            destination_name: Name for the file in GCS (defaults to original filename)
            meta_data: Optional metadata dictionary
            
        Returns:
            Tuple of (success: bool, gcs_uri: str or None)
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False, None
            
            # Get destination name
            if destination_name is None:
                destination_name = Path(file_path).name
            
            # Auto-detect content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            # Read file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            return self.upload_bytes(
                bucket_name=bucket_name,
                file_name=destination_name,
                file_data=file_data,
                content_type=content_type,
                meta_data=meta_data
            )
            
        except Exception as e:
            print(f'File upload failed: {e}')
            return False, None
    
    def upload_bytes(self, bucket_name: str, file_name: str, file_data: bytes, 
                    content_type: Optional[str] = None,
                    meta_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        Upload bytes data to Google Cloud Storage
        
        Args:
            bucket_name: GCS bucket name
            file_name: Name for the file in GCS
            file_data: File data as bytes
            content_type: MIME type of the file (auto-detected if not provided)
            meta_data: Optional metadata dictionary
            
        Returns:
            Tuple of (success: bool, gcs_uri: str or None)
        """
        try:
            # Auto-detect content type if not provided
            if content_type is None:
                content_type, _ = mimetypes.guess_type(file_name)
                if content_type is None:
                    content_type = 'application/octet-stream'
            
            gcs_uri = f"gs://{bucket_name}/{file_name}"
            
            # Get the bucket
            bucket = self.storage_client.bucket(bucket_name)
            
            # Create a blob (object) in the bucket
            blob = bucket.blob(file_name)
            
            # Set metadata if provided
            if meta_data:
                blob.metadata = meta_data
            
            # Upload the bytes directly
            blob.upload_from_string(file_data, content_type=content_type)
            
            print(f'Upload successful: {gcs_uri}')
            
            return True, gcs_uri
            
        except Exception as e:
            print(f'Upload failed: {e}')
            return False, None
    
    def upload_text(self, bucket_name: str, file_name: str, text_content: str,
                   meta_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        Upload text content to Google Cloud Storage (convenience method)
        
        Args:
            bucket_name: GCS bucket name
            file_name: Name for the file in GCS
            text_content: Text content as string
            meta_data: Optional metadata dictionary
            
        Returns:
            Tuple of (success: bool, gcs_uri: str or None)
        """
        try:
            file_data = text_content.encode('utf-8')
            return self.upload_bytes(
                bucket_name=bucket_name,
                file_name=file_name,
                file_data=file_data,
                content_type='text/plain',
                meta_data=meta_data
            )
        except Exception as e:
            print(f'Text upload failed: {e}')
            return False, None
    
    # Keep the original method for backward compatibility
    def upload_to_gcs(self, bucket_name: str, file_name: str, file_data: bytes, 
                     meta_data: Optional[Dict[str, Any]] = None,
                     content_type: str = 'application/pdf') -> Tuple[bool, Optional[str]]:
        """
        Upload data to Google Cloud Storage (legacy method - use upload_bytes instead)
        
        Args:
            bucket_name: GCS bucket name
            file_name: Name for the file in GCS
            file_data: File data as bytes
            meta_data: Optional metadata dictionary
            content_type: MIME type of the file
            
        Returns:
            Tuple of (success: bool, gcs_uri: str or None)
        """
        return self.upload_bytes(
            bucket_name=bucket_name,
            file_name=file_name,
            file_data=file_data,
            content_type=content_type,
            meta_data=meta_data
        )