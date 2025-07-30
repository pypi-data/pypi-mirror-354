"""
Google Secret Manager Examples

This file contains practical examples of using the SecretsManager for various
secret management scenarios in ZionClouds projects.
"""

import os
from datetime import datetime
from zionai_utils import SecretsManager

# Initialize the secrets manager
# Option 1: With explicit credentials
secrets = SecretsManager(
    project_id="your-project-id",
    credentials_path="/path/to/service-account.json"
)

# Option 2: Using environment variables (recommended for production)
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
# export GOOGLE_CLOUD_PROJECT="your-project-id"
# secrets = SecretsManager()

def example_basic_secret_retrieval():
    """Example 1: Basic secret retrieval"""
    print("=== Basic Secret Retrieval ===")
    
    # Get database credentials
    db_host = secrets.get_secret("db-internal-host")
    db_port = secrets.get_secret("db-port")
    db_password = secrets.get_secret("db-password")
    
    print(f"Database Host: {db_host}")
    print(f"Database Port: {db_port}")
    print(f"Password Retrieved: {'✅' if db_password else '❌'}")


def example_secrets_with_defaults():
    """Example 2: Using default values for missing secrets"""
    print("\n=== Secrets with Default Values ===")
    
    # Get configuration with sensible defaults
    api_endpoint = secrets.get_secret("api-endpoint", default="https://api.example.com")
    timeout = secrets.get_secret("request-timeout", default="30")
    debug_mode = secrets.get_secret("debug-mode", default="false")
    
    print(f"API Endpoint: {api_endpoint}")
    print(f"Timeout: {timeout} seconds")
    print(f"Debug Mode: {debug_mode}")


def example_batch_secret_retrieval():
    """Example 3: Get multiple secrets at once"""
    print("\n=== Batch Secret Retrieval ===")
    
    # Define the secrets you need
    secret_mapping = {
        "db_host": "db-internal-host",
        "db_port": "db-port",
        "db_name": "db-name",
        "db_user": "db-user",
        "db_password": "db-password"
    }
    
    # Get all secrets at once
    config = secrets.get_secrets(secret_mapping)
    
    # Build database connection string
    if all(config.values()):
        db_url = f"postgresql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
        print(f"✅ Database URL constructed successfully")
        print(f"Host: {config['db_host']}")
        print(f"Database: {config['db_name']}")
    else:
        missing = [k for k, v in config.items() if v is None]
        print(f"❌ Missing secrets: {missing}")


def example_structured_configuration():
    """Example 4: Load structured configuration with secrets and defaults"""
    print("\n=== Structured Configuration Loading ===")
    
    # Define your application configuration structure
    app_config_structure = {
        "database": {
            "host": {"secret": "db-internal-host", "default": "localhost"},
            "port": {"secret": "db-port", "default": "5432"},
            "name": {"secret": "db-name", "default": "zionapp"},
            "user": {"secret": "db-user", "default": "postgres"},
            "password": {"secret": "db-password"}  # No default for sensitive data
        },
        "storage": {
            "bucket_name": {"secret": "BUCKET_NAME", "default": "zion-default-bucket"},
            "region": {"secret": "storage-region", "default": "us-central1"}
        },
        "ai": {
            "gemini_model": {"secret": "gemini_model_name", "default": "gemini-pro"},
            "embedding_model": {"secret": "embedding_model_name", "default": "textembedding-gecko"},
            "vision_model": {"secret": "vision_model_name", "default": "gemini-pro-vision"}
        },
        "api": {
            "base_url": {"secret": "BASE_URL", "default": "https://api.zionclouds.com"},
            "timeout": {"secret": "api-timeout", "default": "30"},
            "rate_limit": {"secret": "rate-limit", "default": "100"}
        }
    }
    
    # Load the entire configuration
    app_config = secrets.get_config(app_config_structure)
    
    # Use the configuration
    print("📋 Application Configuration Loaded:")
    print(f"Database: {app_config['database']['host']}:{app_config['database']['port']}")
    print(f"Storage Bucket: {app_config['storage']['bucket_name']}")
    print(f"AI Model: {app_config['ai']['gemini_model']}")
    print(f"API Base URL: {app_config['api']['base_url']}")


def example_zioncloud_real_usage():
    """Example 5: Real ZionClouds usage pattern - exactly like your original code"""
    print("\n=== ZionClouds Real Usage Pattern ===")
    
    # This is exactly how you wanted to use it!
    host = secrets.get_secret("db-internal-host")
    port = secrets.get_secret("db-port")
    dbname = secrets.get_secret("db-name")
    user = secrets.get_secret("db-user")
    password = secrets.get_secret("db-password")
    gemini_model_name = secrets.get_secret("gemini_model_name")
    embedding_model_name = secrets.get_secret("embedding_model_name")
    vision_model_name = secrets.get_secret("vision_model_name")
    bucket_name = secrets.get_secret("BUCKET_NAME")
    processor_id = secrets.get_secret("PROCESSOR_ID")
    location = secrets.get_secret("location", default="us-central1")
    base_url = secrets.get_secret("BASE_URL", default="https://zthinkagent-backend-dev-ncqyw4h3fa-uc.a.run.app/")
    
    print("🎯 ZionClouds Configuration:")
    print(f"Database: {host}:{port}/{dbname}")
    print(f"Models: {gemini_model_name}, {embedding_model_name}")
    print(f"Storage: {bucket_name}")
    print(f"Processor: {processor_id}")
    print(f"Location: {location}")
    print(f"Base URL: {base_url}")


def example_secret_management():
    """Example 6: Creating and updating secrets"""
    print("\n=== Secret Management Operations ===")
    
    # Create new secrets
    print("Creating new secrets...")
    
    secrets_to_create = {
        "app-version": "1.2.0",
        "feature-flags": "advanced_analytics:true,beta_features:false",
        "maintenance-mode": "false"
    }
    
    for secret_name, secret_value in secrets_to_create.items():
        success = secrets.create_secret(secret_name, secret_value)
        if success:
            print(f"✅ Created secret: {secret_name}")
        else:
            print(f"❌ Failed to create: {secret_name}")
    
    # Update an existing secret
    print("\nUpdating secrets...")
    updated = secrets.update_secret("app-version", "1.2.1")
    if updated:
        print("✅ Updated app-version to 1.2.1")
    
    # List all secrets
    print("\nListing all secrets...")
    all_secrets = secrets.list_secrets()
    print(f"Found {len(all_secrets)} secrets:")
    for secret_name in all_secrets[:10]:  # Show first 10
        print(f"  - {secret_name}")


def example_secret_discovery():
    """Example 7: Secret discovery and validation"""
    print("\n=== Secret Discovery and Validation ===")
    
    # Check if critical secrets exist
    critical_secrets = [
        "db-password",
        "api-key",
        "encryption-key",
        "jwt-secret"
    ]
    
    print("Checking critical secrets...")
    missing_secrets = []
    
    for secret_name in critical_secrets:
        exists = secrets.secret_exists(secret_name)
        if exists:
            print(f"✅ {secret_name} - exists")
        else:
            print(f"❌ {secret_name} - missing")
            missing_secrets.append(secret_name)
    
    if missing_secrets:
        print(f"\n⚠️  Missing critical secrets: {missing_secrets}")
    else:
        print("\n✅ All critical secrets are available")
    
    # Get secret metadata
    print("\nSecret information...")
    secret_info = secrets.get_secret_info("db-password")
    if secret_info:
        print(f"Secret details: {secret_info}")


def example_environment_specific_config():
    """Example 8: Environment-specific configuration"""
    print("\n=== Environment-Specific Configuration ===")
    
    # Get environment (could be from secret or environment variable)
    environment = secrets.get_secret("environment", default="development")
    
    # Load environment-specific configuration
    env_secrets = {
        "development": {
            "db_host": "db-dev-host",
            "api_url": "dev-api-url",
            "debug_level": "debug-level-dev"
        },
        "staging": {
            "db_host": "db-staging-host", 
            "api_url": "staging-api-url",
            "debug_level": "debug-level-staging"
        },
        "production": {
            "db_host": "db-prod-host",
            "api_url": "prod-api-url", 
            "debug_level": "debug-level-prod"
        }
    }
    
    if environment in env_secrets:
        env_config = secrets.get_secrets(env_secrets[environment])
        print(f"🌍 Environment: {environment}")
        print(f"Database Host: {env_config.get('db_host', 'not configured')}")
        print(f"API URL: {env_config.get('api_url', 'not configured')}")
        print(f"Debug Level: {env_config.get('debug_level', 'not configured')}")
    else:
        print(f"❌ Unknown environment: {environment}")


def example_backup_and_audit():
    """Example 9: Secret backup and audit operations"""
    print("\n=== Secret Backup and Audit ===")
    
    def audit_secrets():
        """Audit all secrets and create a report"""
        all_secrets = secrets.list_secrets()
        
        audit_report = {
            "audit_date": datetime.now().isoformat(),
            "total_secrets": len(all_secrets),
            "secrets_audit": {}
        }
        
        for secret_name in all_secrets:
            info = secrets.get_secret_info(secret_name)
            value = secrets.get_secret(secret_name)
            
            audit_report["secrets_audit"][secret_name] = {
                "exists": value is not None,
                "empty": value == "" if value is not None else None,
                "metadata": info
            }
        
        print(f"📊 Audit Report:")
        print(f"Total secrets: {audit_report['total_secrets']}")
        
        empty_secrets = [name for name, data in audit_report["secrets_audit"].items() 
                        if data.get("empty")]
        if empty_secrets:
            print(f"⚠️  Empty secrets: {empty_secrets}")
        
        return audit_report
    
    # Run audit
    audit_report = audit_secrets()


def example_integration_with_databases():
    """Example 10: Integration with database connections"""
    print("\n=== Database Integration Example ===")
    
    def get_database_connection():
        """Get database connection using secrets"""
        try:
            # Get database configuration from secrets
            db_config = secrets.get_secrets({
                "host": "db-internal-host",
                "port": "db-port", 
                "database": "db-name",
                "username": "db-user",
                "password": "db-password"
            })
            
            # Validate all required secrets are present
            if not all(db_config.values()):
                missing = [k for k, v in db_config.items() if v is None]
                raise ValueError(f"Missing database secrets: {missing}")
            
            # Build connection string
            connection_string = (
                f"postgresql://{db_config['username']}:{db_config['password']}"
                f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            )
            
            print("✅ Database connection configured successfully")
            print(f"Host: {db_config['host']}")
            print(f"Database: {db_config['database']}")
            
            # In a real application, you would return the actual connection
            # import psycopg2
            # return psycopg2.connect(connection_string)
            
            return connection_string
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    # Get database connection
    db_connection = get_database_connection()


if __name__ == "__main__":
    """Run all examples"""
    print("🔐 ZionAI Utils - Secrets Manager Examples\n")
    
    try:
        example_basic_secret_retrieval()
        example_secrets_with_defaults()
        example_batch_secret_retrieval()
        example_structured_configuration()
        example_zioncloud_real_usage()
        example_secret_management()
        example_secret_discovery()
        example_environment_specific_config()
        example_backup_and_audit()
        example_integration_with_databases()
        
        print("\n✅ All examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Valid GCP credentials configured")
        print("2. Secret Manager API enabled")
        print("3. Appropriate IAM permissions")
        print("4. Test secrets created in your project")