"""
Combined Examples - Secrets Manager + GCS Client

This file demonstrates how to use SecretsManager and GCSClient together
for real-world ZionClouds applications.
"""

import json
import os
from datetime import datetime
from zionai_utils import SecretsManager, GCSClient

def example_complete_app_initialization():
    """Example 1: Complete application initialization using secrets"""
    print("=== Complete Application Initialization ===")
    
    # Step 1: Initialize secrets manager
    secrets = SecretsManager(project_id="zthinkagent")
    
    # Step 2: Get all application configuration from secrets
    app_config = secrets.get_config({
        "gcp": {
            "project_id": {"secret": "PROJECT_ID", "default": "zthinkagent"},
            "location": {"secret": "location", "default": "us-central1"}
        },
        "database": {
            "host": {"secret": "db-internal-host", "default": "localhost"},
            "port": {"secret": "db-port", "default": "5432"},
            "name": {"secret": "db-name", "default": "zionapp"},
            "user": {"secret": "db-user", "default": "postgres"},
            "password": {"secret": "db-password"}
        },
        "storage": {
            "bucket_name": {"secret": "BUCKET_NAME", "default": "zion-default-bucket"}
        },
        "ai": {
            "gemini_model": {"secret": "gemini_model_name", "default": "gemini-pro"},
            "embedding_model": {"secret": "embedding_model_name", "default": "textembedding-gecko"},
            "vision_model": {"secret": "vision_model_name", "default": "gemini-pro-vision"}
        },
        "document_ai": {
            "processor_id": {"secret": "PROCESSOR_ID"}
        },
        "api": {
            "base_url": {"secret": "BASE_URL", "default": "https://zthinkagent-backend-dev-ncqyw4h3fa-uc.a.run.app/"}
        }
    })
    
    # Step 3: Initialize GCS client using configuration from secrets
    gcs_client = GCSClient(project_id=app_config["gcp"]["project_id"])
    
    # Step 4: Validate configuration and report status
    print("🚀 Application Initialized Successfully!")
    print(f"Project: {app_config['gcp']['project_id']}")
    print(f"Database: {app_config['database']['host']}:{app_config['database']['port']}")
    print(f"Storage Bucket: {app_config['storage']['bucket_name']}")
    print(f"AI Models: {app_config['ai']['gemini_model']}")
    print(f"API Base: {app_config['api']['base_url']}")
    
    return secrets, gcs_client, app_config


def example_document_processing_pipeline():
    """Example 2: Document processing pipeline with secrets and storage"""
    print("\n=== Document Processing Pipeline ===")
    
    # Initialize components
    secrets = SecretsManager()
    gcs_client = GCSClient()
    
    # Get configuration
    bucket_name = secrets.get_secret("BUCKET_NAME", default="zion-document-processing")
    processor_id = secrets.get_secret("PROCESSOR_ID")
    
    def process_and_upload_document(document_path, client_id):
        """Process a document and upload results to GCS"""
        
        if not os.path.exists(document_path):
            print(f"❌ Document not found: {document_path}")
            return None
        
        # Step 1: Upload original document
        original_filename = os.path.basename(document_path)
        success, original_uri = gcs_client.upload_file(
            bucket_name=bucket_name,
            file_path=document_path,
            destination_name=f"clients/{client_id}/originals/{original_filename}",
            meta_data={
                "client_id": client_id,
                "document_type": "original",
                "upload_timestamp": datetime.now().isoformat(),
                "processor_id": processor_id
            }
        )
        
        if not success:
            print(f"❌ Failed to upload original document")
            return None
        
        # Step 2: Simulate document processing (extract text, classify, etc.)
        processing_results = {
            "document_id": f"DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "client_id": client_id,
            "original_file": original_filename,
            "original_gcs_uri": original_uri,
            "processed_at": datetime.now().isoformat(),
            "processor_id": processor_id,
            "extracted_text": "Sample extracted text from document...",
            "classification": "invoice",
            "confidence": 0.95,
            "extracted_entities": {
                "amount": "$1,250.00",
                "date": "2025-01-15",
                "vendor": "Acme Corp"
            }
        }
        
        # Step 3: Upload processing results
        results_filename = f"processing_results_{processing_results['document_id']}.json"
        success, results_uri = gcs_client.upload_json(
            bucket_name=bucket_name,
            file_name=f"clients/{client_id}/processed/{results_filename}",
            json_data=processing_results,
            meta_data={
                "client_id": client_id,
                "document_type": "processing_results",
                "original_document": original_filename
            }
        )
        
        if success:
            print(f"✅ Document processed: {original_filename}")
            print(f"   Original: {original_uri}")
            print(f"   Results: {results_uri}")
            return processing_results
        else:
            print(f"❌ Failed to upload processing results")
            return None
    
    # Example usage
    # process_and_upload_document("/path/to/invoice.pdf", "client-123")
    print("📄 Document processing pipeline configured")
    print(f"Bucket: {bucket_name}")
    print(f"Processor: {processor_id}")


def example_automated_reporting_system():
    """Example 3: Automated reporting system using secrets for config"""
    print("\n=== Automated Reporting System ===")
    
    # Initialize components
    secrets = SecretsManager()
    gcs_client = GCSClient()
    
    # Get configuration from secrets
    config = secrets.get_secrets({
        "reports_bucket": "REPORTS_BUCKET_NAME",
        "db_host": "db-internal-host",
        "db_name": "db-name",
        "notification_webhook": "slack-webhook-url"
    })
    
    def generate_daily_report():
        """Generate and upload daily business report"""
        
        # Step 1: Collect data (simulated - in real app, query database)
        report_data = {
            "report_id": f"DAILY_{datetime.now().strftime('%Y%m%d')}",
            "generated_at": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d'),
            "metrics": {
                "total_documents_processed": 245,
                "new_clients": 3,
                "revenue": 15420.50,
                "api_calls": 12543,
                "storage_usage_gb": 128.5,
                "error_rate": 0.02
            },
            "top_clients": [
                {"name": "Acme Corp", "documents": 45},
                {"name": "TechStart Inc", "documents": 32},
                {"name": "Global Dynamics", "documents": 28}
            ],
            "system_health": {
                "uptime": "99.98%",
                "avg_response_time": "245ms",
                "storage_health": "excellent"
            }
        }
        
        # Step 2: Upload report to GCS
        report_filename = f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.json"
        bucket_name = config.get("reports_bucket", "zion-reports")
        
        success, report_uri = gcs_client.upload_json(
            bucket_name=bucket_name,
            file_name=f"daily/{report_filename}",
            json_data=report_data,
            meta_data={
                "report_type": "daily_business",
                "auto_generated": "true",
                "data_source": config.get("db_host", "unknown"),
                "retention_period": "365_days"
            }
        )
        
        # Step 3: Generate summary report for executives
        if success:
            executive_summary = {
                "date": report_data["date"],
                "key_metrics": {
                    "documents_processed": report_data["metrics"]["total_documents_processed"],
                    "revenue": f"${report_data['metrics']['revenue']:,.2f}",
                    "new_clients": report_data["metrics"]["new_clients"],
                    "system_uptime": report_data["system_health"]["uptime"]
                },
                "status": "✅ All systems operational",
                "action_items": [
                    "Review client onboarding for 3 new clients",
                    "Monitor storage usage approaching 130GB threshold"
                ]
            }
            
            # Upload executive summary
            exec_filename = f"executive_summary_{datetime.now().strftime('%Y-%m-%d')}.json"
            exec_success, exec_uri = gcs_client.upload_json(
                bucket_name=bucket_name,
                file_name=f"executive/{exec_filename}",
                json_data=executive_summary,
                make_public=False,
                meta_data={
                    "report_type": "executive_summary",
                    "confidentiality": "restricted",
                    "derived_from": report_uri
                }
            )
            
            if exec_success:
                print("✅ Daily reports generated successfully")
                print(f"   Detailed Report: {report_uri}")
                print(f"   Executive Summary: {exec_uri}")
                
                # Step 4: Send notification (simulated)
                webhook_url = config.get("notification_webhook")
                if webhook_url:
                    print(f"📧 Notification sent to: {webhook_url}")
                
                return {
                    "detailed_report": report_uri,
                    "executive_summary": exec_uri,
                    "metrics": report_data["metrics"]
                }
            else:
                print("❌ Failed to generate executive summary")
        else:
            print("❌ Failed to generate daily report")
        
        return None
    
    # Generate report
    report_result = generate_daily_report()


def example_multi_environment_deployment():
    """Example 4: Multi-environment deployment configuration"""
    print("\n=== Multi-Environment Deployment ===")
    
    def setup_environment(environment_name):
        """Setup application for specific environment"""
        
        # Initialize secrets manager
        secrets = SecretsManager()
        
        # Get environment-specific configuration
        env_config = secrets.get_config({
            "environment": {
                "name": {"secret": f"{environment_name}-env-name", "default": environment_name},
                "debug": {"secret": f"{environment_name}-debug-mode", "default": "false"}
            },
            "database": {
                "host": {"secret": f"{environment_name}-db-host"},
                "port": {"secret": f"{environment_name}-db-port", "default": "5432"},
                "name": {"secret": f"{environment_name}-db-name"},
                "ssl_mode": {"secret": f"{environment_name}-db-ssl", "default": "require"}
            },
            "storage": {
                "bucket": {"secret": f"{environment_name}-bucket-name"},
                "region": {"secret": f"{environment_name}-storage-region", "default": "us-central1"}
            },
            "monitoring": {
                "log_level": {"secret": f"{environment_name}-log-level", "default": "INFO"},
                "metrics_endpoint": {"secret": f"{environment_name}-metrics-url"}
            }
        })
        
        # Initialize GCS client for environment
        gcs_client = GCSClient()
        
        # Upload environment configuration for auditing
        config_backup = {
            "environment": environment_name,
            "configuration": env_config,
            "deployed_at": datetime.now().isoformat(),
            "deployed_by": "zionai_utils_automation"
        }
        
        bucket_name = env_config["storage"]["bucket"]
        if bucket_name:
            success, config_uri = gcs_client.upload_json(
                bucket_name=bucket_name,
                file_name=f"config/deployment_{environment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                json_data=config_backup,
                meta_data={
                    "environment": environment_name,
                    "config_type": "deployment_backup",
                    "auto_generated": "true"
                }
            )
            
            if success:
                print(f"✅ {environment_name.upper()} environment configured")
                print(f"   Database: {env_config['database']['host']}:{env_config['database']['port']}")
                print(f"   Storage: {bucket_name}")
                print(f"   Config Backup: {config_uri}")
            else:
                print(f"❌ Failed to backup {environment_name} configuration")
        else:
            print(f"⚠️  {environment_name.upper()} environment configured (no storage bucket)")
        
        return env_config, gcs_client
    
    # Setup multiple environments
    environments = ["development", "staging", "production"]
    
    for env in environments:
        print(f"\n🌍 Setting up {env} environment...")
        env_config, gcs_client = setup_environment(env)


def example_data_backup_and_sync():
    """Example 5: Data backup and synchronization system"""
    print("\n=== Data Backup and Synchronization ===")
    
    # Initialize components
    secrets = SecretsManager()
    gcs_client = GCSClient()
    
    # Get backup configuration
    backup_config = secrets.get_secrets({
        "primary_bucket": "PRIMARY_BACKUP_BUCKET",
        "secondary_bucket": "SECONDARY_BACKUP_BUCKET", 
        "backup_encryption_key": "BACKUP_ENCRYPTION_KEY",
        "retention_days": "BACKUP_RETENTION_DAYS"
    })
    
    def backup_application_data():
        """Backup critical application data"""
        
        # Simulate collecting data from various sources
        backup_data = {
            "backup_id": f"BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "data_sources": {
                "user_data": {"records": 1500, "size_mb": 45.2},
                "transaction_logs": {"records": 8900, "size_mb": 123.8},
                "configuration": {"records": 89, "size_mb": 2.1},
                "analytics": {"records": 15600, "size_mb": 78.5}
            },
            "metadata": {
                "version": "1.2.0",
                "environment": "production",
                "encryption": "AES-256" if backup_config.get("backup_encryption_key") else "none"
            }
        }
        
        # Primary backup
        primary_bucket = backup_config.get("primary_bucket", "zion-primary-backup")
        backup_filename = f"backup_{backup_data['backup_id']}.json"
        
        success_primary, primary_uri = gcs_client.upload_json(
            bucket_name=primary_bucket,
            file_name=f"daily/{backup_filename}",
            json_data=backup_data,
            meta_data={
                "backup_type": "daily_full",
                "encryption": backup_data["metadata"]["encryption"],
                "retention_days": backup_config.get("retention_days", "30")
            }
        )
        
        # Secondary backup (for redundancy)
        secondary_bucket = backup_config.get("secondary_bucket")
        success_secondary = False
        secondary_uri = None
        
        if secondary_bucket:
            success_secondary, secondary_uri = gcs_client.upload_json(
                bucket_name=secondary_bucket,
                file_name=f"daily/{backup_filename}",
                json_data=backup_data,
                meta_data={
                    "backup_type": "daily_full_replica",
                    "primary_backup": primary_uri,
                    "encryption": backup_data["metadata"]["encryption"]
                }
            )
        
        # Report backup status
        if success_primary:
            print("✅ Primary backup completed")
            print(f"   Location: {primary_uri}")
            
            if success_secondary:
                print("✅ Secondary backup completed")
                print(f"   Location: {secondary_uri}")
            elif secondary_bucket:
                print("⚠️  Secondary backup failed")
            
            return {
                "backup_id": backup_data["backup_id"],
                "primary_uri": primary_uri,
                "secondary_uri": secondary_uri,
                "status": "success"
            }
        else:
            print("❌ Primary backup failed")
            return {"status": "failed"}
    
    # Run backup
    backup_result = backup_application_data()


def example_real_zioncloud_application():
    """Example 6: Complete real ZionCloud application setup"""
    print("\n=== Real ZionCloud Application Setup ===")
    
    def initialize_zioncloud_app():
        """Complete application initialization - exactly like your use case"""
        
        # Step 1: Initialize secrets (your exact usage!)
        secrets = SecretsManager(project_id="zthinkagent")
        
        # Step 2: Get ALL your secrets exactly as you wanted
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
        
        # Step 3: Initialize GCS client
        gcs_client = GCSClient(project_id="zthinkagent")
        
        # Step 4: Create application configuration
        app_config = {
            "database": {
                "connection_string": f"postgresql://{user}:{password}@{host}:{port}/{dbname}",
                "host": host,
                "port": port,
                "database": dbname,
                "user": user
            },
            "ai_models": {
                "gemini": gemini_model_name,
                "embedding": embedding_model_name,
                "vision": vision_model_name
            },
            "storage": {
                "bucket": bucket_name,
                "location": location
            },
            "document_ai": {
                "processor_id": processor_id,
                "location": location
            },
            "api": {
                "base_url": base_url
            }
        }
        
        # Step 5: Upload configuration backup to GCS
        config_backup = {
            "application": "zthinkagent",
            "version": "1.2.0",
            "configuration": app_config,
            "initialized_at": datetime.now().isoformat(),
            "secrets_loaded": {
                "database": all([host, port, dbname, user, password]),
                "ai_models": all([gemini_model_name, embedding_model_name, vision_model_name]),
                "storage": bucket_name is not None,
                "document_ai": processor_id is not None
            }
        }
        
        success, config_uri = gcs_client.upload_json(
            bucket_name=bucket_name,
            file_name=f"config/app_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            json_data=config_backup,
            meta_data={
                "config_type": "application_initialization",
                "environment": "production",
                "auto_generated": "true"
            }
        )
        
        # Step 6: Report initialization status
        print("🚀 ZionCloud Application Initialized!")
        print(f"Database: {host}:{port}/{dbname}")
        print(f"AI Models: {gemini_model_name}")
        print(f"Storage: {bucket_name}")
        print(f"Document AI: {processor_id}")
        print(f"API Base: {base_url}")
        
        if success:
            print(f"✅ Configuration backed up: {config_uri}")
        
        return secrets, gcs_client, app_config
    
    # Initialize the application
    secrets, gcs_client, config = initialize_zioncloud_app()
    
    # Example usage of initialized components
    def process_document_example(document_path):
        """Example document processing using initialized components"""
        if not os.path.exists(document_path):
            print(f"❌ Document not found: {document_path}")
            return
        
        # Upload document using the configured bucket
        bucket_name = config["storage"]["bucket"]
        filename = os.path.basename(document_path)
        
        success, gcs_uri = gcs_client.upload_file(
            bucket_name=bucket_name,
            file_path=document_path,
            destination_name=f"documents/{filename}",
            meta_data={
                "processor_id": config["document_ai"]["processor_id"],
                "ai_model": config["ai_models"]["gemini"],
                "upload_timestamp": datetime.now().isoformat()
            }
        )
        
        if success:
            print(f"✅ Document uploaded for processing: {gcs_uri}")
            return gcs_uri
        else:
            print("❌ Document upload failed")
            return None
    
    # Example: Process a document
    # process_document_example("/path/to/sample_document.pdf")
    
    return secrets, gcs_client, config


def example_monitoring_and_alerting():
    """Example 7: Monitoring and alerting system"""
    print("\n=== Monitoring and Alerting System ===")
    
    # Initialize components
    secrets = SecretsManager()
    gcs_client = GCSClient()
    
    # Get monitoring configuration
    monitoring_config = secrets.get_secrets({
        "metrics_bucket": "METRICS_BUCKET",
        "alert_webhook": "ALERT_WEBHOOK_URL",
        "log_level": "LOG_LEVEL",
        "error_threshold": "ERROR_THRESHOLD"
    })
    
    def collect_system_metrics():
        """Collect and store system metrics"""
        
        # Simulate collecting system metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.1,
                "network_io": {
                    "bytes_in": 1245670,
                    "bytes_out": 987543
                }
            },
            "application": {
                "active_sessions": 245,
                "api_requests_per_minute": 523,
                "average_response_time": 342,
                "error_rate": 0.015,
                "queue_length": 12
            },
            "storage": {
                "total_files": 15420,
                "storage_used_gb": 234.7,
                "upload_success_rate": 0.998
            },
            "ai_services": {
                "model_calls": 1523,
                "avg_processing_time": 1.2,
                "success_rate": 0.995
            }
        }
        
        # Check for alerts
        alerts = []
        error_threshold = float(monitoring_config.get("error_threshold", "0.05"))
        
        if metrics["application"]["error_rate"] > error_threshold:
            alerts.append({
                "type": "error_rate_high",
                "message": f"Error rate {metrics['application']['error_rate']:.3f} exceeds threshold {error_threshold}",
                "severity": "high"
            })
        
        if metrics["system"]["memory_usage"] > 80:
            alerts.append({
                "type": "memory_usage_high", 
                "message": f"Memory usage at {metrics['system']['memory_usage']:.1f}%",
                "severity": "medium"
            })
        
        # Store metrics
        metrics_bucket = monitoring_config.get("metrics_bucket", "zion-metrics")
        metrics_filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        success, metrics_uri = gcs_client.upload_json(
            bucket_name=metrics_bucket,
            file_name=f"hourly/{metrics_filename}",
            json_data=metrics,
            meta_data={
                "metric_type": "system_health",
                "alerts_count": len(alerts),
                "collection_timestamp": metrics["timestamp"]
            }
        )
        
        if success:
            print(f"✅ Metrics collected: {metrics_uri}")
            
            # Handle alerts
            if alerts:
                alert_data = {
                    "timestamp": datetime.now().isoformat(),
                    "alerts": alerts,
                    "metrics_source": metrics_uri,
                    "system_status": "degraded" if any(a["severity"] == "high" for a in alerts) else "warning"
                }
                
                # Store alert
                alert_filename = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                alert_success, alert_uri = gcs_client.upload_json(
                    bucket_name=metrics_bucket,
                    file_name=f"alerts/{alert_filename}",
                    json_data=alert_data
                )
                
                if alert_success:
                    print(f"🚨 Alerts generated: {len(alerts)} alerts")
                    for alert in alerts:
                        print(f"   - {alert['severity'].upper()}: {alert['message']}")
                    
                    # Send webhook notification (simulated)
                    webhook_url = monitoring_config.get("alert_webhook")
                    if webhook_url:
                        print(f"📧 Alert notification sent to: {webhook_url}")
            else:
                print("✅ All systems normal - no alerts")
        
        return metrics, alerts
    
    # Collect metrics
    metrics, alerts = collect_system_metrics()


if __name__ == "__main__":
    """Run all combined examples"""
    print("🔗 ZionAI Utils - Combined Examples (Secrets + Storage)\n")
    
    try:
        # Run examples
        example_complete_app_initialization()
        example_document_processing_pipeline()
        example_automated_reporting_system()
        example_multi_environment_deployment()
        example_data_backup_and_sync()
        example_real_zioncloud_application()
        example_monitoring_and_alerting()
        
        print("\n🎉 All combined examples completed successfully!")
        print("\nKey takeaways:")
        print("✅ Secrets Manager + GCS Client work seamlessly together")
        print("✅ Configuration is centralized and secure")
        print("✅ Applications can be fully automated and self-documenting")
        print("✅ Real-world ZionClouds patterns are simple and reliable")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nTroubleshooting checklist:")
        print("1. ✅ Valid GCP credentials configured")
        print("2. ✅ Secret Manager API enabled")
        print("3. ✅ Cloud Storage API enabled") 
        print("4. ✅ Appropriate IAM permissions")
        print("5. ✅ Test secrets and buckets created")
        print("6. ✅ Project ID correctly specified")