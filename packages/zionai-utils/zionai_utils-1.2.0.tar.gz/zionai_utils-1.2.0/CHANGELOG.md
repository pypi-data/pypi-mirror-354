# Changelog

All notable changes to ZionAI Utils will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-15

### Added
- **SecretsManager class** for Google Cloud Secret Manager operations
- `get_secret()` method for simple secret retrieval with defaults
- `get_secrets()` method for batch secret operations
- `get_config()` method for structured configuration loading
- `create_secret()` and `update_secret()` methods for secret management
- `list_secrets()` and `secret_exists()` methods for secret discovery
- Smart auto-detection of project_id from multiple sources
- Application Default Credentials (ADC) support
- Environment variable support for credentials and project_id
- Enhanced GCS client with new methods:
  - `upload_json()` for direct JSON uploads
  - `batch_upload()` for multiple file uploads
  - `list_files()` and `delete_file()` for file management
  - `make_public` parameter for public file access
- Comprehensive logging throughout the library
- Better error handling and user feedback

### Enhanced
- **GCS Client improvements:**
  - Auto-detection of project_id from service account files
  - Enhanced metadata support
  - Better content type detection
  - Improved error messages and logging
- **Documentation:**
  - Complete usage examples for all methods
  - Real-world ZionClouds use cases
  - Environment setup instructions
  - Combined usage patterns

### Changed
- Parameter order in constructors: `project_id` now comes first for consistency
- Improved error messages with more specific guidance
- Enhanced type hints and documentation strings

### Dependencies
- Added `google-cloud-secret-manager>=2.0.0`
- Updated minimum Python version support documentation

## [1.1.0] - 2025-01-15

### Added
- `upload_file()` method for direct file path uploads
- `upload_text()` method for text content uploads
- `upload_bytes()` method with better defaults
- Automatic MIME type detection
- Enhanced error handling and validation
- File existence checking before upload
- Custom destination naming support
- Metadata support for all upload methods

### Enhanced
- Better content type auto-detection
- Improved error messages
- More comprehensive README with usage examples

### Changed
- Made `content_type` parameter optional with auto-detection
- Improved method naming for clarity

### Deprecated
- `upload_to_gcs()` method (still works, but use `upload_bytes()` instead)

## [1.0.2] - 2025-01-14

### Added
- Initial release of ZionAI Utils
- Basic `GCSClient` for Google Cloud Storage uploads
- `upload_to_gcs()` method for file uploads
- Basic error handling
- MIT License

### Features
- Simple GCS file upload functionality
- Service account authentication support
- Basic metadata support for uploads

[1.2.0]: https://github.com/ZionClouds/zionai-utils/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ZionClouds/zionai-utils/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/ZionClouds/zionai-utils/releases/tag/v1.0.2