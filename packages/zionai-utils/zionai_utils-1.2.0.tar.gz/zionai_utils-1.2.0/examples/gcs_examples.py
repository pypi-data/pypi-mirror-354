"""
Google Cloud Storage Examples

This file contains practical examples of using the GCSClient for various
file upload scenarios in ZionClouds projects.
"""

import os
import json
from datetime import datetime
from zionai_utils import GCSClient

# Initialize the client
# Option 1: With explicit credentials
client = GCSClient(
    project_id="your-project-id",
    credentials_path="/path/to/service-account.json"
)

# Option 2: Using environment variables (recommended for production)
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
# export GOOGLE_CLOUD_PROJECT="your-project-id"
# client = GCSClient()

def example_basic_file_upload():
    """Example 1: Basic file upload"""
    print("=== Basic File Upload ===")
    
    # Upload any file
    success, gcs_uri = client.upload_file(
        bucket_name="zion-documents",
        file_path="document.pdf"
    )
    
    if success:
        print(f"✅ Uploaded: {gcs_uri}")
    else:
        print("❌ Upload failed")


def example_text_upload():
    """Example 2: Upload text content directly"""
    print("\n=== Text Content Upload ===")
    
    # Create a simple report
    report_content = f"""
    Daily Report - {datetime.now().strftime('%Y-%m-%d')}
    
    Status: All systems operational
    Users: 1,250 active
    Revenue: $15,420
    """
    
    success, gcs_uri = client.upload_text(
        bucket_name="zion-reports",
        file_name="daily-report.txt",
        text_content=report_content,
        meta_data={
            "report_type": "daily",
            "generated_by": "zionai_utils",
            "timestamp": datetime.now().isoformat()
        }
    )
    
    if success:
        print(f"✅ Report uploaded: {gcs_uri}")


def example_json_upload():
    """Example 3: Upload JSON data"""
    print("\n=== JSON Data Upload ===")
    
    # Create analytics data
    analytics_data = {
        "date": datetime.now().isoformat(),
        "metrics": {
            "page_views": 5420,
            "unique_visitors": 1230,
            "bounce_rate": 0.23,
            "conversion_rate": 0.045
        },
        "top_pages": [
            "/dashboard",
            "/analytics",
            "/reports"
        ]
    }
    
    success, gcs_uri = client.upload_json(
        bucket_name="zion-analytics",
        file_name="analytics-data.json",
        json_data=analytics_data,
        meta_data={
            "data_type": "analytics",
            "source": "web_analytics"
        }
    )
    
    if success:
        print(f"✅ Analytics data uploaded: {gcs_uri}")


def example_batch_upload():
    """Example 4: Upload multiple files at once"""
    print("\n=== Batch File Upload ===")
    
    # List of files to upload
    files_to_upload = [
        "report1.pdf",
        "report2.pdf", 
        "data.csv",
        "presentation.pptx"
    ]
    
    # Upload all files with a prefix
    results = client.batch_upload(
        bucket_name="zion-batch-uploads",
        file_paths=files_to_upload,
        prefix="daily-batch/",
        meta_data={
            "batch_id": "daily-001",
            "upload_date": datetime.now().isoformat()
        }
    )
    
    # Show results
    for file_path, (success, gcs_uri) in results.items():
        if success:
            print(f"✅ {file_path} -> {gcs_uri}")
        else:
            print(f"❌ Failed: {file_path}")


def example_client_document_processing():
    """Example 5: Real ZionClouds use case - Client document processing"""
    print("\n=== Client Document Processing ===")
    
    def process_client_documents(client_name, documents_folder):
        """Process and upload client documents with organized structure"""
        
        if not os.path.exists(documents_folder):
            print(f"❌ Folder not found: {documents_folder}")
            return
        
        uploaded_count = 0
        failed_count = 0
        
        for filename in os.listdir(documents_folder):
            file_path = os.path.join(documents_folder, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Create organized destination path
            file_extension = os.path.splitext(filename)[1].lower()
            document_type = get_document_type(file_extension)
            destination_name = f"clients/{client_name}/{document_type}/{filename}"
            
            success, gcs_uri = client.upload_file(
                bucket_name="zion-client-documents",
                file_path=file_path,
                destination_name=destination_name,
                meta_data={
                    "client": client_name,
                    "document_type": document_type,
                    "upload_date": datetime.now().isoformat(),
                    "processed_by": "zionai_utils",
                    "file_size": str(os.path.getsize(file_path))
                }
            )
            
            if success:
                print(f"✅ {filename} -> {gcs_uri}")
                uploaded_count += 1
            else:
                print(f"❌ Failed: {filename}")
                failed_count += 1
        
        print(f"\nSummary: {uploaded_count} uploaded, {failed_count} failed")
    
    def get_document_type(file_extension):
        """Categorize documents by type"""
        document_types = {
            '.pdf': 'documents',
            '.doc': 'documents',
            '.docx': 'documents',
            '.xls': 'spreadsheets',
            '.xlsx': 'spreadsheets',
            '.csv': 'data',
            '.jpg': 'images',
            '.jpeg': 'images',
            '.png': 'images',
            '.ppt': 'presentations',
            '.pptx': 'presentations'
        }
        return document_types.get(file_extension, 'other')
    
    # Process documents for a client
    process_client_documents("acme-corp", "/path/to/client/documents")


def example_automated_report_generation():
    """Example 6: Automated report generation and upload"""
    print("\n=== Automated Report Generation ===")
    
    def generate_and_upload_report():
        """Generate a business report and upload to GCS"""
        
        # Simulate report data (in real scenario, this would come from database)
        report_data = {
            "report_id": f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "metrics": {
                "total_revenue": 125000,
                "new_customers": 45,
                "active_projects": 12,
                "team_utilization": 0.87
            },
            "summary": "Strong performance this quarter with increased revenue and customer acquisition."
        }
        
        # Generate report filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"business-report_{timestamp}.json"
        
        # Upload the report
        success, gcs_uri = client.upload_json(
            bucket_name="zion-business-reports",
            file_name=f"reports/{report_filename}",
            json_data=report_data,
            meta_data={
                "report_type": "business_summary",
                "auto_generated": "true",
                "format": "json",
                "retention_period": "7_years"
            }
        )
        
        if success:
            print(f"✅ Business report generated: {gcs_uri}")
            return gcs_uri
        else:
            print("❌ Failed to generate report")
            return None
    
    # Generate and upload report
    report_uri = generate_and_upload_report()


def example_file_management():
    """Example 7: File management operations"""
    print("\n=== File Management Operations ===")
    
    bucket_name = "zion-test-bucket"
    
    # List files in bucket
    print("Listing files in bucket...")
    files = client.list_files(bucket_name, prefix="reports/")
    print(f"Found {len(files)} files:")
    for file_name in files[:5]:  # Show first 5 files
        print(f"  - {file_name}")
    
    # Upload a test file
    test_content = "This is a test file for deletion"
    success, gcs_uri = client.upload_text(
        bucket_name=bucket_name,
        file_name="temp/test-file.txt",
        text_content=test_content
    )
    
    if success:
        print(f"✅ Test file uploaded: {gcs_uri}")
        
        # Delete the test file
        deleted = client.delete_file(bucket_name, "temp/test-file.txt")
        if deleted:
            print("✅ Test file deleted successfully")
        else:
            print("❌ Failed to delete test file")


def example_public_file_upload():
    """Example 8: Upload files with public access"""
    print("\n=== Public File Upload ===")
    
    # Upload a public file (like a shared document or image)
    public_content = """
    ZionClouds Public Information
    
    This document contains publicly available information about our services.
    Contact us at: info@zionclouds.com
    """
    
    success, gcs_uri = client.upload_text(
        bucket_name="zion-public-content",
        file_name="public/company-info.txt",
        text_content=public_content,
        make_public=True,
        meta_data={
            "access_level": "public",
            "content_type": "informational"
        }
    )
    
    if success:
        print(f"✅ Public file uploaded: {gcs_uri}")
        print("📝 File is now publicly accessible")


if __name__ == "__main__":
    """Run all examples"""
    print("🚀 ZionAI Utils - GCS Examples\n")
    
    try:
        example_basic_file_upload()
        example_text_upload()
        example_json_upload()
        # example_batch_upload()  # Uncomment if you have test files
        example_client_document_processing()
        example_automated_report_generation()
        example_file_management()
        example_public_file_upload()
        
        print("\n✅ All examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Valid GCP credentials configured")
        print("2. Appropriate bucket permissions")
        print("3. Buckets created in your project")