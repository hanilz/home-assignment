from azure.storage.blob import BlobServiceClient
import os

source_conn = os.getenv("SOURCE_CONN")
dest_conn = os.getenv("DEST_CONN")

source_client = BlobServiceClient.from_connection_string(source_conn)
dest_client = BlobServiceClient.from_connection_string(dest_conn)

source_container = source_client.get_container_client("source")
dest_container = dest_client.get_container_client("dest")

source_container.create_container()
dest_container.create_container()

for i in range(100):
    blob_name = f"file_{i}.txt"
    data = f"This is blob number {i}".encode("utf-8")
    source_container.upload_blob(name=blob_name, data=data)

    # Copy blob
    source_url = source_container.get_blob_client(blob_name).url + "?" + source_client.generate_account_shared_access_signature()
    dest_container.get_blob_client(blob_name).start_copy_from_url(source_url)
