# Integrating Google Cloud Storage RAG Source

# This code sets up the integration for Google Cloud Storage with the flooring chat agent.

from google.cloud import storage

class FlooringChatAgent:
    def __init__(self, project_id, bucket_name):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.storage_client = storage.Client(project=self.project_id)

    def list_files(self):
        # List all files in the bucket
        blobs = self.storage_client.list_blobs(self.bucket_name)
        return [blob.name for blob in blobs]

    def download_file(self, file_name):
        # Download a file from the bucket
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(file_name)
        print(f'Downloaded {file_name} from bucket {self.bucket_name}.')