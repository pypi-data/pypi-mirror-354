'''
Author : krishnamurthy S
mail: krishnamurthy.s@hpe.com
'''

import json
import os
import stat
from concurrent.futures import ThreadPoolExecutor, as_completed

import paramiko
import time
from scp import SCPClient


class RemoteConnection():
    def __init__(self, ipaddress, username, password, port):
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None
        self.cursor_path = None
        self.port = port

    def connect_server(self):
        self.ssh.connect(self.ipaddress, username=self.username, password=self.password, port=self.port)
        self.ssh.get_transport().set_keepalive(60)  # Send a keep-alive message every 60 seconds
        self.sftp = self.ssh.open_sftp()

    ################### File Operation ################
    def create_directory(self, path):
        stdin, stdout, stderr = self.ssh.exec_command(f'if not exist "{path}" mkdir "{path}"')
        if stderr.read():
            raise Exception(f"Failed to create directory {path}")

    def download_multiple_folders(self, root_path, local_base_path, max_workers=4):
        directory_list = self.list_directory(root_path)
        tasks = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for sub_folder in directory_list:
                remote_file_path = fr"{root_path}/{sub_folder}"
                local_file_path = f"{local_base_path}/{sub_folder}"

                # Submit a task to the executor
                task = executor.submit(self.download_file_with_retry, remote_file_path, local_file_path)
                tasks.append(task)

            # Wait for all tasks to complete
            for task in as_completed(tasks):
                success = task.result()  # This will raise an exception if the download failed after retries
                if not success:
                    print(f"Failed to download a folder. Retry limit exceeded.")
                else:
                    print(f"Folder download succeeded.")

    def download_file_with_retry(self, remote_file_path, local_file_path, retries=3, delay=5):
        """
        Download the folder with retry logic, including renaming special folders.
        """
        attempt = 0

        # Now perform the download
        while attempt < retries:
            try:
                with SCPClient(self.ssh.get_transport(), socket_timeout=120) as scp:
                    print(f"Attempting to download {remote_file_path} to {local_file_path}, attempt {attempt + 1}...")
                    scp.get(remote_file_path, local_file_path, recursive=True)
                    print(f"Successfully downloaded {remote_file_path} to {local_file_path}")
                    break  # If successful, break out of the retry loop
                return True
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(delay)  # Wait before retrying
                attempt += 1
        else:
            print(f"All {retries} attempts failed. Returning False.")
            return False

        return True

    def list_directory(self, remote_file_path):
        if self.sftp is None:
            self.sftp = self.ssh.open_sftp()
        directory_list = self.sftp.listdir(remote_file_path)
        return directory_list

    def remove_file(self, remote_file_path):
        remote_file_path = self.adjust_remote_path(remote_file_path)
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            self.sftp.remove(remote_file_path)
            print(f"File '{remote_file_path}' removed successfully.")
        except Exception as e:
            print(f"Error removing file '{remote_file_path}': {e}")

    def remove_directory(self, remote_directory_path):
        remote_file_path = self.adjust_remote_path(remote_directory_path)
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            self.sftp.rmdir(remote_file_path)
            print(f"File '{remote_file_path}' removed successfully.")
        except Exception as e:
            print(f"Error removing file '{remote_file_path}': {e}")

    def details_folder_file(self, path):
        remote_file_path = self.adjust_remote_path(path)
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            return self.sftp.stat(remote_file_path)

        except Exception as e:
            print(f"unable to find '{remote_file_path}': {e}")

    def current_path_details(self):
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            return self.sftp.getcwd()

        except Exception as e:
            print(f"unable to find current path: {e}")

    def rename_file(self, remote_old_path, remote_new_path):
        remote_old_path = self.adjust_remote_path(remote_old_path)
        remote_new_path = self.adjust_remote_path(remote_new_path)
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            self.sftp.rename(remote_old_path, remote_new_path)
            print(f"File '{remote_old_path}' renamed to '{remote_new_path}' successfully.")
        except Exception as e:
            print(f"Error renaming file '{remote_old_path}' to '{remote_new_path}': {e}")
        return remote_new_path

    def rename_folder_file(self, remote_old_path, remote_new_path):
        remote_old_path = self.adjust_remote_path(remote_old_path)
        remote_new_path = self.adjust_remote_path(remote_new_path)
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            self.sftp.posix_rename(remote_old_path, remote_new_path)
            print(f"File '{remote_old_path}' renamed to '{remote_new_path}' successfully.")
        except Exception as e:
            print(f"Error renaming file '{remote_old_path}' to '{remote_new_path}': {e}")

    def check_directory(self, directory):
        try:
            if self.sftp is None:
                self.sftp = self.ssh.open_sftp()
            self.sftp.chdir(directory)
            return True
        except FileNotFoundError:
            return False

    def close_connection(self):
        if self.sftp:
            self.sftp.close()
        self.ssh.close()

    def set_cursor_path(self, cursor_path):
        self.cursor_path = cursor_path

    def adjust_remote_path(self, remote_file_path):
        if self.cursor_path and remote_file_path.startswith('/'):
            remote_file_path = self.cursor_path + remote_file_path
        return remote_file_path

    def put_file(self, local_file_path, remote_file_path):
        remote_file_path = self.adjust_remote_path(remote_file_path)
        self.sftp.put(local_file_path, remote_file_path)

    ################# Run any file  ############################
    def run_bat_file(self, bat_file, arguments=None):
        full_command = f"{bat_file} {arguments}" if arguments else bat_file
        stdin, stdout, stderr = self.ssh.exec_command(full_command)
        if stderr.read():
            print(f"Error running batch file '{bat_file}'")
        else:
            print(f"Batch file '{bat_file}' executed successfully.")

    ############## Connect to Dev / Production Server ########################

    def production_server(self, host, user_name, password):
        transport = self.ssh.get_transport()
        dest_addr = (host, 22)  # Destination SSH server address and port
        local_addr = (self.ipaddress, 0)  # Local address to bind (intermediate server)

        dest_ssh = transport.open_channel("direct-tcpip", dest_addr, local_addr)
        final_ssh = paramiko.SSHClient()
        final_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        final_ssh.connect(hostname=host, username=user_name, password=password, sock=dest_ssh)

    ######################### Execute Commands ################################
    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error executing command '{command}': {error}")
        else:
            print(f"Command '{command}' executed successfully.")
            if output:
                print(f"Output:\n{output}")

    ##########################access the Service################################
    def start_service(self, service_name):
        command = f'sc start {service_name}'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error starting service '{service_name}': {stderr.read()}")
        else:
            print(f"Service '{service_name}' started successfully.")

    def restart_service(self, service_name):
        command = f'sc stop {service_name} && sc start {service_name}'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error restarting service '{service_name}': {stderr.read()}")
        else:
            print(f"Service '{service_name}' restarted successfully.")

    def stop_service(self, service_name):
        command = f'sc stop {service_name}'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error stopping service '{service_name}': {stderr.read()}")
        else:
            print(f"Service '{service_name}' stopped successfully.")

    def kill_process(self, process_name):
        command = f'powershell Stop-Process -Name "{process_name}"'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error killing process '{process_name}': {stderr.read()}")
        else:
            print(f"Process '{process_name}' killed successfully.")

    def check_service_status(self, service_name):
        command = f'powershell Get-Service -Name "{service_name}"'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error checking service '{service_name}' status: {error}")
        else:
            print(f"Service '{service_name}' status:")
            print(output)

    ######################### 4.	System Monitoring	################################

    def check_cpu_usage(self):
        command = 'powershell -Command "Get-WmiObject -Class Win32_PerfFormattedData_PerfOS_Processor | Select-Object -ExpandProperty PercentProcessorTime"'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error:
            raise Exception(f"Error getting processor time: {error}")

        return output

        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error checking CPU usage: {error}")
        else:
            print(f"CPU Usage (%):\n{output}")

    def list_processes(self):
        # command = 'powershell Get-Process'
        command = '''powershell -Command "$processes = Get-Process | Select-Object Name, Id, CPU, MemoryUsage, Status | ConvertTo-Json -Compress; Write-Output $processes"'''

        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            raise Exception(f"Error listing processes: {error}")

        return json.loads(output)

    def check_memory_usage(self):
        command = '''
    
    $os = Get-WmiObject -Class Win32_OperatingSystem
    Write-Output 'Retrieved OS information'
    $totalMemory = $os.TotalVisibleMemorySize
    $freeMemory = $os.FreePhysicalMemory
    Write-Output 'Total Memory (KB): ' $totalMemory
    Write-Output 'Free Memory (KB): ' $freeMemory
    if ($totalMemory -and $freeMemory) {
        $usedMemory = $totalMemory - $freeMemory
        $totalMemoryGB = [math]::Round($totalMemory / 1MB, 2)
        $freeMemoryGB = [math]::Round($freeMemory / 1MB, 2)
        $usedMemoryGB = [math]::Round($usedMemory / 1MB, 2)
        Write-Output 'Total Physical Memory: ' $totalMemoryGB ' GB'
        Write-Output 'Free Physical Memory: ' $freeMemoryGB ' GB'
        Write-Output 'Used Physical Memory: ' $usedMemoryGB ' GB'
    } else {
        Write-Output 'Unable to retrieve memory information'
    }
    '''

        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error checking memory usage: {error}")
        else:
            print(f"Free Physical Memory (bytes):\n{output}")

    def check_disk_usage(self):
        command = 'powershell Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, FreeSpace, Size'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error checking disk usage: {error}")
        else:
            print(f"Disk Usage:\n{output}")

    def view_system_events(self):
        command = 'powershell Get-EventLog -LogName System -Newest 10'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error viewing system events: {error}")
        else:
            print(f"System Events:\n{output}")

    def upload_directory(self, local_directory, remote_directory):
        """
        Recursively upload a local directory to the remote server.
        """
        if self.sftp is None:
            self.sftp = self.ssh.open_sftp()

        def recursive_upload(local_path, remote_path):
            if not self.check_directory(remote_path):
                self.sftp.mkdir(remote_path)
            for file in os.listdir(local_path):
                local_file = os.path.join(local_path, file)
                remote_file = f"{remote_path}/{file}"
                if os.path.isdir(local_file):
                    recursive_upload(local_file, remote_file)
                else:
                    self.sftp.put(local_file, remote_file)

        recursive_upload(local_directory, remote_directory)
        print(f"Directory '{local_directory}' uploaded to '{remote_directory}' successfully.")

    def download_directory(self, remote_directory, local_directory):
        """
        Recursively download a remote directory to the local machine.
        """
        if self.sftp is None:
            self.sftp = self.ssh.open_sftp()

        os.makedirs(local_directory, exist_ok=True)
        for item in self.sftp.listdir_attr(remote_directory):
            remote_path = os.path.join(remote_directory, item.filename).replace('\\', '/')
            local_path = os.path.join(local_directory, item.filename)

            if stat.S_ISDIR(item.st_mode):
                self.download_directory(remote_path, local_path)
            else:
                self.sftp.get(remote_path, local_path)

        print(f"Directory '{remote_directory}' downloaded to '{local_directory}' successfully.")

    def list_directory_detailed(self, remote_path):
        """
        Return a detailed list of files/folders including size, permissions, and modified time.
        """
        if self.sftp is None:
            self.sftp = self.ssh.open_sftp()

        file_details = []
        for file_attr in self.sftp.listdir_attr(remote_path):
            file_details.append({
                "filename": file_attr.filename,
                "size": file_attr.st_size,
                "modified_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_attr.st_mtime)),
                "permissions": oct(file_attr.st_mode)
            })

        return file_details

    def read_remote_file(self, remote_file_path):
        """
        Read the contents of a remote file and return it as a string.
        """
        if self.sftp is None:
            self.sftp = self.ssh.open_sftp()
        with self.sftp.open(remote_file_path, 'r') as f:
            content = f.read()
        return content

    def write_remote_file(self, remote_file_path, content):
        """
        Write content to a remote file.
        """
        if self.sftp is None:
            self.sftp = self.ssh.open_sftp()
        with self.sftp.open(remote_file_path, 'w') as f:
            f.write(content)
        print(f"Successfully wrote to '{remote_file_path}'.")

    def connect(self):
        """
        Connects to the remote server using SSH and opens an SFTP session.
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.username, password=self.password, port=self.port)
        self.sftp = self.ssh.open_sftp()
        print(f"Connected to {self.host}.")

    def close(self):
        """
        Closes the SSH and SFTP connections.
        """
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        print(f"Disconnected from {self.host}.")

    def upload_file(self, local_file_path, remote_file_path):
        """
        Uploads a file from the local system to the remote server.

        Args:
            local_file_path (str): The path of the local file to upload.
            remote_file_path (str): The path where the file should be uploaded on the remote server.
        """
        self.sftp.put(local_file_path, remote_file_path)
        print(f"File '{local_file_path}' uploaded to '{remote_file_path}'.")

    def download_file(self, remote_file_path, local_file_path):
        """
        Downloads a file from the remote server to the local system.

        Args:
            remote_file_path (str): The path of the remote file to download.
            local_file_path (str): The path where the file should be saved locally.
        """
        self.sftp.get(remote_file_path, local_file_path)
        print(f"File '{remote_file_path}' downloaded to '{local_file_path}'.")

    def upload_directory(self, local_directory, remote_directory):
        """
        Uploads an entire directory (and its contents) from the local system to the remote server.

        Args:
            local_directory (str): The local directory to upload.
            remote_directory (str): The remote directory where the local directory should be uploaded.
        """

        def recursive_upload(local_path, remote_path):
            if not self.check_directory(remote_path):
                self.sftp.mkdir(remote_path)
            for file in os.listdir(local_path):
                local_file = os.path.join(local_path, file)
                remote_file = f"{remote_path}/{file}"
                if os.path.isdir(local_file):
                    recursive_upload(local_file, remote_file)
                else:
                    self.sftp.put(local_file, remote_file)

        recursive_upload(local_directory, remote_directory)
        print(f"Directory '{local_directory}' uploaded to '{remote_directory}'.")

    def download_directory(self, remote_directory, local_directory):
        """
        Downloads an entire directory (and its contents) from the remote server to the local system.

        Args:
            remote_directory (str): The remote directory to download.
            local_directory (str): The local directory where the remote directory should be downloaded.
        """
        os.makedirs(local_directory, exist_ok=True)
        for item in self.sftp.listdir_attr(remote_directory):
            remote_path = os.path.join(remote_directory, item.filename)
            local_path = os.path.join(local_directory, item.filename)

            if stat.S_ISDIR(item.st_mode):
                self.download_directory(remote_path, local_path)
            else:
                self.sftp.get(remote_path, local_path)

        print(f"Directory '{remote_directory}' downloaded to '{local_directory}'.")

    def list_directory_detailed(self, remote_path):
        """
        Lists the detailed information (filename, size, permissions, modified time) of the remote directory.

        Args:
            remote_path (str): The path of the remote directory.

        Returns:
            list: A list of dictionaries containing detailed information of files in the directory.
        """
        file_details = []
        for file_attr in self.sftp.listdir_attr(remote_path):
            file_details.append({
                "filename": file_attr.filename,
                "size": file_attr.st_size,
                "modified_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_attr.st_mtime)),
                "permissions": oct(file_attr.st_mode)
            })
        return file_details

    def remove_file(self, remote_file_path):
        """
        Removes a file from the remote server.

        Args:
            remote_file_path (str): The path of the file to remove.
        """
        self.sftp.remove(remote_file_path)
        print(f"File '{remote_file_path}' removed.")

    def create_directory(self, remote_path):
        """
        Creates a directory on the remote server.

        Args:
            remote_path (str): The path of the directory to create.
        """
        self.ssh.exec_command(f'mkdir -p "{remote_path}"')
        print(f"Directory '{remote_path}' created.")

    def rename_file(self, remote_old_path, remote_new_path):
        """
        Renames a file on the remote server.

        Args:
            remote_old_path (str): The current path of the file.
            remote_new_path (str): The new path of the file.
        """
        self.sftp.rename(remote_old_path, remote_new_path)
        print(f"File '{remote_old_path}' renamed to '{remote_new_path}'.")

    def rename_folder(self, remote_old_path, remote_new_path):
        """
        Renames a folder on the remote server.

        Args:
            remote_old_path (str): The current path of the folder.
            remote_new_path (str): The new path of the folder.
        """
        self.sftp.posix_rename(remote_old_path, remote_new_path)
        print(f"Folder '{remote_old_path}' renamed to '{remote_new_path}'.")

    def execute_command(self, command):
        """
        Executes a command on the remote server.

        Args:
            command (str): The command to execute on the remote server.
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error:
            print(f"Error executing command '{command}': {error}")
        else:
            print(f"Command '{command}' executed successfully.")
            print(f"Output:\n{output}")

    def run_bat_file(self, bat_file, arguments=None):
        """
        Runs a batch file on the remote server.

        Args:
            bat_file (str): The path to the batch file on the remote server.
            arguments (str, optional): Arguments to pass to the batch file.
        """
        full_command = f"{bat_file} {arguments}" if arguments else bat_file
        stdin, stdout, stderr = self.ssh.exec_command(full_command)
        if stderr.read():
            print(f"Error running batch file '{bat_file}'")
        else:
            print(f"Batch file '{bat_file}' executed successfully.")

    def run_python_script(self, script_path, arguments=None):
        """
        Runs a Python script on the remote server.

        Args:
            script_path (str): The path to the Python script on the remote server.
            arguments (str, optional): Arguments to pass to the Python script.
        """
        full_command = f"python {script_path} {arguments}" if arguments else f"python {script_path}"
        stdin, stdout, stderr = self.ssh.exec_command(full_command)
        if stderr.read():
            print(f"Error running Python script '{script_path}'")
        else:
            print(f"Python script '{script_path}' executed successfully.")

    def run_shell_script(self, script_path, arguments=None):
        """
        Runs a shell script on the remote server.

        Args:
            script_path (str): The path to the shell script on the remote server.
            arguments (str, optional): Arguments to pass to the shell script.
        """
        full_command = f"bash {script_path} {arguments}" if arguments else f"bash {script_path}"
        stdin, stdout, stderr = self.ssh.exec_command(full_command)
        if stderr.read():
            print(f"Error running shell script '{script_path}'")
        else:
            print(f"Shell script '{script_path}' executed successfully.")

    def check_cpu_usage(self):
        """
        Checks the CPU usage on the remote server.

        Returns:
            str: The CPU usage percentage.
        """
        command = 'powershell -Command "Get-WmiObject -Class Win32_PerfFormattedData_PerfOS_Processor | Select-Object -ExpandProperty PercentProcessorTime"'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        return output

    def check_memory_usage(self):
        """
        Checks the memory usage on the remote server.

        Returns:
            str: The total and free memory in kilobytes.
        """
        command = '''
           $os = Get-WmiObject -Class Win32_OperatingSystem
           $totalMemory = $os.TotalVisibleMemorySize
           $freeMemory = $os.FreePhysicalMemory
           Write-Output 'Total Memory (KB): ' $totalMemory
           Write-Output 'Free Memory (KB): ' $freeMemory
           '''
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def check_disk_usage(self):
        """
        Checks the disk usage on the remote server.

        Returns:
            str: The disk usage information.
        """
        command = 'powershell Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, FreeSpace, Size'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def list_processes(self):
        """
        Lists the running processes on the remote server.

        Returns:
            str: The list of running processes.
        """
        command = 'powershell Get-Process'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def get_system_uptime(self):
        """
        Gets the system uptime on the remote server.

        Returns:
            str: The system uptime.
        """
        command = 'powershell (Get-WmiObject -Class Win32_OperatingSystem).LastBootUpTime'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def start_service(self, service_name):
        """
        Starts a service on the remote server.

        Args:
            service_name (str): The name of the service to start.
        """
        command = f'sc start {service_name}'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error starting service '{service_name}': {stderr.read()}")
        else:
            print(f"Service '{service_name}' started.")

    def stop_service(self, service_name):
        """
        Stops a service on the remote server.

        Args:
            service_name (str): The name of the service to stop.
        """
        command = f'sc stop {service_name}'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error stopping service '{service_name}': {stderr.read()}")
        else:
            print(f"Service '{service_name}' stopped.")

    def restart_service(self, service_name):
        """
        Restarts a service on the remote server.

        Args:
            service_name (str): The name of the service to restart.
        """
        command = f'sc stop {service_name} && sc start {service_name}'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error restarting service '{service_name}': {stderr.read()}")
        else:
            print(f"Service '{service_name}' restarted.")

    def kill_process(self, process_name):
        """
        Kills a process on the remote server.

        Args:
            process_name (str): The name of the process to kill.
        """
        command = f'powershell Stop-Process -Name "{process_name}"'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error killing process '{process_name}': {stderr.read()}")
        else:
            print(f"Process '{process_name}' killed.")

    def check_service_status(self, service_name):
        """
        Checks the status of a service on the remote server.

        Args:
            service_name (str): The name of the service to check.
        """
        command = f'powershell Get-Service -Name "{service_name}"'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        if stderr.read():
            print(f"Error checking service '{service_name}' status: {stderr.read()}")
        else:
            print(f"Service '{service_name}' status:\n{output}")

    def read_remote_file(self, remote_file_path):
        """
        Reads a remote file from the server.

        Args:
            remote_file_path (str): The path of the file to read.

        Returns:
            str: The content of the remote file.
        """
        with self.sftp.open(remote_file_path, 'r') as f:
            content = f.read()
        return content

    def write_remote_file(self, remote_file_path, content):
        """
        Writes content to a remote file on the server.

        Args:
            remote_file_path (str): The path of the file to write.
            content (str): The content to write to the file.
        """
        with self.sftp.open(remote_file_path, 'w') as f:
            f.write(content)
        print(f"Content written to '{remote_file_path}'.")

    def append_to_remote_file(self, remote_file_path, content):
        """
        Appends content to a remote file on the server.

        Args:
            remote_file_path (str): The path of the file to append to.
            content (str): The content to append to the file.
        """
        with self.sftp.open(remote_file_path, 'a') as f:
            f.write(content)
        print(f"Content appended to '{remote_file_path}'.")

    def file_exists(self, remote_file_path):
        """
        Checks if a file exists on the remote server.

        Args:
            remote_file_path (str): The path of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            self.sftp.stat(remote_file_path)
            return True
        except FileNotFoundError:
            return False

    def get_file_size(self, remote_file_path):
        """
        Gets the size of a remote file.

        Args:
            remote_file_path (str): The path of the file.

        Returns:
            int: The size of the file in bytes.
        """
        file_info = self.sftp.stat(remote_file_path)
        return file_info.st_size

    def change_file_permissions(self, remote_file_path, permissions):
        """
        Changes the permissions of a remote file.

        Args:
            remote_file_path (str): The path of the file.
            permissions (int): The new permissions in octal format.
        """
        self.sftp.chmod(remote_file_path, permissions)
        print(f"Permissions for '{remote_file_path}' changed to {oct(permissions)}.")

    def move_directory(self, remote_old_path, remote_new_path):
        """
        Moves or renames a directory on the remote server.

        Args:
            remote_old_path (str): The current path of the directory.
            remote_new_path (str): The new path of the directory.
        """
        self.sftp.rename(remote_old_path, remote_new_path)
        print(f"Directory '{remote_old_path}' moved to '{remote_new_path}'.")

    ######### Admin Functions

    def create_user(self, username, password):
        """
        Creates a new user on the remote server.

        Args:
            username (str): The username of the new user.
            password (str): The password for the new user.
        """
        command = f"sudo useradd -m {username} && echo '{username}:{password}' | sudo chpasswd"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error creating user '{username}': {stderr.read()}")
        else:
            print(f"User '{username}' created successfully.")

    def delete_user(self, username):
        """
        Deletes an existing user on the remote server.

        Args:
            username (str): The username of the user to delete.
        """
        command = f"sudo userdel -r {username}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error deleting user '{username}': {stderr.read()}")
        else:
            print(f"User '{username}' deleted successfully.")

    def add_user_to_group(self, username, group_name):
        """
        Adds a user to a group on the remote server.

        Args:
            username (str): The username to add to the group.
            group_name (str): The name of the group.
        """
        command = f"sudo usermod -aG {group_name} {username}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error adding user '{username}' to group '{group_name}': {stderr.read()}")
        else:
            print(f"User '{username}' added to group '{group_name}'.")

    def remove_user_from_group(self, username, group_name):
        """
        Removes a user from a group on the remote server.

        Args:
            username (str): The username to remove from the group.
            group_name (str): The name of the group.
        """
        command = f"sudo gpasswd -d {username} {group_name}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error removing user '{username}' from group '{group_name}': {stderr.read()}")
        else:
            print(f"User '{username}' removed from group '{group_name}'.")

    def get_user_info(self, username):
        """
        Retrieves information about a user on the remote server.

        Args:
            username (str): The username whose information is required.

        Returns:
            str: The user information (e.g., UID, GID, home directory).
        """
        command = f"getent passwd {username}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        if stderr.read():
            print(f"Error retrieving info for user '{username}': {stderr.read()}")
        else:
            return output.strip()

    def list_all_users(self):
        """
        Lists all the users on the remote server.

        Returns:
            list: A list of usernames on the server.
        """
        command = "cut -d: -f1 /etc/passwd"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        return output.splitlines()

    def set_environment_variable(self, var_name, var_value):
        """
        Sets an environment variable on the remote server.

        Args:
            var_name (str): The name of the environment variable.
            var_value (str): The value of the environment variable.
        """
        command = f"export {var_name}={var_value}"
        self.ssh.exec_command(command)
        print(f"Environment variable '{var_name}' set to '{var_value}'.")

    def get_environment_variable(self, var_name):
        """
        Retrieves the value of an environment variable on the remote server.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable.
        """
        command = f"echo ${var_name}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8').strip()

    def list_cron_jobs(self, username=None):
        """
        Lists cron jobs for a user or for all users.

        Args:
            username (str, optional): The username to list cron jobs for. If None, lists all users' cron jobs.

        Returns:
            str: The cron jobs of the user or all users.
        """
        if username:
            command = f"crontab -u {username} -l"
        else:
            command = "crontab -l"

        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        if stderr.read():
            print(f"Error listing cron jobs for '{username}': {stderr.read()}")
        else:
            return output.strip()

    def add_cron_job(self, cron_schedule, command, username=None):
        """
        Adds a cron job for a user.

        Args:
            cron_schedule (str): The schedule for the cron job (e.g., '0 0 * * *').
            command (str): The command to run.
            username (str, optional): The username to add the cron job for. If None, it adds for the current user.
        """
        cron_job = f"{cron_schedule} {command}"
        if username:
            command = f"echo '{cron_job}' | sudo crontab -u {username} -"
        else:
            command = f"echo '{cron_job}' | crontab -"
        self.ssh.exec_command(command)
        print(f"Cron job '{cron_job}' added.")

    def remove_cron_job(self, cron_schedule, command, username=None):
        """
        Removes a cron job for a user.

        Args:
            cron_schedule (str): The schedule for the cron job.
            command (str): The command to remove.
            username (str, optional): The username to remove the cron job from. If None, removes from the current user.
        """
        cron_job = f"{cron_schedule} {command}"
        if username:
            command = f"crontab -u {username} -l | grep -v '{cron_job}' | crontab -u {username} -"
        else:
            command = f"crontab -l | grep -v '{cron_job}' | crontab -"
        self.ssh.exec_command(command)
        print(f"Cron job '{cron_job}' removed.")

    def get_system_logs(self, log_type='syslog'):
        """
        Retrieves system logs from the remote server.

        Args:
            log_type (str): The type of log to fetch (e.g., 'syslog', 'auth.log').

        Returns:
            str: The contents of the log file.
        """
        log_files = {
            'syslog': '/var/log/syslog',
            'auth': '/var/log/auth.log',
            'kern': '/var/log/kern.log',
            'dmesg': '/var/log/dmesg',
        }
        log_file_path = log_files.get(log_type.lower(), '/var/log/syslog')
        command = f"cat {log_file_path}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def clear_system_logs(self, log_type='syslog'):
        """
        Clears system logs on the remote server.

        Args:
            log_type (str): The type of log to clear (e.g., 'syslog', 'auth.log').
        """
        log_files = {
            'syslog': '/var/log/syslog',
            'auth': '/var/log/auth.log',
            'kern': '/var/log/kern.log',
            'dmesg': '/var/log/dmesg',
        }
        log_file_path = log_files.get(log_type.lower(), '/var/log/syslog')
        command = f"sudo truncate -s 0 {log_file_path}"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stderr.read():
            print(f"Error clearing log '{log_type}': {stderr.read()}")
        else:
            print(f"Log '{log_type}' cleared.")

    def get_network_info(self):
        """
        Retrieves network information such as IP address and interfaces.

        Returns:
            str: The network information of the server.
        """
        command = "ifconfig"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def check_server_load(self):
        """
        Checks the system load average on the remote server.

        Returns:
            str: The system load average.
        """
        command = "uptime"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def check_server_temperature(self):
        """
        Checks the temperature of the remote server (if supported).

        Returns:
            str: The server temperature (if available).
        """
        command = "sensors"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def check_system_version(self):
        """
        Retrieves the version of the operating system on the remote server.

        Returns:
            str: The system version information.
        """
        command = "lsb_release -a"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')

    def get_uptime(self):
        """
        Retrieves the uptime of the server.

        Returns:
            str: The uptime of the system.
        """
        command = "uptime -p"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode('utf-8')
