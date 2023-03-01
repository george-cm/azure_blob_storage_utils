from azure.storage.blob import BlockBlobService, PublicAccess
import easygui as g

# import csv
# from urllib.parse import quote
# from datetime import datetime
# import os, uuid
import sys
from pathlib import Path
from zipfile import ZipFile
from dam_file_name import DamFileName
from secrets_his import blobs as his_blobs


def create_blob(filepath):
    # his_blobs has the following shape:
    # blobs = {
    #     "ezconfig": {
    #         "storage_account_name": "...",
    #         "storage_account_key": "...",
    #         "sas": "",
    #         "is_emulated": False,
    #         "container_name": "...",
    #     }
    # }

    blobs = his_blobs
    blob_url = ""
    try:
        local_file_name = filepath.name
        full_path_to_file = filepath.as_posix()

        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(
            account_name=blobs["ezconfig"]["storage_account_name"],
            account_key=blobs["ezconfig"]["storage_account_key"],
        )
        container_name = blobs["ezconfig"]["container_name"]

        # Upload the created file, use local_file_name for the blob name.
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
        # blob_metadata = block_blob_service.get_blob_metadata(container_name, local_file_name)
        # blob_properties = block_blob_service.get_blob_properties(container_name, local_file_name)
        status = block_blob_service.exists(container_name, local_file_name)
        if status:
            print(f"Upload successful")
            blob_url = block_blob_service.make_blob_url(container_name, local_file_name)
        #   print(blobl_url)
        # print(blob_metadata)
        # print(blob_properties)
        else:
            print(f"Upload failed")

        return blob_url

    except Exception as ex:
        print("Exception:")
        print(ex)
        sys.exit(1)


def main():
    # get the exe file that needs to be uploaded to Azure
    inputf = g.fileopenbox(
        "Select the exe file to upload to Azure Storage",
        "Azure Storage Uploader",
        default="./*.exe",
        filetypes=["*.exe"],
    )

    if inputf is None:
        g.msgbox(msg="You haven'nt selected any file. Exiting.", ok_button="Ok")
        sys.exit(0)

    # sys.exit(0)
    input_file = Path(inputf)
    print(input_file.as_posix())
    dfn = DamFileName()
    zip_file = Path(input_file.parent, dfn.create_proper_name_wo_suffix(input_file.stem) + ".zip")
    url_file = Path(
        input_file.parent,
        dfn.create_proper_name_wo_suffix(input_file.stem) + "_url.log",
    )
    print(zip_file.as_posix())
    with ZipFile(zip_file.as_posix(), "w") as zip_archive:
        zip_archive.write(input_file.as_posix(), input_file.name)

    blob_url = create_blob(zip_file)
    if blob_url != "":
        print(f"url: {blob_url}")
        g.msgbox(msg="URL: " + blob_url, title="Upload successfull", ok_button="Ok")
        with open(url_file.as_posix(), "w") as url_f:
            url_f.write(blob_url)
    else:
        g.msgbox(msg="Upload failed.", title="Upload failed.", ok_button="Ok")


if __name__ == "__main__":
    main()
