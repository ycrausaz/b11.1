import boto3
import os
from botocore.config import Config
from typing import Dict, List
from django.conf import settings

def get_storage_config(is_divio: bool = False) -> Dict:
    """
    Get the appropriate S3/MinIO configuration from Django settings.
    
    Args:
        is_divio (bool): Flag to determine if using Divio production environment
    
    Returns:
        Dict: Configuration dictionary for boto3 client
    """
    config = {
        'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
        'bucket_name': settings.AWS_STORAGE_BUCKET_NAME
    }
    
    if is_divio:
        # Production (Divio) settings
        config['region_name'] = settings.AWS_S3_REGION_NAME
        config['endpoint_url'] = None  # Use default AWS endpoints
    else:
        # Development (MinIO) settings
        config['region_name'] = None
        config['endpoint_url'] = settings.AWS_S3_ENDPOINT_URL
    
    return config

def list_bucket_contents(config: Dict) -> List[Dict]:
    """
    Recursively list all objects in the S3/MinIO bucket.
    
    Args:
        config (Dict): Storage configuration dictionary
    
    Returns:
        List[Dict]: List of objects with their details
    """
    # Create boto3 client with appropriate configuration
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        region_name=config['region_name'],
        endpoint_url=config.get('endpoint_url'),  # Only present for MinIO
        config=Config(signature_version='s3v4')  # Ensure compatibility
    )
    
    objects = []
    paginator = s3_client.get_paginator('list_objects_v2')
    
    try:
        # Use paginator to handle buckets with many objects
        for page in paginator.paginate(Bucket=config['bucket_name']):
            if 'Contents' in page:
                for obj in page['Contents']:
                    # Get detailed information about each object
                    objects.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'storage_class': obj.get('StorageClass', 'STANDARD')
                    })
    except Exception as e:
        print(f"Error listing bucket contents: {str(e)}")
        return []
    
    return objects

def print_bucket_contents(objects: List[Dict], environment: str):
    """
    Print the contents of the bucket in a formatted way.
    
    Args:
        objects (List[Dict]): List of objects with their details
        environment (str): Name of the environment (Development/Production)
    """
    print(f"\n{environment} Environment Bucket Contents:")
    print("-" * 80)
    print(f"{'Object Key':<50} {'Size (bytes)':<15} {'Last Modified':<20}")
    print("-" * 80)
    
    for obj in objects:
        print(
            f"{obj['key']:<50} "
            f"{obj['size']:<15} "
            f"{obj['last_modified'].strftime('%Y-%m-%d %H:%M:%S'):<20}"
        )
    print(f"\nTotal objects: {len(objects)}")

def main():
    """
    Main function to list contents of both development and production buckets.
    """
    # List contents based on current Django settings
    is_divio = getattr(settings, 'DIVIO_HOSTING', False)
    environment = "Production (Divio)" if is_divio else "Development (MinIO)"
    
    config = get_storage_config(is_divio)
    objects = list_bucket_contents(config)
    print_bucket_contents(objects, environment)

if __name__ == "__main__":
    # Setup Django environment
    import os
    import django
    
    # Set the Django settings module path
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LBA.settings')
    django.setup()
    
    main()
