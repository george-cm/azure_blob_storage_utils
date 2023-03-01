from azure.storage.blob import BlockBlobService, PublicAccess
import csv
from urllib.parse import quote
from datetime import datetime
from secrets_ppr import creds as ppr_creds


def main():
    # ppr_creds has the following shape:
    # creds = [
    #     {
    #         "storage_account_name": "...",
    #         "storage_account_key": "...",
    #         "sas": "",
    #         "is_emulated": False,
    #         "container_name": "...",
    #     },
    #     {
    #         "storage_account_name": "...",
    #         "storage_account_key": "...",
    #         "sas": "",
    #         "is_emulated": False,
    #         "container_name": "...",
    #     },
    # ]

    creds = ppr_creds
    todays_date = datetime.now().strftime("%Y%m%d%H%M%S")
    for blob_creds in creds:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(
            account_name=blob_creds["storage_account_name"],
            account_key=blob_creds["storage_account_key"],
        )

        # Create a container called 'quickstartblobs'.
        container_name = blob_creds["container_name"]
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        with open(
            f"{blob_creds['storage_account_name']}_{blob_creds['container_name']}_{todays_date}.csv",
            "w",
            encoding="utf-8-sig",
            newline="",
        ) as csvout:
            writer = csv.writer(
                csvout,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writerow(
                [
                    "blob_name",
                    "blob_creation_date",
                    "blob_last_modification_date",
                    "blob_size_bytes",
                    "blob_url",
                ]
            )
            generator = block_blob_service.list_blobs(container_name)
            for blob in generator:
                print(
                    blob.name,
                    blob.properties.creation_time.strftime("%Y/%m/%d %H:%M:%S"),
                    blob.properties.last_modified.strftime("%Y/%m/%d %H:%M:%S"),
                    blob.properties.content_length,
                )
                writer.writerow(
                    [
                        blob.name,
                        blob.properties.creation_time.strftime("%Y/%m/%d %H:%M:%S"),
                        blob.properties.last_modified.strftime("%Y/%m/%d %H:%M:%S"),
                        blob.properties.content_length,
                        quote(block_blob_service.make_blob_url(blob_creds["container_name"], blob.name)),
                    ]
                )


if __name__ == "__main__":
    main()
