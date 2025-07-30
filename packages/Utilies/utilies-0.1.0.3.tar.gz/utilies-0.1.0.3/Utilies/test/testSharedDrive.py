import logging
import os.path
import time
from datetime import datetime

from Utilies.SharedDrive import ShareDrive_Utilities

# Enable logging for visibility
logging.basicConfig(level=logging.INFO)


def test_share_drive_utilities():
    # Replace these with actual credentials and paths
    username = ""
    password = ""
    hostname = ""
    share_path = r""
    local_test_file = r""
    test_folder = f"{share_path}\\TestFolder"
    list_details = fr"{share_path}"
    # Prepare a local test file
    with open(local_test_file, "w") as f:
        f.write("This is a test file.")

    # Initialize utility
    smb_util = ShareDrive_Utilities(username, password, hostname)

    try:
        smb_util.login()

        # Create directory
        smb_util.create_directory(test_folder)

        # Upload file
        smb_util.upload_file(test_folder, '',
                             filters={
                                 'starts_with': 'SIILR',
                                 'ends_with': '.txt',
                                 'not_contains': 'SIILR_ES_EQUATE_ISSUED_ESB58481151_20170710060918',
                                 'not_extension': '.tmp',
                                 'regex': r'^log_\d+\.gz$',
                                 'created_after': datetime(2023, 1, 1),
                                 'accessed_before': datetime(2024, 12, 31),
                                 'modified_within_days': 30,
                                 'size_gt': 500,
                                 'not_regex': r'.*old.*',
                                 'custom_filter': lambda f, info: 'important' in f and info.st_size > 10_000,
                             }

                             )
        smb_util.upload_single_file(

            '',
            os.path.join(test_folder, 'Test.XLSX')
        )
        # List directory contents
        logging.info("Directory listing:")
        for item in smb_util.list_details(list_details):
            print(f" - {item}")

        # Rename the file
        smb_util.rename_file_or_folder(os.path.join(test_folder, 'Test.XLSX'),
                                       os.path.join(test_folder, 'renamed.XLSX'))

        # Download the renamed file
        smb_util.download_all_files_from_smb(test_folder, '',
                                             filters={
                                                 'starts_with': 'SIILR',
                                                 'ends_with': '.txt',
                                                 'not_contains': 'SIILR_ES_EQUATE_ISSUED_ESB58481151_20170710060918',
                                                 'not_extension': '.tmp',
                                                 'regex': r'^log_\d+\.gz$',
                                                 'created_after': datetime(2023, 1, 1),
                                                 'accessed_before': datetime(2024, 12, 31),
                                                 'modified_within_days': 30,
                                                 'size_gt': 500,
                                                 'not_regex': r'.*old.*',
                                                 'custom_filter': lambda f,
                                                                         info: 'important' in f and info.st_size > 10_000,
                                             }
                                             )

        # Delete file
        smb_util.remove_file(os.path.join(test_folder, 'renamed.XLSX'))

        # Remove directory
        smb_util.remove_directory(os.path.join(test_folder, 'Test'))

        # # Set file times
        smb_util.set_file_time(os.path.join(test_folder, 'Test.XLSX'), time.time(), time.time())

        # Get extended attribute
        attr_val = smb_util.get_xattr(os.path.join(test_folder, 'Test.XLSX'), "user.testattr")
        print("Extended attribute value:", attr_val)

        # List extended attributes
        xattrs = smb_util.list_xattr(os.path.join(test_folder, 'Test.XLSX'))
        print("All extended attributes:", xattrs)


    except Exception as e:
        logging.error(f"Test failed: {e}")
    finally:
        # smb_util.logout()
        logging.info("Test complete.")


if __name__ == '__main__':

    # Call test function
    test_share_drive_utilities()
