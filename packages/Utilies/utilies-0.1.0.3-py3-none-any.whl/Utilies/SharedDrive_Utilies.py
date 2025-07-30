import logging
import os
import re
from datetime import datetime

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from concurrent.futures import ThreadPoolExecutor
import logging
from smbclient import getxattr, listxattr, \
    mkdir, register_session, remove, rmdir, setxattr, smbclient, symlink, unlink, utime

from smbclient import listdir

import smbclient
import traceback
import threading
import queue


class ShareDrive_Utilities:

    def __init__(self, username, password, hostname, port=None):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.register_session = None

    def login(self):
        """
        Registers the session with the SMB server using the provided credentials.
        """
        self.register_session = register_session(self.hostname, username=self.username, password=self.password,
                                                 port=self.port if self.port else 445)
        logging.info(f"Logged into server: {self.hostname}")

    def reconnect(self):
        """
        Re-registers the session in case it dropped
        :return:  activate the session and store in init
        """

        print(f"[Reconnect] Reconnecting to {self.hostname}")
        smbclient.register_session(self.hostname, username=self.username, password=self.password)
        logging.info(f"Logged into server: {self.hostname}")

    def logout(self):
        """
        Logs out by closing the SMB session.
        """
        if self.register_session:
            self.register_session.disconnect()
            logging.info("Logged out of the server.")
        else:
            raise Exception("Session not logged in.")

    def check_session(self):
        """
        Verifies the session is logged in and the path is a valid directory on the SMB share.
        return : if session is active else False
        """
        if not self.register_session:
            print("Session not logged in.")
            return False
        return True

    def check_directory(self, path):
        """
        Verifies the session is logged in and the path is a valid directory on the SMB share.
        return : if session is active else False
        """
        try:
            file_info = smbclient.stat(path)
            print("Directory is exit")
            logging.info("Directory is exit")
            return True
        except Exception as e:
            print(e)
            logging.warning("Directory does not is exit")
        return False

    def list_details(self, path):
        """
        Lists the files and directories at the given path.
        :returns : List of files and directories
        """
        if self.check_session_directory(path) and self.path_exists(path):
            return listdir(path)
        elif not self.path_exists(path):
            print(f"No Path exist : {path}")
        elif not self.check_session_directory(path):
            print(f"No Path exist : {path}")
        return []

    def is_connected(self, test_path):
        try:
            smbclient.listdir(test_path)
            return True
        except Exception:
            return False

    def download_file_from_smb(self, remote_path, local_path):
        """
        :param remote_path: remote path where the files need to download
        :param local_path:  Local Path where it should be saved
        :return: NA
        """
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        try:
            # Check connection
            if not self.is_connected(remote_path):
                self.reconnect()

            file_info = smbclient.stat(remote_path)
            if not file_info.st_mode & 0o40000:  # Not a directory
                with smbclient.open_file(remote_path, mode='rb') as smb_file:
                    with open(local_path, mode='wb') as local_file:
                        while chunk := smb_file.read(4096):
                            local_file.write(chunk)
                print(f"[Downloaded] {remote_path} -> {local_path}")
        except Exception as e:
            print(f"[Error] Failed to download {remote_path}: {e}")
            traceback.print_exc()

    def download_worker(self, task_queue):
        """
        :param task_queue: help to schedule a individual Task
        :return:
        """
        while not task_queue.empty():
            try:
                remote_path, local_path = task_queue.get()
                self.download_file_from_smb(remote_path, local_path)
                task_queue.task_done()
            except Exception as e:
                print(f"[Worker Error] {e}")
                traceback.print_exc()
                task_queue.task_done()

    def matches_filters(self, filename, file_info, filters):
        """
        :param filename: string (filename)
        :param file_info: file information like create, modified, accessed
        :param filters: filters to apply
        :return: True/False
        """

        # Starts/Ends with (handles multiple values separated by semicolons)
        if 'starts_with' in filters:
            starts_with_values = filters['starts_with'].split(';')
            if any(filename.startswith(value) for value in starts_with_values):
                return True

        if 'ends_with' in filters:
            ends_with_values = filters['ends_with'].split(';')
            if any(filename.endswith(value) for value in ends_with_values):
                return True

        # Contains filter (handles multiple values separated by semicolons)
        if 'contains' in filters:
            contains_values = filters['contains'].split(';')  # Split by semicolon
            if any(substring in filename for substring in contains_values):  # Check if any value is in filename
                return True

        # Negation filters (handles multiple values separated by semicolons)
        if 'not_contains' in filters:
            not_contains_values = filters['not_contains'].split(';')
            if any(substring not in filename for substring in not_contains_values):
                return True

        if 'not_extension' in filters:
            not_extension_values = filters['not_extension'].split(';')
            if any(not filename.endswith(ext) for ext in not_extension_values):
                return True

        if 'not_regex' in filters:
            not_regex_values = filters['not_regex'].split(';')
            if any(not re.search(regex, filename) for regex in not_regex_values):
                return True

        # Created time (no need for semicolon handling, as it's a single value)
        ctime = datetime.fromtimestamp(file_info.st_ctime)
        if 'created_after' in filters and ctime < filters['created_after']:
            return True
        if 'created_before' in filters and ctime > filters['created_before']:
            return True

        # Accessed time (no need for semicolon handling, as it's a single value)
        atime = datetime.fromtimestamp(file_info.st_atime)
        if 'accessed_after' in filters and atime < filters['accessed_after']:
            return True
        if 'accessed_before' in filters and atime > filters['accessed_before']:
            return True

        # Modified within N days (no need for semicolon handling, as it's a single value)
        mtime = datetime.fromtimestamp(file_info.st_mtime)
        if 'modified_within_days' in filters:
            delta = datetime.now() - mtime
            if delta.days > filters['modified_within_days']:
                return True

        # Custom lambda filter (no need for semicolon handling, as it's a single function)
        if 'custom_filter' in filters and callable(filters['custom_filter']):
            if filters['custom_filter'](filename, file_info):
                return True

        return False

    def download_all_files_from_smb(self, remote_path, local_path, num_threads=4, filters=None, limit=None,
                                    bottom=False):
        """
        :param remote_path: where the Files are present in Remote
        :param local_path:  where we have to save the  downloaded files
        :param num_threads:  its integer value how many worked need to assign
        :param filters:  if filters need then we have to sent in dictory
        :param limit: is any limit of downloades
        :param bottom:  if bottom files need to download then this
        :return:NA
        """
        os.makedirs(local_path, exist_ok=True)
        task_queue = queue.Queue()
        file_tasks = []

        # Populate the list with filtered file tasks
        for entry in smbclient.listdir(remote_path):
            full_remote_path = os.path.join(remote_path, entry)
            full_local_path = os.path.join(local_path, entry)

            try:
                file_info = smbclient.stat(full_remote_path)
                if file_info.st_mode & 0o40000:
                    # If it's a directory, recursively walk
                    self.download_all_files_from_smb(full_remote_path, full_local_path, num_threads, filters, limit,
                                                     bottom)
                else:
                    if self.matches_filters(entry, file_info, filters):
                        print(f"File Matched adding to task list :{file_info}")
                        file_tasks.append((full_remote_path, full_local_path, file_info.st_mtime))
            except Exception as e:
                print(f"[Error] Skipping {full_remote_path}: {e}")
                traceback.print_exc()

        # Sort files by modified time if using top/bottom record limit
        if limit is not None:
            file_tasks.sort(key=lambda x: x[2], reverse=bottom)
            file_tasks = file_tasks[:limit]

        # Queue the filtered file tasks
        for remote, local, _ in file_tasks:
            task_queue.put((remote, local))

        # Start threads
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=self.download_worker, args=(task_queue,))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()

        print("[Done] All files downloaded.")

    def check_session_directory(self, path):
        """
        Verifies the session is logged in and the path is a valid directory on the SMB share.
        :return check the path is folder /Dictory path the return True/ False based on that
        """
        if not self.register_session:
            print("Session not logged in.")
            return False
        try:
            file_info = smbclient.stat(path)
            if not file_info.st_mode & 0o40000:  # If not a directory
                print(f"Path '{path}' is not a directory.")
                return False
        except Exception as e:
            print(f"Error checking path '{path}': {e}")
            return False
        return True

    def download_folder(self, server_folder_path, local_folder_path):
        """
        Downloads an entire folder from the SMB server to a local path, including all subfolders and files.
        """
        if self.check_session_directory(server_folder_path):
            # Ensure the local folder exists
            if not os.path.exists(local_folder_path):
                os.makedirs(local_folder_path)
                logging.info(f"Created local directory: {local_folder_path}")

            # Traverse the directory contents
            for item in smbclient.listdir(server_folder_path):
                server_item_path = os.path.join(server_folder_path, item)
                local_item_path = os.path.join(local_folder_path, item)

                try:
                    # Check if the item is a directory
                    file_info = smbclient.stat(server_item_path)
                    if file_info.st_mode & 0o40000:  # Directory check
                        logging.info(f"Found directory: {item}, downloading recursively...")
                        self.download_folder(server_item_path, local_item_path)  # Recursive call
                    else:
                        smbclient.copyfile(server_item_path, local_item_path)
                        logging.info(f"Downloaded file: {item} to {local_item_path}")
                except Exception as e:
                    logging.warning(f"Skipping item {item} due to error: {e}")

    def filter_file(self, file, filters):
        """
        Apply filters to check if the file should be uploaded.
        Returns True if file passes the filters, False otherwise.
        """
        # Starts/Ends with (handles multiple values separated by semicolons)
        if 'starts_with' in filters:
            starts_with_values = filters['starts_with'].split(';')
            if any(file.startswith(value) for value in starts_with_values):
                return True

        if 'ends_with' in filters:
            ends_with_values = filters['ends_with'].split(';')
            if any(file.endswith(value) for value in ends_with_values):
                return True

        # Contains filter (handles multiple values separated by semicolons)
        if 'contains' in filters:
            contains_values = filters['contains'].split(';')
            if any(substring in file for substring in contains_values):
                return True

        # Negation filters (handles multiple values separated by semicolons)
        if 'not_contains' in filters:
            not_contains_values = filters['not_contains'].split(';')
            if any(substring not in file for substring in not_contains_values):
                return True

        if 'not_extension' in filters:
            not_extension_values = filters['not_extension'].split(';')
            if any(not file.endswith(ext) for ext in not_extension_values):
                return True

        if 'regex' in filters:
            regex_values = filters['regex'].split(';')
            if any(re.match(regex, file) for regex in regex_values):
                return True

        # Created time (no need for semicolon handling, as it's a single value)
        if 'created_after' in filters:
            created_time = datetime.fromtimestamp(os.path.getctime(file))
            if created_time < filters['created_after']:
                return True

        # Accessed time (no need for semicolon handling, as it's a single value)
        if 'accessed_before' in filters:
            accessed_time = datetime.fromtimestamp(os.path.getatime(file))
            if accessed_time > filters['accessed_before']:
                return True

        # Modified within N days (no need for semicolon handling, as it's a single value)
        if 'modified_within_days' in filters:
            modified_time = datetime.fromtimestamp(os.path.getmtime(file))
            if (datetime.now() - modified_time).days > filters['modified_within_days']:
                return True

        # File size greater than (handles a single value)
        if 'size_gt' in filters:
            if os.path.getsize(file) <= filters['size_gt']:
                return True

        # Negation regex (handles multiple values separated by semicolons)
        if 'not_regex' in filters:
            not_regex_values = filters['not_regex'].split(';')
            if any(not re.match(regex, file) for regex in not_regex_values):
                return True

        # Custom lambda filter (no need for semicolon handling, as it's a single function)
        if 'custom_filter' in filters:
            if filters['custom_filter'](file, os.stat(file)):
                return True

        return False

    def upload_file(self, server_path, local_path, filters=None, max_threads=4):
        """
        Uploads files from a local path to the SMB server recursively with filters and multithreading.
        :param server_path: The SMB server path to upload files to
        :param local_path: The local path to search for files
        :param filters: A dictionary of filters to apply to the files
        :param max_threads: The maximum number of concurrent threads to use
        :return:    NA
        """

        if not self.check_session_directory(server_path):
            self.create_directory(server_path)  # Create the server directory if it doesn't exist

        # Initialize ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Walk through all directories and files under local_path recursively
            for root, dirs, files in os.walk(local_path):
                # Determine the relative directory path on the server
                relative_path = os.path.relpath(root, local_path)
                server_subdir = os.path.join(server_path, relative_path)

                # Create directories on the SMB server if they don't exist
                if not self.check_session_directory(server_subdir):
                    self.create_directory(server_subdir)

                # Submit file upload tasks to executor
                for file in files:
                    local_file_path = os.path.join(root, file)
                    server_file_path = os.path.join(server_subdir, file)

                    # Apply filters before submitting the upload task
                    if filters and self.filter_file(local_file_path, filters):
                        logging.info(f"Skipping file due to filter: {local_file_path}")
                        print(f"Skipping file due to filter: {local_file_path}")
                        continue

                    # Submit the file upload task to the executor
                    executor.submit(self.upload_single_file, local_file_path, server_file_path)

    def upload_single_file(self, local_file_path, server_file_path):
        """
        Upload a single file to the SMB server.
        This method is called by the thread pool to upload files concurrently.
        :param local_file_path : The local path of the file to upload
        :param server_file_path : The SMB server path to upload the file to
        """
        try:
            with smbclient.open_file(server_file_path, mode="wb") as server_fd:
                # Open local file in binary read mode
                with open(local_file_path, "rb") as local_fd:
                    # Write the contents of the local file to the server file
                    server_fd.write(local_fd.read())

            logging.info(f"Successfully uploaded file: {local_file_path} to {server_file_path}")
        except Exception as e:
            # If there's an error, log it but do not leave a corrupted file
            logging.error(f"Failed to upload file {local_file_path} to {server_file_path}: {e}")

    def create_directory(self, path):
        """
        Creates a directory on the SMB share.
        :param path: make the diretory if not present
        """
        if not self.check_session_directory(path):
            mkdir(path)
            logging.info(f"Directory created: {path}")
            print(f"Directory created: {path}")

    def remove_file(self, file_path):
        """
        Removes a file from the SMB share.
        :param file_path: remove the filepath
        """
        try:
            # Check if the old_path exists and its type (file or directory)
            try:
                file_info = smbclient.stat(file_path)
            except Exception as e:
                logging.error(f"Path {file_path} does not exist on the SMB server.")

            remove(file_path)
            print(f"File removed: {file_path}")
            logging.info(f"File removed: {file_path}")
        except Exception as e:
            logging.info(f"File removed: {file_path}")
            print(e)

    def remove_directory(self, dir_path):
        """
        Removes a directory from the SMB share.
        :param dir_path: remove the directory path
        """
        if self.check_session_directory(dir_path):
            rmdir(dir_path)
            print(f"Directory removed: {dir_path}")
            logging.info(f"Directory removed: {dir_path}")

    def rename_file_or_folder(self, old_path, new_path):
        """
        Renames a file or folder on the SMB share. Automatically checks if it's a file or folder.
        :param old_path : The SMB server path of the file or folder to rename
        :param new_path: The new SMB server path of the file or folder
        """
        try:
            # Check if the old_path exists and its type (file or directory)
            try:
                file_info = smbclient.stat(old_path)
            except Exception as e:
                logging.error(f"Path {old_path} does not exist on the SMB server.")
                return

            # Determine if it's a file or directory
            if os.path.isfile(old_path):  # This checks the local file, assuming smbclient.stat gave a valid result
                # It's a file, proceed with renaming
                smbclient.rename(old_path, new_path)
                logging.info(f"Renamed file {old_path} to {new_path}")
            elif os.path.isdir(old_path):  # This checks if it is a folder
                # It's a folder, proceed with renaming
                smbclient.rename(old_path, new_path)
                logging.info(f"Renamed folder {old_path} to {new_path}")
            else:
                # The path doesn't exist as a file or folder
                logging.error(f"Path {old_path} does not exist or is not a file or folder.")
        except Exception as e:
            logging.error(f"Failed to rename {old_path} to {new_path}: {e}")

    def path_exists(self, path):
        """
        Checks if a file or directory exists at the specified path.
        :param path: its check path is there r not if not False else True
        """
        try:
            listdir(path)
            return True
        except:
            return False

    def make_directories(self, path):
        """
        Creates multiple nested directories
        :param path : make the directory if not present in Server
        """
        if not self.path_exists(path):
            mkdir(path)
            logging.info(f"Created directories: {path}")
        else:
            logging.info(f"Directory already exists: {path}")

    def create_symlink(self, target, link_name):
        """
        Creates a symbolic link on the SMB share.
        :param link_name: its add link_name for target
        """
        if self.check_directory(target):
            symlink(target, link_name)
            logging.info(f"Created symlink: {link_name} -> {target}")

    def remove_symlink(self, symlink_path):
        """
        Removes a symbolic link from the SMB share.
        :param symlink_path: its remove link_name for target
        """
        if self.check_directory(symlink_path):
            unlink(symlink_path)
            logging.info(f"Removed symlink: {symlink_path}")

    def set_xattr(self, file_path, attribute_name, value):
        """
        Sets an extended attribute for a file on the SMB share.
        :param file_path: its add attribute_name for target
        """
        if self.check_directory(file_path):
            setxattr(file_path, attribute_name, value)
            logging.info(f"Set extended attribute: {attribute_name} for {file_path}")

    def get_xattr(self, file_path, attribute_name):
        """
        Gets an extended attribute of a file from the SMB share.
        """
        try:
            file_info = smbclient.stat(file_path)
        except Exception as e:
            logging.error(f"Path {file_path} does not exist on the SMB server.")
            print(f"Path {file_path} does not exist on the SMB server.")
            return
        try:
            return getxattr(file_path, attribute_name)
        except Exception as e:
            print(e)
        return None

    def list_xattr(self, file_path):
        """
        Lists all extended attributes for a file on the SMB share.
        """
        try:
            file_info = smbclient.stat(file_path)
        except Exception as e:
            logging.error(f"Path {file_path} does not exist on the SMB server.")
            print(f"Path {file_path} does not exist on the SMB server.")
            return
        try:
            return listxattr(file_path)
        except Exception as e:
            print(e)

        return []

    def set_file_time(self, file_path, atime, mtime):
        """
        Sets the access and modification times of a file.
        """
        try:
            file_info = smbclient.stat(file_path)
        except Exception as e:
            logging.error(f"Path {file_path} does not exist on the SMB server.")
            print(f"Path {file_path} does not exist on the SMB server.")
            return

        try:

            utime(file_path, (int(atime), int(mtime)))
            logging.info(f"Set file times for: {file_path}")
            print(f"Set file times for: {file_path}")
        except Exception as e:
            print(f"Fail to times for: {file_path}")
