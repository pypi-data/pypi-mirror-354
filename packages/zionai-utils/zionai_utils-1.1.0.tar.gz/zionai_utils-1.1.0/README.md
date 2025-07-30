# ZionAI Utils - GCS Upload Made Simple

A dead-simple utility library for uploading files to Google Cloud Storage.

## Installation

```bash
pip install zionai_utils==1.1.0
```

## Quick Start

### 1. Upload a File (Simplest Way)

```python
from zionai_utils import GCSClient

# Initialize client
client = GCSClient(
    credentials_path="/path/to/service-account.json",
    project_id="your-project-id"
)

# Upload any file with one line
success, gcs_uri = client.upload_file(
    bucket_name="your-bucket",
    file_path="document.pdf"
)

if success:
    print(f"✅ Uploaded: {gcs_uri}")
else:
    print("❌ Upload failed")
```

### 2. Upload Text Content

```python
from zionai_utils import GCSClient

client = GCSClient(
    credentials_path="/path/to/service-account.json",
    project_id="your-project-id"
)

# Upload text directly
success, gcs_uri = client.upload_text(
    bucket_name="your-bucket",
    file_name="hello.txt",
    text_content="Hello, World!"
)
```

### 3. Upload from Memory (Advanced)

```python
from zionai_utils import GCSClient
import json

client = GCSClient(
    credentials_path="/path/to/service-account.json",
    project_id="your-project-id"
)

# Create JSON data
data = {"name": "John", "age": 30}
json_bytes = json.dumps(data).encode('utf-8')

success, gcs_uri = client.upload_bytes(
    bucket_name="your-bucket",
    file_name="data.json",
    file_data=json_bytes,
    content_type="application/json"
)
```

## Environment Variables Setup

Set your credentials as an environment variable to avoid passing the path:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

Then initialize without credentials path:

```python
from zionai_utils import GCSClient

# No need to specify credentials_path if env var is set
client = GCSClient(project_id="your-project-id")

success, gcs_uri = client.upload_file("your-bucket", "document.pdf")
```

## Methods Available

| Method | Description | Best For |
|--------|-------------|----------|
| `upload_file()` | Upload from file path | Most common use case |
| `upload_text()` | Upload text content | Quick text uploads |
| `upload_bytes()` | Upload raw bytes | Advanced scenarios |

## Features

- ✅ **Auto-detects file types** - No need to specify content type
- ✅ **Simple error handling** - Returns success boolean + URI
- ✅ **Flexible initialization** - Use credentials file or environment variables
- ✅ **Metadata support** - Add custom metadata to uploads
- ✅ **Backward compatible** - Existing code continues to work

## Common Use Cases

### Upload with Custom Destination Name

```python
success, gcs_uri = client.upload_file(
    bucket_name="your-bucket",
    file_path="local_file.pdf",
    destination_name="renamed_file.pdf"
)
```

### Upload with Metadata

```python
success, gcs_uri = client.upload_file(
    bucket_name="your-bucket",
    file_path="document.pdf",
    meta_data={
        "author": "John Doe",
        "department": "Engineering",
        "version": "1.0"
    }
)
```

### Batch Upload

```python
files_to_upload = ["file1.pdf", "file2.jpg", "file3.txt"]

for file_path in files_to_upload:
    success, gcs_uri = client.upload_file("your-bucket", file_path)
    if success:
        print(f"✅ {file_path} -> {gcs_uri}")
    else:
        print(f"❌ Failed to upload {file_path}")
```

## Error Handling

All methods return a tuple `(success: bool, gcs_uri: str | None)`:

```python
success, gcs_uri = client.upload_file("bucket", "file.pdf")

if success:
    print(f"File uploaded successfully: {gcs_uri}")
    # Do something with the GCS URI
else:
    print("Upload failed - check your credentials and bucket name")
```

## Requirements

- Python 3.7+
- Google Cloud Storage credentials
- `google-cloud-storage>=2.0.0` (installed automatically)