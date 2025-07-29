from universal_mcp.applications import BaseApplication
from universal_mcp.integrations import Integration
import boto3
from typing import Optional, List, Dict, Any
import base64
from botocore.exceptions import ClientError
from universal_mcp.integrations import Integration

class AwsS3App(BaseApplication):
    """
    A class to interact with Amazon S3.
    """

    def __init__(self, integration: Integration | None = None, client = None, **kwargs):
        """
        Initializes the AmazonS3App.

        Args:
            aws_access_key_id (str, optional): AWS access key ID.
            aws_secret_access_key (str, optional): AWS secret access key.
            region_name (str, optional): AWS region name.
        """
        super().__init__(name="aws-s3", integration=integration, **kwargs)
        self._client = client
        self.integration = integration

    @property
    def client(self):
        """
        Gets the S3 client.
        """
        if not self.integration:
            raise ValueError("Integration not initialized")
        if not self._client:
            credentials = self.integration.get_credentials()
            credentials = {
                'aws_access_key_id': credentials.get('access_key_id') or credentials.get("username"),
                'aws_secret_access_key': credentials.get('secret_access_key') or credentials.get("password"),
                'region_name': credentials.get('region')
            }
            self._client = boto3.client('s3', **credentials)
        return self._client

    def list_prefixes(self, bucket_name: str, prefix: Optional[str] = None) -> List[str]:
        """
        Lists common prefixes ("folders") in the specified S3 bucket and prefix.

        Args:
            bucket_name (str): The name of the S3 bucket.
            prefix (str, optional): The prefix to list folders under.

        Returns:
            List[str]: A list of folder prefixes.
        Tags:
            important
        """
        paginator = self.client.get_paginator('list_objects_v2')
        operation_parameters = {'Bucket': bucket_name}
        if prefix:
            operation_parameters['Prefix'] = prefix
            operation_parameters['Delimiter'] = '/'
        else:
            operation_parameters['Delimiter'] = '/'

        prefixes = []
        for page in paginator.paginate(**operation_parameters):
            for cp in page.get('CommonPrefixes', []):
                prefixes.append(cp.get('Prefix'))
        return prefixes

    def put_prefix(self, bucket_name: str, prefix_name: str, parent_prefix: Optional[str] = None) -> bool:
        """
        Creates a prefix ("folder") in the specified S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.
            prefix_name (str): The name of the prefix to create.
            parent_prefix (str, optional): The parent prefix (folder path).

        Returns:
            bool: True if the prefix was created successfully.
        Tags:
            important
        """
        if parent_prefix:
            key = f"{parent_prefix.rstrip('/')}/{prefix_name}/"
        else:
            key = f"{prefix_name}/"
        self.client.put_object(Bucket=bucket_name, Key=key)
        return True

    def list_objects(self, bucket_name: str, prefix: str) -> List[Dict[str, Any]]:
        """
        Lists all objects in a specified S3 prefix.

        Args:
            bucket_name (str): The name of the S3 bucket.
            prefix (str): The prefix (folder path) to list objects under.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing object metadata.
        Tags:
            important
        """
        paginator = self.client.get_paginator('list_objects_v2')
        operation_parameters = {'Bucket': bucket_name, 'Prefix': prefix}
        objects = []
        for page in paginator.paginate(**operation_parameters):
            for obj in page.get('Contents', []):
                if not obj['Key'].endswith('/'):
                    objects.append({
                        "key": obj['Key'],
                        "name": obj['Key'].split('/')[-1],
                        "size": obj['Size'],
                        "last_modified": obj['LastModified'].isoformat() if hasattr(obj['LastModified'], "isoformat") else str(obj['LastModified'])
                    })
        return objects

    def put_object(self, bucket_name: str, prefix: str, object_name: str, content: str) -> bool:
        """
        Uploads an object to the specified S3 prefix.

        Args:
            bucket_name (str): The name of the S3 bucket.
            prefix (str): The prefix (folder path) where the object will be created.
            object_name (str): The name of the object to create.
            content (str): The content to write into the object.

        Returns:
            bool: True if the object was created successfully.
        Tags:
            important
        """
        key = f"{prefix.rstrip('/')}/{object_name}" if prefix else object_name
        self.client.put_object(Bucket=bucket_name, Key=key, Body=content.encode('utf-8'))
        return True

    def get_object_content(self, bucket_name: str, key: str) -> Dict[str, Any]:
        """
        Gets the content of a specified object.

        Args:
            bucket_name (str): The name of the S3 bucket.
            key (str): The key (path) to the object.

        Returns:
            Dict[str, Any]: A dictionary containing the object's name, content type, content (as text or base64), and size.
        Tags:
            important
        """
        try:
            obj = self.client.get_object(Bucket=bucket_name, Key=key)
            content = obj['Body'].read()
            is_text_file = key.lower().endswith(('.txt', '.csv', '.json', '.xml', '.html', '.md', '.js', '.css', '.py'))
            content_dict = {"content": content.decode('utf-8')} if is_text_file else {"content_base64": base64.b64encode(content).decode('ascii')}
            return {
                "name": key.split("/")[-1],
                "content_type": "text" if is_text_file else "binary",
                **content_dict,
                "size": len(content)
            }
        except ClientError as e:
            return {"error": str(e)}

    def delete_object(self, bucket_name: str, key: str) -> bool:
        """
        Deletes an object from S3.

        Args:
            bucket_name (str): The name of the S3 bucket.
            key (str): The key (path) to the object to delete.

        Returns:
            bool: True if the object was deleted successfully.
        Tags:
            important
        """
        try:
            self.client.delete_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError:
            return False
        
    def list_tools(self):
        return [
            self.list_prefixes,
            self.put_prefix,
            self.list_objects,
            self.put_object,
            self.get_object_content,
            self.delete_object
        ]
