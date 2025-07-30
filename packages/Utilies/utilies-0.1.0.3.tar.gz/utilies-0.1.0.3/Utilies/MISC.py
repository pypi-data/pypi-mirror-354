import calendar
import datetime
import glob
import json
import logging
import math
import os
import pickle
import random
import re
import shutil
import smtplib
import string
import subprocess
import sys
import threading
import time
import traceback
import zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
import pandas as pd
import requests
import win32com.client
from win32com import client
from xlsxwriter.utility import xl_col_to_name, xl_cell_to_rowcol, xl_rowcol_to_cell

# Set current directory path
Path = os.curdir
sys.path.append(Path)

# Threading lock for synchronization
lock = threading.Lock()


class Utility:
    """
    A class that encapsulates a variety of utility methods for file processing, emailing,
    Excel manipulation, and data cleanup.
    """

    def str_to_float(self, df, cols):
        """
        Convert columns to float in a pandas DataFrame after cleaning the data.

        Args:
            df (pandas.DataFrame): DataFrame containing the data.
            cols (list): List of column names to be converted.

        Returns:
            pandas.DataFrame: Updated DataFrame with cleaned and converted columns.
        """
        for col in cols:
            try:
                df[col] = df[col].map(str).apply(lambda x: self.cleanAmount(x)).astype(float)
            except Exception as e:
                logging.error(f"Error converting column {col} to float: {str(e)}")
        return df

    def log_infos(self, message):
        """Logs the provided info message."""
        logging.info(message)

    def log_renames(self, fname1, fname2):
        """Logs the renaming or copying of files."""
        shutil.copy(fname1, fname2)

    def TimeOut(self, timeout):
        """Pauses execution for the specified timeout (in seconds)."""
        time.sleep(timeout)

    def get_config(self, configfile):
        """
        Reads and returns configuration data from the specified config file.

        Args:
            configfile (str): Path to the configuration file.

        Returns:
            configparser.ConfigParser: ConfigParser object with the parsed configuration.
        """
        import configparser
        config = configparser.ConfigParser()
        config.read(configfile)
        return config

    def GetFiscalYr(self, date):
        """
        Returns the fiscal year based on a given date.

        Args:
            date (datetime): The date to calculate the fiscal year.

        Returns:
            int: The fiscal year corresponding to the given date.
        """
        return date.year if date.month <= 10 else date.year + 1

    def GetFiscalMnth(self, month):
        """
        Returns the fiscal month number corresponding to a given month.

        Args:
            month (int): The month number (1 to 12).

        Returns:
            int: Fiscal month number (1 to 12).
        """
        fiscal_month_mapping = {
            11: 1, 12: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8,
            7: 9, 8: 10, 9: 11, 10: 12
        }
        return fiscal_month_mapping.get(month, "nothing")

    def GetFiscalQuarter(self, endDate):
        """
        Returns the fiscal quarter and corresponding months for a given end date.

        Args:
            endDate (datetime): The end date to calculate the fiscal quarter.

        Returns:
            tuple: (Quarter string, List of months in the quarter).
        """
        month = endDate.month
        if month in [11, 12, 1]:
            return "Q1", [11, 12, 1]
        elif month in [2, 3, 4]:
            return "Q2", [2, 3, 4]
        elif month in [5, 6, 7]:
            return "Q3", [5, 6, 7]
        else:
            return "Q4", [8, 9, 10]

    def MailTrigger(self, mfrom, mto, subj, msg, path=""):
        """
        Sends an email with the specified subject, message, and attachment.

        Args:
            mfrom (str): Sender's email address.
            mto (str): Receiver's email address (can be a semicolon-separated list).
            subj (str): Subject of the email.
            msg (str): Body of the email.
            path (str or list): Path(s) to attachment(s) (optional).
        """
        msg = MIMEMultipart()
        msg['From'] = mfrom
        msg['To'] = mto
        msg['Subject'] = subj

        # Attach files if specified
        if path:
            attachments = [path] if isinstance(path, str) else path
            for file in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file, 'rb') as f:
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
                msg.attach(part)

        msg.attach(MIMEText(msg, 'html'))
        server = smtplib.SMTP('smtp3.hpe.com')
        server.sendmail(mfrom, mto.split('; '), msg.as_string())
        server.quit()

    def cleanAmount(self, amt):
        """
        Cleans and converts amounts to a float.

        Args:
            amt (str): Amount as a string.

        Returns:
            float: Cleaned amount as float.
        """
        if isinstance(amt, (int, float)):
            return amt
        if str(amt) == "nan" or not amt:
            return 0
        return float(str(amt).replace(',', '').replace('-$', '-').replace('$', ''))

    def GetDataFromDirFiles(self, flpath, fltype, filterlist):
        """
        Reads data from all files in a directory with the specified file extension.

        Args:
            flpath (str): Directory path to search for files.
            fltype (str): File extension to search for (e.g., 'csv', 'xlsx').
            filterlist (list): List of columns to filter in the data.

        Returns:
            pandas.DataFrame: Consolidated DataFrame with data from all files.
        """
        df = pd.DataFrame()
        for filename in glob.glob(f'{flpath}/*.{fltype}'):
            df1 = pd.read_csv(filename, encoding='ISO-8859-1') if fltype == 'csv' else pd.read_excel(filename)
            df1 = df1[filterlist]
            df = pd.concat([df, df1], ignore_index=True)
        return df

    def convert_Excel_to_csv(self, filename):
        """
        Converts Excel files (.xls, .xlsx, .xlsb) to CSV format.

        Args:
            filename (str): Path to the Excel file to convert.

        Returns:
            str: Path to the converted CSV file.
        """
        output_filename = filename.rsplit('.', 1)[0] + '.csv'
        if not os.path.exists(output_filename):
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            doc = excel.Workbooks.Open(filename)
            doc.SaveAs(output_filename, FileFormat=6)  # CSV format
            doc.Close()
            excel.Quit()
        return output_filename

    def EmptyFolder(self, path, allow_root=False):
        """
        Deletes all files and subdirectories in a given folder, but keeps the folder itself.

        Args:
            path (str): Folder path to clear.
            allow_root (bool): If True, allows clearing the root folder even with short path lengths.
        """
        if len(path) > 10 or allow_root:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))

    def csv_consolidation(self, files, column_list):
        """
        Consolidates data from multiple CSV files into a single DataFrame.

        Args:
            files (list): List of CSV files to be read.
            column_list (list): Columns to be retained in the final DataFrame.

        Returns:
            pandas.DataFrame: Consolidated DataFrame containing data from all files.
        """
        df = pd.DataFrame()
        for filename in files:
            df_temp = pd.read_csv(filename, encoding="ISO-8859-1")
            df_temp = self.Sanity_Clean_df(df_temp)
            df_temp = self.remove_unnamed_columns(df_temp)
            df = pd.concat([df, df_temp], ignore_index=True)
        return df

    def Sanity_Clean_df(self, df):
        """
        Cleans the DataFrame by stripping unwanted whitespace from strings.

        Args:
            df (pandas.DataFrame): DataFrame to clean.

        Returns:
            pandas.DataFrame: Cleaned DataFrame.
        """
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df.columns = df.columns.map(lambda x: str(x).replace("\n", ' ').strip())
        return df

    def remove_unnamed_columns(self, df):
        """
        Removes columns from the DataFrame that have 'Unnamed' in their name.

        Args:
            df (pandas.DataFrame): DataFrame to clean.

        Returns:
            pandas.DataFrame: Cleaned DataFrame with 'Unnamed' columns removed.
        """
        return df.loc[:, ~df.columns.str.contains('^Unnamed')]

    def wait_untill_file_download(self, outputDir, sleep_time, skip_file_name="_ExpenseItemization"):
        """
        Waits until a file is fully downloaded in a specified directory.
`
        Args:
            outputDir (str): Directory to check for downloaded files.
            sleep_time (int): Time (in seconds) to wait before checking again.
            skip_file_name (str): Filename to skip if present in the directory.
        """
        while any(file.endswith(".crdownload") for file in os.listdir(outputDir)):
            time.sleep(sleep_time)

        while True:
            latest_pdf_file = max(glob.glob(os.path.join(outputDir, "*.pdf")), key=os.path.getmtime)
            if skip_file_name not in latest_pdf_file and os.path.getsize(latest_pdf_file) > 0:
                break
            time.sleep(sleep_time)

        file = [f for f in glob.glob(os.path.join(outputDir, "*.*")) if skip_file_name not in f]
        for filename in file:
            os.rename(filename, os.path.join(outputDir, "DownloadedFile.pdf"))

    def read_file(self, file_path, mode='r'):
        """Read content from a file."""
        try:
            with open(file_path, mode) as file:
                return file.read()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def write_to_file(self, file_path, data, mode='w'):
        """Write data to a file."""
        try:
            with open(file_path, mode) as file:
                file.write(data)
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False

    def create_directory(self, path):
        """Create a directory if it doesn't exist."""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Directory '{path}' created.")
                return True
            else:
                print(f"Directory '{path}' already exists.")
                return False
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False

    def get_file_extension(self, file_path):
        """Get the file extension."""
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    def is_valid_email(self, email):
        """Check if an email address is valid."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def generate_random_string(self, length=8):
        """Generate a random string of a given length."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def pretty_print_json(self, data):
        """Pretty print JSON data."""
        print(json.dumps(data, indent=4))

    def convert_to_json(self, data):
        """Convert data to JSON."""
        try:
            return json.dumps(data)
        except TypeError as e:
            print(f"Error converting to JSON: {e}")
            return None

    def get_current_timestamp(self):
        """Get the current timestamp in ISO format."""
        return datetime.datetime.now().isoformat()

    def execute_shell_command(self, command):
        """Execute a shell command and capture the output."""
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return None

    def wait_until_file_exists(self, file_path, timeout=60, sleep_interval=1):
        """Wait until the file exists or timeout is reached."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                return True
            time.sleep(sleep_interval)
        print(f"Timeout reached. File '{file_path}' not found.")
        return False

    def get_file_size(self, file_path):
        """Get the size of a file."""
        try:
            return os.path.getsize(file_path)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None

    def send_post_request(self, url, data):
        """Send an HTTP POST request."""
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending POST request: {e}")
            return None

    def get_current_datetime(self):
        """Get the current date and time."""
        return datetime.datetime.now()

    def convert_to_datetime(self, date_str, date_format='%Y-%m-%d %H:%M:%S'):
        """Convert a string to a datetime object."""
        try:
            return datetime.datetime.strptime(date_str, date_format)
        except ValueError as e:
            print(f"Error converting string to datetime: {e}")
            return None

    def is_file_empty(self, file_path):
        """Check if a file is empty."""
        try:
            return os.path.getsize(file_path) == 0
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None

    def append_to_file(self, file_path, data):
        """Append data to an existing file."""
        try:
            with open(file_path, 'a') as file:
                file.write(data)
            return True
        except Exception as e:
            print(f"Error appending to file: {e}")
            return False

    def read_lines_from_file(self, file_path):
        """Read lines from a file into a list."""
        try:
            with open(file_path, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading lines from file: {e}")
            return None

    def get_last_modified_time(self, file_path):
        """Get the last modified time of a file."""
        try:
            return os.path.getmtime(file_path)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None

    def is_directory_empty(self, directory_path):
        """Check if a directory is empty."""
        try:
            return len(os.listdir(directory_path)) == 0
        except FileNotFoundError:
            print(f"Directory '{directory_path}' not found.")
            return None

    def copy_file(self, source, destination):
        """Copy a file from source to destination."""
        try:
            if not os.path.exists(source):
                print(f"Source file '{source}' does not exist.")
                return False
            with open(source, 'rb') as src, open(destination, 'wb') as dest:
                dest.write(src.read())
            print(f"File copied from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False

    def move_file(self, source, destination):
        """Move a file from source to destination."""
        try:
            if not os.path.exists(source):
                print(f"Source file '{source}' does not exist.")
                return False
            os.rename(source, destination)
            print(f"File moved from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def remove_file(self, file_path):
        """Remove a file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' removed.")
                return True
            else:
                print(f"File '{file_path}' not found.")
                return False
        except Exception as e:
            print(f"Error removing file: {e}")
            return False

    def save_pickledata(self, data, filename):
        """
        Saves data to a pickle file.

        :param data: Data to be saved.
        :param filename: Path to the output pickle file.
        """
        with open(filename, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def str_to_float(self, df, cols):
        """
        Converts columns in a dataframe to float after cleaning the amount fields.

        :param df: Input dataframe.
        :param cols: List of columns to be converted to float.
        :return: Dataframe with converted columns.
        """
        for col in cols:
            try:
                df[col] = df[col].map(str)
                df[col] = df[col].apply(lambda x: self.cleanAmount(x))
                df[col] = df[col].astype(float)
            except Exception as e:
                self.log_exceptions(e)
        return df

    def col_to_str(self, df, cols):
        """
        Converts specified columns in a dataframe to string and removes any trailing '.0' from them.

        :param df: Input dataframe.
        :param cols: List of columns to be converted to string.
        :return: Dataframe with converted columns.
        """
        for col in cols:
            try:
                df[col] = df[col].astype(str)
                df[col] = df[col].str.replace('\.0', '')
            except Exception as e:
                self.log_exceptions(e)
        return df

    def get_skiprows(self, filename, column_to_find):
        """
        Returns the number of rows to skip in a file before the desired column is found.

        :param filename: Path to the file.
        :param column_to_find: Column to search for.
        :return: The number of rows to skip.
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

        df = pd.DataFrame(lines, columns=["colname"])
        skiprows = 0
        for index, row in df.iterrows():
            if column_to_find in row["colname"]:
                skiprows = index
                break
        return skiprows

    def logFiles(self, fname):
        """
        Configures logging to write to the specified file.

        :param fname: Path to the log file.
        """
        try:
            logging.basicConfig(filename=fname, filemode='w', level=logging.DEBUG,
                                format='%(asctime)s - %(levelname)s - %(message)s')
        except Exception as e:
            self.log_exceptions(e)

    def extract_function_names(self):
        """
        Extracts the function name where the exception occurred.

        :return: Function name as a string.
        """
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)
        return stk[0][3]

    def log_exceptions(self, e):
        """
        Logs exception details to the log file.

        :param e: Exception instance.
        """
        try:
            logging.error(
                "Function {function_name} raised {exception_class} ({exception_docstring}): {exception_message}".format(
                    function_name=self.extract_function_names(),
                    exception_class=e.__class__,
                    exception_docstring=e.__doc__,
                    exception_message=e))
        except Exception as inner_e:
            logging.error(f"Error in logging exception: {inner_e}")

    def log_infos(self, message):
        """
        Logs informational messages to the log file.

        :param message: Information message to log.
        """
        try:
            logging.info(message)
        except Exception as e:
            self.log_exceptions(e)

    def log_renames(self, fname1, fname2):
        """
        Renames (copies) a file from fname1 to fname2.

        :param fname1: Source file path.
        :param fname2: Destination file path.
        """
        try:
            shutil.copy(fname1, fname2)
        except Exception as e:
            self.log_exceptions(e)

    def TimeOut(self, time_out):
        """
        Pauses execution for the specified time.

        :param time_out: Time in seconds to sleep.
        """
        try:
            time.sleep(time_out)
        except Exception as e:
            self.log_exceptions(e)

    def GetFiscalYr(self, date):
        """
        Returns the fiscal year based on the current date.

        :param date: The current date.
        :return: Fiscal year.
        """
        try:
            if date.today().month <= 10:
                return date.today().year
            else:
                return date.today().year + 1
        except Exception as e:
            self.log_exceptions(e)

    def GetFiscalMnth(self, mnth):
        """
        Maps the month to its corresponding fiscal month.

        :param mnth: Month number (1-12).
        :return: Fiscal month number.
        """
        switcher = {
            11: 1, 12: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11, 10: 12
        }
        return switcher.get(mnth, "nothing")

    def GetFiscalMnthStr(self, mnth):
        """
        Returns fiscal month as a two-digit string.

        :param mnth: Month number (1-12).
        :return: Fiscal month as a string.
        """
        switcher = {
            11: '01', 12: '02', 1: '03', 2: '04', 3: '05', 4: '06', 5: '07', 6: '08', 7: '09',
            8: '10', 9: '11', 10: '12'
        }
        return switcher.get(mnth, "nothing")

    def GetFiscalMnth_Daily(self, mnth):
        """
        Returns the name of the fiscal month.

        :param mnth: Month number (1-12).
        :return: Fiscal month name.
        """
        switcher = {
            11: "November", 12: "December", 1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October"
        }
        return switcher.get(mnth, "nothing")

    def GetFiscalQuarter(self, endDate):
        """
        Determines the fiscal quarter based on the end date.

        :param endDate: Date to check.
        :return: Tuple (Quarter, List of months in that quarter).
        """
        try:
            if endDate.month in [11, 12, 1]:
                return "Q1", [11, 12, 1]
            elif endDate.month in [2, 3, 4]:
                return "Q2", [2, 3, 4]
            elif endDate.month in [5, 6, 7]:
                return "Q3", [5, 6, 7]
            else:
                return "Q4", [8, 9, 10]
        except Exception as e:
            self.log_exceptions(e)

    def MailTrigger(self, mfrom, mto, subj, msg, path, html_body=False):
        """
        Sends an email with optional attachment.

        :param mfrom: Sender's email address.
        :param mto: Recipient(s) email address.
        :param subj: Subject of the email.
        :param msg: Body message of the email.
        :param path: Path to the attachment (if any).
        :param html_body: Whether the body is HTML formatted.
        """
        try:
            email = mfrom
            send_to_email = ", ".join(mto.split("; "))
            subject = subj
            message = msg
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = send_to_email
            msg['Subject'] = subject

            if path:
                part = MIMEBase('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(path)))
                msg.attach(part)

            if html_body:
                msg.attach(MIMEText(message, 'html'))
            else:
                msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP('smtp3.hpe.com') as server:
                server.sendmail(email, mto.split('; '), msg.as_string())
            print("Mail Sent...")
        except Exception as e:
            self.log_exceptions(e)

    def cleanAmount(self, amt):
        """
        Cleans the amount string by removing commas and fixing negative signs.

        :param amt: Amount string to clean.
        :return: Cleaned amount string.
        """
        try:
            cleanAmount = amt.replace(',', '')
            cleanAmount = re.sub("([0-9.]+)-$", r"-\1", cleanAmount)
            return cleanAmount
        except Exception as e:
            self.log_exceptions(e)

    def CleanFolder(self, fPath):
        """
        Cleans (removes) all files in the specified folder.

        :param fPath: Folder path to clean.
        """
        try:
            files_to_remove = [os.path.join(fPath, f) for f in os.listdir(fPath)]
            for f in files_to_remove:
                os.remove(f)
        except Exception as e:
            self.log_exceptions(e)

    def GetFileNameFromDir(self, flpath):
        """
        Returns the file names from the specified directory.

        :param flpath: Folder path.
        :return: List of file names in the directory.
        """
        try:
            filenames = []
            for _, _, filenames in os.walk(flpath):
                break
            return filenames
        except Exception as e:
            self.log_exceptions(e)

    def convert_Excel_to_csv(self, filename):
        """
        Converts an Excel file to CSV format.

        :param filename: Path to the Excel file.
        :return: Path to the output CSV file.
        """
        try:
            if filename[-4:] == 'xlsb':
                output_filename = filename[:-4] + 'csv'
                if filename.endswith('csv'):
                    print(output_filename, 'File is already a CSV file')
                    return filename

                if not os.path.exists(output_filename):
                    excel = win32com.client.Dispatch("Excel.Application")
                    excel.DisplayAlerts = False
                    excel.Visible = False
                    doc = excel.Workbooks.Open(filename)
                    try:
                        doc.Worksheets("Sheet1").Move(Before=doc.Worksheets(1))
                    except:
                        pass
                    doc.SaveAs(Filename=output_filename, FileFormat=6)
                    doc.Close()
                    excel.Quit()
                    print(filename, ' Converted to ', output_filename)
                return output_filename

        except Exception as e:
            self.log_exceptions(e)

    # ... CONTINUES ...

    def convert_xlsm_to_xlsx(self, filename):
        try:
            if filename[-4:] == 'xlsb':
                output_filename = filename[:-4] + 'xlsx'
            elif filename[-3:] == 'xls':
                output_filename = filename[:-3] + 'xlsx'
            elif filename[-4:] == 'xlsm':
                output_filename = filename[:-4] + 'xlsx'
            if filename[-4:] == 'xlsx':
                output_filename = filename
                print(filename, 'File is a xlsx file')
            else:
                if os.path.exists(output_filename) == False:
                    excel = win32com.client.Dispatch("Excel.Application")

                    excel.DisplayAlerts = False
                    doc = excel.Workbooks.Open(filename)
                    doc.DoNotPromptForConvert = True
                    doc.CheckCompatibility = False
                    doc.SaveAs(output_filename, FileFormat=51, ConflictResolution=2)
                    excel.Quit()

                print(filename, ' Converted to ', output_filename)
                return output_filename


        except Exception:
            excp = "Exception  occurs due to absence of xlsm file in the folder- " + traceback.format_exc()
            print(excp)
            logging.info(
                excp + " it can be resolved by checking the path of the excel file in  main function where it is called")

    '''clean df'''

    def Sanity_Clean_df(self, df):
        try:
            df.columns = df.columns.str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            # df.columns = df.columns.map(lambda x:x.strip())
            df.columns = df.columns.map(lambda x: str(x).replace("\n", ' '))
            df.columns = df.columns.map(lambda x: re.sub("\s\s+", " ", str(x)))
            return df

        except Exception:
            excp = "Exception  occurs due to data frame is empty " + traceback.format_exc()
            print(excp)
            logging.info(excp + " it can be resolved by checking the path of the df and data is there or not ")

    def set_column_width(self, df, col, ws):
        length_list = [len(x) + 5 for x in df.columns]
        for i, width in enumerate(length_list):
            ws.set_column(i, i + col, width)

    def Keep_Numeric_Data(self, x):
        return float(re.sub("[^0-9-.]", "", str(x)))

    def Find_Numeric_Columns(self, df):
        ColumnList = [x for x in df.columns if any(re.findall(r'amt|cost|amount|Quantity|Qty', x, re.IGNORECASE))]
        return ColumnList

    def insert_object_excel(self, filename, sheet_name, cell_loc, file_location):

        # excel = win32com.client.Dispatch("Excel.Application")
        excel, client = self.launch_excel()
        try:
            excel.DisplayAlerts = False
        except:
            pass
        try:
            excel.Visible = True
        except:
            pass
        doc = excel.Workbooks.Open(filename)
        worksheet = doc.Sheets(sheet_name)
        dest_cell = worksheet.Range("C2")
        Embedded_object = worksheet.OLEObjects()
        print(Embedded_object)
        Embedded_object.Add(ClassType=None, Filename=file_location, Link=False, DisplayAsIcon=True, Left=dest_cell.Left,
                            Top=dest_cell.Top, Width=50, Height=50)

        '''Assign object to obj variable'''
        obj = Embedded_object.Item(1)

        '''Copy and paste object to specific cell'''
        worksheet.OLEObjects(1).Copy()
        worksheet.Paste(Destination=worksheet.Range(cell_loc))

        '''Delete original object, so only the copied one is left'''
        obj.Delete()

        try:
            doc.save
            doc.close
            excel.quit()
        except:
            doc.SaveAs(filename)
            doc.Close()
            excel.Quit()

    def insert_multi_object_excel(self, filename, sheet_name, cell_loc, file_location, label_name, label_loc):

        excel, client = self.launch_excel()
        ''' excel = win32com.client.Dispatch("Excel.Application")'''
        try:
            excel.DisplayAlerts = False
        except:
            pass
        try:
            excel.Visible = True
        except:
            pass
        doc = excel.Workbooks.Open(filename)
        worksheet = doc.Sheets(sheet_name)
        Embedded_object = worksheet.OLEObjects()
        try:
            for i in range(1, len(file_location) + 1):
                dest_cell = worksheet.Range(cell_loc[i - 1])  # '''change to your wanted location'''
                if label_loc != None:
                    row_number, col_number = self.return_range2num(label_loc[i - 1])
                    worksheet.Cells(row_number, col_number).Value = label_name[i - 1]
                Embedded_object.Add(ClassType=None, Filename=file_location[i - 1], Link=False, DisplayAsIcon=True,
                                    Left=dest_cell.Left, Top=dest_cell.Top, Width=50, Height=50,
                                    IconFileName=r"C:\Windows\system32\packager.dll", IconIndex=0, IconLabel="")
                '''Assign object to obj variable'''
                obj = Embedded_object.Item(i)

                ''' Copy and paste object to specific cell'''
                worksheet.OLEObjects(i).Copy()
                worksheet.Paste(Destination=worksheet.Range(cell_loc[i - 1]))

                '''Delete original object, so only the copied one is left'''
                obj.Delete()
        except:
            pass
        try:
            doc.save
            doc.close
            excel.quit()
        except:
            doc.SaveAs(filename)
            doc.Close()
            excel.Quit()

    def Create_Summary(self, df, ColumnList=None):
        """
        Create a summary row at the bottom of a DataFrame by summing numeric columns.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        ColumnList (list, optional): List of column names to summarize. Defaults to all numeric columns.

        Returns:
        pd.DataFrame: DataFrame with a summary row added.
        """
        summary_dict = {}
        if ColumnList is None:
            ColumnList = df.select_dtypes(include=[np.number]).columns.tolist()

        for col in df.columns:
            if col in ColumnList:
                try:
                    summary_dict[col] = df[col].sum()
                except:
                    try:
                        df[col] = df[col].apply(lambda x: self.cleanAmount(x) if str(x) != "nan" else x).astype(
                            float)
                        summary_dict[col] = df[col].sum()
                    except:
                        pass
            elif col == df.columns[0]:
                summary_dict[col] = "Total"
            else:
                summary_dict[col] = ""

        summary_row = pd.DataFrame(summary_dict, index=[len(df) + 1])
        return pd.concat([df, summary_row], ignore_index=True)

    def set_header(self, workbook, ws, df, start_row, percent_cols=None, totals=False, start_col=0,
                   formulae_cols=None):
        """
        Apply header formatting and column formats to Excel worksheet using xlsxwriter.

        Parameters:
        workbook: xlsxwriter Workbook object.
        ws: xlsxwriter Worksheet object.
        df (pd.DataFrame): DataFrame to write.
        start_row (int): Row index to start writing headers.
        percent_cols (list, optional): Columns with percentage formatting.
        totals (bool, optional): Whether to include totals row at the end.
        start_col (int, optional): Column index to start writing data.
        formulae_cols (list, optional): Columns that require formula formatting.
        """
        end_row = len(df) + start_row
        header_format = workbook.add_format(
            {'bold': True, 'fg_color': '#c5d9f1', 'border': 1, 'align': 'center'})
        total_format = workbook.add_format(
            {'bold': True, 'fg_color': '#f2cfbb', 'border': 1, 'num_format': '#,##0.00'})
        non_total_format = workbook.add_format(
            {'bold': True, 'fg_color': '#f2cfbb', 'border': 1, 'num_format': '@'})
        text_fmt = workbook.add_format({'num_format': '@', 'align': 'center'})
        decimal_fmt = workbook.add_format({'num_format': '#,##0.00'})
        percent_fmt = workbook.add_format({'num_format': '0.00%'})

        for col_num, col_name in enumerate(df.columns, start=start_col):
            ws.write(start_row, col_num, col_name, header_format)
            if totals:
                try:
                    ws.write(end_row, col_num, df.iloc[-1][col_name], total_format)
                except:
                    ws.write(end_row, col_num, "", non_total_format)

            column_width = max(df[col_name].astype(str).str.len().max(), len(col_name)) + 3
            dtype = str(df[col_name].dtype)

            if dtype in ['float64', 'int64']:
                ws.set_column(col_num, col_num, column_width, decimal_fmt)
            elif formulae_cols and col_name in formulae_cols:
                ws.set_column(col_num, col_num, column_width, decimal_fmt)
            else:
                ws.set_column(col_num, col_num, column_width, text_fmt)

            if percent_cols and col_name in percent_cols:
                ws.set_column(col_num, col_num, column_width, percent_fmt)

    def set_formats(self, workbook):
        """
        Create and return commonly used Excel cell formats.

        Parameters:
        workbook: xlsxwriter Workbook object.

        Returns:
        tuple: Format objects for various styles.
        """
        return (
            workbook,
            workbook.add_format({'bg_color': '#78B0DE'}),
            workbook.add_format({'bold': True, 'fg_color': '#c5d9f1', 'border': 1}),
            workbook.add_format({'num_format': '$#,##0'}),
            workbook.add_format({'num_format': '0.00%'}),
            workbook.add_format({'num_format': '@'}),
            workbook.add_format({'num_format': '#,##0.00'})
        )

    def colnum_string(self, n):
        """
        Convert column index to Excel-style letter (e.g. 1 -> A, 27 -> AA).

        Parameters:
        n (int): Column number.

        Returns:
        str: Excel-style column name.
        """
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string

    def create_ZipFile(self, zip_file, file_to_be_added):
        """
        Create a zip archive containing the specified file.

        Parameters:
        zip_file (str): Path of zip file to create.
        file_to_be_added (str): Path of file to include in zip.
        """
        with zipfile.ZipFile(zip_file, "w") as myzip:
            myzip.write(file_to_be_added)

    def create_zip_and_remove_original(self, output_file, file_format):
        """
        Create zip from file and delete original.

        Parameters:
        output_file (str): Path to original file.
        file_format (str): Extension of file to replace (e.g. '.xlsx').
        """
        zip_path = output_file.replace(file_format, ".zip")
        try:
            os.remove(zip_path)
        except FileNotFoundError:
            pass
        self.create_ZipFile(zip_path, output_file)
        os.remove(output_file)

    def Remove_Columns(self, df, ColumnNameList):
        """
        Remove specified columns from DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        ColumnNameList (list): List of column names to remove.

        Returns:
        pd.DataFrame: Modified DataFrame.
        """
        return df.drop(ColumnNameList, axis=1)

    def launch_excel(self):
        """
        Launch an instance of Excel using win32com.

        Returns:
        tuple: Excel COM object and win32com client module.
        """
        try:
            excel = client.gencache.EnsureDispatch('Excel.Application')
        except AttributeError:
            import re
            import shutil
            import sys

            for module in list(sys.modules):
                if re.match(r'win32com\.gen_py\..+', module):
                    del sys.modules[module]

            shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'), ignore_errors=True)
            excel = client.gencache.EnsureDispatch('Excel.Application')

        return excel, client

    def Create_Pivot_Table(self, filename, sheet_name, pivot_sheet, no_of_rows, no_of_cols,
                           row_field1=None, col_field1=None, page_field1=None, data_field1=None,
                           start_row=1, start_col=1, pivot_row=1, pivot_col=1, clean=True,
                           currentpagefilter=None, label_name=None):
        """
        Create pivot table in an Excel sheet using win32com.

        Parameters:
        filename (str): Full path to Excel file.
        sheet_name (str): Name of source worksheet.
        pivot_sheet (str): Name of pivot sheet to create or update.
        no_of_rows (int): Number of data rows.
        no_of_cols (int): Number of data columns.
        row_field1, col_field1, page_field1, data_field1 (list): Fields for pivot.
        start_row, start_col (int): Data range start in source sheet.
        pivot_row, pivot_col (int): Position to insert pivot table.
        clean (bool): Whether to delete existing pivot sheet.
        currentpagefilter (dict, optional): Filters for page fields.
        label_name (str, optional): Label to add above pivot table.
        """
        excel, client = self.launch_excel()
        excel.Interactive = False
        excel.DisplayAlerts = False
        excel.Visible = True

        wb = excel.Workbooks.Open(filename)
        ws = wb.Sheets(sheet_name)

        win32c = client.constants
        cl1 = ws.Cells(start_row, start_col)
        cl2 = ws.Cells(start_row + no_of_rows, start_col + no_of_cols - 1)
        pivot_source = ws.Range(cl1, cl2)

        try:
            sheet2 = wb.Sheets(pivot_sheet)
            if clean:
                sheet2.Delete()
                sheet2 = wb.Sheets.Add(After=ws)
                sheet2.Name = pivot_sheet
        except:
            sheet2 = wb.Sheets.Add(After=ws)
            sheet2.Name = pivot_sheet

        if label_name:
            sheet2.Cells(pivot_row, pivot_col).Value = label_name

        dest_cell = sheet2.Cells(pivot_row + 1, pivot_col)
        pivot_cache = wb.PivotCaches().Create(SourceType=1, SourceData=pivot_source, Version=5)
        pivot_table = pivot_cache.CreatePivotTable(TableDestination=dest_cell,
                                                   TableName=sheet_name + 'ReportPivotTable' + str(pivot_col),
                                                   DefaultVersion=5)

        for i, field in enumerate(row_field1 or [], 1):
            pivot_table.PivotFields(field).Orientation = win32c.xlRowField
            pivot_table.PivotFields(field).Position = i

        for i, field in enumerate(col_field1 or [], 1):
            pivot_table.PivotFields(field).Orientation = win32c.xlColumnField
            pivot_table.PivotFields(field).Position = i

        for i, field in enumerate(page_field1 or [], 1):
            pivot_table.PivotFields(field).Orientation = win32c.xlPageField
            pivot_table.PivotFields(field).Position = i
            if currentpagefilter and field in currentpagefilter:
                pivot_table.PivotFields(field).CurrentPage = currentpagefilter[field]

        for field in data_field1 or []:
            data_field = pivot_table.AddDataField(pivot_table.PivotFields(field))
            data_field.NumberFormat = '#,##0.00'
            data_field.Function = win32c.xlSum

        try:
            wb.Save()
        finally:
            wb.Close(False)
            excel.Quit()

    def return_range2num(self, col):
        """
        Split Excel cell reference into row and column numbers.

        Parameters:
        col (str): Excel cell reference (e.g. "A10").

        Returns:
        tuple: (row_number, column_number)
        """
        import string
        num = 0
        row_num = ""
        for c in col:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
            else:
                row_num += str(c)
        return int(row_num), num

    def insert_formulaes(self, df, columnname, formulae, columns=None, Summary=None, no_of_rows=0):
        """
        Insert Excel-compatible formula strings into a specified column of the DataFrame.

        Parameters:
        df (pd.DataFrame): Source DataFrame.
        columnname (str): Name of the column to insert formulae.
        formulae (str): Base formula string to apply.
        columns (list): Columns used in the formula.
        Summary (bool): Whether to include summary row.
        no_of_rows (int): Offset row number for formula base.

        Returns:
        pd.DataFrame: Updated DataFrame with formulae.
        """
        df1 = df.copy()
        df = df.reset_index(drop=True)
        df['i'] = df.index + 2 + no_of_rows

        def return_alpha(df_, colname):
            return xl_col_to_name(df_.columns.get_loc(colname))

        def modify_formula(x, formula, df_):
            if columns:
                for n in range(len(columns)):
                    formula = formula.replace(columns[n], return_alpha(df_, columns[n]) + str(x))
            return formula

        if len(df) > 1:
            if Summary:
                df.loc[:, columnname] = df["i"].apply(lambda x: modify_formula(x, formulae, df))
            else:
                df.iloc[:-1, df.columns.get_loc(columnname)] = df["i"].apply(lambda x: modify_formula(x, formulae, df))
        else:
            df[columnname] = df["i"].apply(lambda x: modify_formula(x, formulae, df))

        del df["i"]

        if Summary:
            summary_dict = {}
            numeric_cols = df1.select_dtypes(include=[np.number]).columns.tolist()

            for col in df1.columns:
                if col in numeric_cols:
                    try:
                        summary_dict[col] = df1[col].sum()
                    except:
                        try:
                            df1[col] = df1[col].apply(lambda x: self.cleanAmount(x) if str(x) != "nan" else x).astype(
                                float)
                            summary_dict[col] = df1[col].sum()
                        except:
                            pass
                elif col == df1.columns[0]:
                    summary_dict[col] = "Total"
                else:
                    summary_dict[col] = ""

            df2 = pd.DataFrame(summary_dict, index=[len(df1) + 9])
            return pd.concat([df, df2], ignore_index=True)
        return df

    def return_No_of_days_in_month(self, yearname, monthname):
        """
        Return number of days in a given month.

        Parameters:
        yearname (int): Year.
        monthname (int): Month number.

        Returns:
        int: Number of days in the month.
        """
        return calendar.monthrange(yearname, monthname)[1]

    def write_Data_to_Excel(self, df, writer, workbook, sheetname, startrow=0, startcol=0,
                            percentcols=None, formulaecols=None, header=None, Summary=True):
        """
        Write a DataFrame to Excel with optional summary and formatting.

        Parameters:
        df (pd.DataFrame): Data to write.
        writer (ExcelWriter): Pandas ExcelWriter object.
        workbook: xlsxwriter workbook object.
        sheetname (str): Sheet name.
        startrow (int): Starting row in Excel.
        startcol (int): Starting column in Excel.
        percentcols (list): Columns to apply percentage format.
        formulaecols (list): Columns that contain formulas.
        header (str): Optional header title.
        Summary (bool): Whether to include summary row.
        """
        if Summary and len(df) > 0:
            df_Summary = self.Create_Summary(df)
            total_ = True
        else:
            df_Summary = df
            total_ = False

        try:
            df_Summary.to_excel(writer, sheet_name=sheetname, startrow=startrow, startcol=startcol, index=False)
        except NotImplementedError:
            df_Summary.to_excel(writer, sheet_name=sheetname, startrow=startrow, startcol=startcol, index=True)

        worksheet = workbook.get_worksheet_by_name(sheetname)

        if header:
            startrow += 1
            header_format = workbook.add_format({'bold': True, 'fg_color': '#ffff00', 'italic': True, 'font_size': 12})
            worksheet.write(xl_col_to_name(startcol) + str(startrow), header, header_format)

            for i in range(1, len(df.columns)):
                worksheet.write(xl_col_to_name(startcol + i) + str(startrow), "", header_format)

        if len(df) > 0:
            try:
                self.set_header(workbook, worksheet, df_Summary, startrow, percent_cols=percentcols,
                                totals=total_, start_col=startcol, formulae_cols=formulaecols)
            except:
                pass

        print("Summary Data written to", sheetname)

    def Create_Grouped_Table(self, df, Select_Columns, Group_Columns, rename_dict=None):
        """
        Create a grouped summary table using specified columns.

        Parameters:
        df (pd.DataFrame): Source DataFrame.
        Select_Columns (list): Columns to include in grouping.
        Group_Columns (list): Columns to group by.
        rename_dict (dict, optional): Column rename mapping.

        Returns:
        pd.DataFrame: Grouped and optionally renamed summary table.
        """
        df_Pivot = df[Select_Columns].groupby(by=Group_Columns).sum().reset_index()
        if rename_dict:
            df_Pivot = df_Pivot.rename(columns=rename_dict)
        return df_Pivot

    def Create_writer(self, output_Folder, output_filename, output_var, Output_file=None):
        """
        Create a Pandas ExcelWriter object.

        Parameters:
        output_Folder (str): Folder path to save Excel file.
        output_filename (str): Name of Excel file.
        output_var (str): Log label.
        Output_file (str, optional): Full path override.

        Returns:
        tuple: (ExcelWriter, workbook, output file path)
        """
        print(f"{output_var} : Creating Excel File for Output")
        if Output_file is None:
            Output_file = os.path.join(output_Folder, output_filename)

        os.makedirs(output_Folder, exist_ok=True)
        writer = pd.ExcelWriter(Output_file, engine="xlsxwriter")
        workbook = writer.book
        print(f"{output_var} : Processing Output")

        return writer, workbook, Output_file

    def insert_multiple_images_in_worksheet(self, wk, wsname, image_loc, image_list, header_loc=None, header_list=None):
        """
        Insert multiple images into a worksheet.

        Parameters:
        wk: Workbook object.
        wsname (str): Worksheet name.
        image_loc (list): List of cell locations for images.
        image_list (list): List of image file paths.
        header_loc (list, optional): List of cell locations for headers.
        header_list (list, optional): List of headers.
        """
        ws = wk.get_worksheet_by_name(wsname)
        if len(image_list) == len(image_loc):
            for i in range(len(image_list)):
                ws.insert_image(image_loc[i], image_list[i], {'x_scale': 0.75, 'y_scale': 0.75})
                if header_loc and header_list:
                    try:
                        header_format = wk.add_format({'bold': True, 'fg_color': '#ffff00', 'italic': True,
                                                       'font_size': 10, 'align': 'left'})
                        ws.write(header_loc[i], header_list[i], header_format)
                        row, col = self.return_cell_to_rowcol(header_loc[i])
                        for j in range(1, 7):
                            ws.write(row, col + j, "", header_format)
                    except:
                        pass

    def insert_New_Worksheets(self, Sheet_Names, writer, workbook):
        """
        Create empty worksheets in Excel.

        Parameters:
        Sheet_Names (list): List of sheet names to create.
        writer (ExcelWriter): Pandas writer.
        workbook: xlsxwriter workbook object.
        """
        for sheetname in Sheet_Names:
            self.write_Data_to_Excel(pd.DataFrame(), writer, workbook, sheetname, header=None, Summary=False)

    def split_alpha_numeric_string(self, x):
        return re.findall(r"[^\W\d_]+|\d+", x)

    def return_cell_to_rowcol(self, x):
        return xl_cell_to_rowcol(x)

    def return_alpha(self, x):
        return xl_col_to_name(x)

    def return_row_col_to_cell(self, rownum, colnum):
        return xl_rowcol_to_cell(rownum, colnum)

    def round_upto_2_digits(self, n, decimals=2):
        """
        Custom rounding method to 2 decimal digits with rounding up logic.
        """
        if n < 0:
            n = -n
            expoN = n * 10 ** decimals
            return math.floor(expoN) * -1 / 10 ** decimals if abs(expoN) - math.floor(expoN) < 0.5 else \
                math.ceil(expoN) * -1 / 10 ** decimals
        else:
            expoN = n * 10 ** decimals
            return math.floor(expoN) / 10 ** decimals if abs(expoN) - math.floor(expoN) < 0.5 else \
                math.ceil(expoN) / 10 ** decimals

    def remove_Rounding_Diff(self, df, base_colname, round_colname):
        """
        Adjust rounding differences to ensure totals match.
        """
        diff_amount = self.round_upto_2_digits(df[base_colname].sum()) - df[round_colname].sum()
        if diff_amount != 0:
            for i in range(1, len(df)):
                if abs(self.round_upto_2_digits(df.iloc[-i][base_colname])) > 0:
                    df.iloc[-i, df.columns.get_loc(round_colname)] = self.round_upto_2_digits(
                        df.iloc[-i][round_colname] + diff_amount)
                    break
        return df

    def insert_image_in_worksheet_openpyxl(self, writer, wsname, image_file, image_loc, mult_fac=0.5):
        """
        Insert an image using openpyxl into an Excel worksheet.
        """
        try:
            from openpyxl.drawing.image import Image
            img = Image(image_file)
            img.height = round(img.height * mult_fac, 0)
            img.width = round(img.width * mult_fac, 0)
            writer.sheets.get(wsname).add_image(img, image_loc)
        except:
            pass

    def create_converters(self, list1):
        return {x: str for x in list1}

    def convert_to_num(self, df, list1):
        for colname in list1:
            try:
                df[colname] = df[colname].astype("float")
            except:
                try:
                    df[colname] = df[colname].apply(lambda x: float(self.cleanAmount(x)) if str(x) != "nan" else x)
                except ValueError:
                    print(f"Value Error in converting column: {colname}")
        return df

    def clean_str_data(self, df, list1):
        for colname in list1:
            try:
                df[colname] = df[colname].map(str).replace("\.0", "", regex=True)
            except:
                pass
        return df

    def kill_excel_file(self, file_name):
        for _ in range(5):
            if os.path.exists(file_name):
                import win32com.client as win32
                excel = win32.DispatchEx("Excel.Application")
                excel.Visible = True
                try:
                    workbook = excel.Workbooks.Open(file_name)
                    time.sleep(5)
                    workbook.Close(SaveChanges=False)
                    excel.Quit()
                    os.system(f'taskkill /f /im excel.exe')
                    print(f"Closed Excel file: {file_name}")
                    break
                except Exception as e:
                    print(f"Failed to close Excel file: {file_name}", e)

    def delete_folder_contents(self, folder_path):
        """
        Delete all files and folders within a directory.

        Parameters:
        folder_path (str): Path to the folder.
        """
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            print(f"The contents of folder '{folder_path}' have been successfully deleted.")
        except OSError as e:
            print(f"Error: {folder_path} : {e.strerror}")
