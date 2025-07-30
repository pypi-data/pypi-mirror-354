✅ Python Automation Library with Excel, Web, and SFTP Utilities
This library provides reusable utilities for automating Excel, web interactions with Selenium, and secure file transfers with SSH/SFTP. It is designed to save time and effort by abstracting common tasks into simple-to-use functions.

📁 Library Structure Overview
bash
Copy
Edit
📦 automation_utils/
 ┣ 📜 __init__.py
 ┣ 📜 Utility.py                → Excel + general automation tools
 ┣ 📜 chrome.py                 → Selenium reusable web automation functions
 ┣ 📜 selenium_certificate.py   → Specialized Selenium logic for certificate selection
 ┣ 📜 sftp.py              → SSH/SFTP helper functions
 ┗ 📜 README.md
🔧 Utility.py (Excel/General Automation)
Utility.py contains reusable functions for various automation tasks related to data handling and Excel processing:

Cleaning Data:

str_to_float: Converts string columns to float and cleans data.

col_to_str: Converts columns to string and removes unwanted .0 suffix.

Sanity_Clean_df: Strips whitespace from column names and values in DataFrames.

Excel Formatting:

set_column_width: Sets column widths in an Excel worksheet.

set_header: Applies header formatting and column styles using xlsxwriter.

write_Data_to_Excel: Writes a DataFrame to Excel with optional formatting and summary rows.

Create_Pivot_Table: Creates dynamic Pivot Tables with win32com.

Excel File Management:

create_ZipFile: Creates zip archives from Excel outputs.

CleanFolder: Removes all files within a directory.

convert_Excel_to_csv: Converts an Excel file to CSV.

General Automation:

logFiles: Configures logging for error tracking.

TimeOut: Pauses script execution for specified intervals.

MailTrigger: Sends an email with optional attachments.

🌐 chrome.py (Selenium Web Automation)
chrome.py contains essential Selenium helper functions that simplify web automation tasks, especially for dynamic pages and interactions:

click_element(driver, locator): Safely clicks an element, handling waits and exceptions.

send_keys(driver, locator, text): Enters text into a field, ensuring it's ready for input.

change_download_directory(driver, path): Dynamically changes the download directory in Chrome at runtime.

extract_text(driver, locator): Extracts and returns visible text from a specified web element.

These methods are robust and include error handling and logging to ensure smooth automation in dynamic web environments.

📄 selenium_certificate.py
selenium_certificate.py focuses on automating certificate selection workflows, especially useful for secure logins that require a certificate or token:

select_certificate(driver, cert_name): Automates the selection of a digital certificate from available options (handles popups, frame switching, etc.).



🔐 sftp_util.py
sftp_util.py provides SSH/SFTP helper functions using the paramiko library for secure file handling and remote server management.

SFTP Functions:
connect(self)
Establishes an SSH connection to the remote server.

connect_server(self)
Connects to the server and prepares the session for file transfers.

put_file(self, local_file_path, remote_file_path)
Uploads a file from the local machine to the remote server.

download_file(self, remote_file_path, local_file_path)
Downloads a file from the remote server to the local machine.

upload_directory(self, local_directory, remote_directory)
Uploads an entire directory from the local machine to the remote server.

download_directory(self, remote_directory, local_directory)
Downloads an entire directory from the remote server to the local machine.

create_directory(self, remote_path)
Creates a directory on the remote server.

remove_file(self, remote_file_path)
Removes a file from the remote server.

rename_file(self, remote_old_path, remote_new_path)
Renames a file on the remote server.

rename_folder(self, remote_old_path, remote_new_path)
Renames a folder on the remote server.

list_directory(self, remote_file_path)
Lists the contents of a remote directory.

list_directory_detailed(self, remote_path)
Lists detailed information of files in the remote directory.

details_folder_file(self, path)
Retrieves detailed information about files and directories on the remote server.

current_path_details(self)
Retrieves the current path details on the remote server.

adjust_remote_path(self, remote_file_path)
Adjusts the file path on the remote server for proper file handling.

check_directory(self, directory)
Checks if a directory exists on the remote server.

set_cursor_path(self, cursor_path)
Sets the cursor path for the current file operation.

Remote Command Execution:
execute_command(self, command)
Executes a command on the remote server via SSH.

run_bat_file(self, bat_file, arguments=None)
Runs a .bat file on the remote server with optional arguments.

run_python_script(self, script_path, arguments=None)
Executes a Python script on the remote server.

run_shell_script(self, script_path, arguments=None)
Runs a shell script on the remote server.

Admin Functions:
start_service(self, service_name)
Starts a specified service on the remote server.

stop_service(self, service_name)
Stops a specified service on the remote server.

restart_service(self, service_name)
Restarts a specified service on the remote server.

kill_process(self, process_name)
Terminates a process running on the remote server.

check_service_status(self, service_name)
Checks the status of a specified service on the remote server.

check_cpu_usage(self)
Retrieves the CPU usage statistics on the remote server.

check_memory_usage(self)
Checks the memory usage on the remote server.

check_disk_usage(self)
Retrieves disk usage statistics on the remote server.

list_processes(self)
Lists all processes running on the remote server.

get_system_uptime(self)
Retrieves the system uptime on the remote server.

view_system_events(self)
Views the system event logs on the remote server.

File Handling:
file_exists(self, remote_file_path)
Checks if a specific file exists on the remote server.

get_file_size(self, remote_file_path)
Retrieves the size of a file on the remote server.

change_file_permissions(self, remote_file_path, permissions)
Changes the permissions of a file on the remote server.

move_directory(self, remote_old_path, remote_new_path)
Moves a directory on the remote server.

append_to_remote_file(self, remote_file_path, content)
Appends content to a file on the remote server.




SharedDrive_Utilies
🔹 download_file_from_smb
✅ Use to download a single file from an SMB share to the local system.

Great for transferring log files, configs, or backups.

🔹 download_worker
✅ Worker thread to handle multiple file downloads in parallel.

Useful when downloading many files faster using multithreading.

🔹 matches_filters
✅ Apply filters to include/exclude files based on name, size, time, etc.

Helps in automating selective file processing.

🔹 download_all_files_from_smb
✅ Recursively download entire folder contents from SMB with filtering and threading.

Best for bulk downloads with rules (e.g., latest 10 logs).

🔹 check_session_directory
✅ Check if a path is a valid and accessible SMB directory.

Prevents errors by validating directory before use.

🔹 download_folder
✅ Downloads all files from a server folder to local directory.

Useful for backing up or syncing a directory.

🔹 filter_file
✅ Determine if a local file matches given criteria.

Handy in uploading only relevant or new files.

🔹 upload_file
✅ Uploads all files from a local path to an SMB folder using threads.

Great for bulk uploads with optional filtering.

🔹 upload_single_file
✅ Upload one specific file to an SMB path.

Ideal for manual or one-off uploads.

🔹 create_directory
✅ Create a single directory on the SMB share.

Use before upload to ensure target path exists.

🔹 remove_file
✅ Delete a specific file on the SMB server.

Good for clean-up scripts or removing outdated data.

🔹 remove_directory
✅ Remove a directory from SMB, if empty.

Helps in automating cleanup tasks.

🔹 rename_file_or_folder
✅ Rename or move files/folders on the SMB share.

Useful for reorganizing files or applying naming conventions.

🔹 path_exists
✅ Check whether a given path exists on SMB.

Avoids errors by pre-checking before operations.

🔹 make_directories
✅ Create nested directory structure on the SMB share.

Best when mirroring local folder structures remotely.

🔹 create_symlink
✅ Create a symbolic link pointing to another file.

Useful for aliasing or redirecting to latest files.

🔹 remove_symlink
✅ Delete an existing symbolic link on SMB.

Keeps directory structures clean and up to date.

🔹 set_xattr
✅ Set custom metadata attributes on a file.

Great for tagging files with version, owner, or flags.

🔹 get_xattr
✅ Retrieve a specific extended attribute from a file.

Allows reading custom file metadata.

🔹 list_xattr
✅ List all extended attributes for a given file.

Useful for inspecting metadata attached to files.

🔹 set_file_time
✅ Update a file's access and modification timestamps.

Critical for syncing timestamps during backups or audits.