from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import os

source_conn = os.getenv("SOURCE_CONN")
dest_conn = os.getenv("DEST_CONN")

source_client = BlobServiceClient.from_connection_string(source_conn)
dest_client = BlobServiceClient.from_connection_string(dest_conn)

source_container = source_client.get_container_client("source")
dest_container = dest_client.get_container_client("dest")

if not source_container.exists():
    source_container.create_container()
if not dest_container.exists():
    dest_container.create_container()

for i in range(100):
    blob_name = f"file_{i}.txt"
    data = f"This is blob number {i}".encode("utf-8")
    print(f"Uploading {blob_name} to source container")
    source_container.upload_blob(name=blob_name, data=data)
    print(f"Uploaded {blob_name} to source container")

    sas_token = generate_blob_sas(
        account_name=source_client.account_name,
        container_name="source",
        blob_name=blob_name,
        account_key=source_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now() + timedelta(hours=1)
    )

    print(f"Copying {blob_name} from source container to dest container")
    # Copy blob
    source_url = source_container.get_blob_client(blob_name).url + "?" + sas_token
    dest_container.get_blob_client(blob_name).start_copy_from_url(source_url)
    print(f"Copied {blob_name} from source container to dest container")
