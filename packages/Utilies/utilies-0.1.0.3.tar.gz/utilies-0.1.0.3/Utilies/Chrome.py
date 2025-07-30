"""
Author : Krishna Murthy S
"""

import json
import logging
import ntpath
import os
import sys
import warnings
import time, glob

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

warnings.filterwarnings("ignore")
argumentlist = sys.argv[1:]
print(argumentlist)

''' Change Working Directory and Set Standard Directories'''
logging.warning(os.path.realpath(__file__))
masterDir = os.path.split(os.path.realpath(__file__))[0]
for i in range(3):
    if ntpath.basename(masterDir) == "Scripts":
        masterDir = os.path.split(masterDir)[0]
        break
    else:
        masterDir = os.path.split(masterDir)[0]
logging.warning(masterDir)

''' Directory Declaring '''
inputDir = os.path.join(masterDir, "Input")
scriptsDir = os.path.join(masterDir, "Scripts")
outputDir = os.path.join(masterDir, "Output")
log_dir = os.path.join(masterDir, "Log_File")

'''Appending scriptsDir'''
sys.path.append(scriptsDir)

'''Chrome Operation'''


class Chrome:
    '''Initial data'''

    def __init__(self):

        self.chrome_options = webdriver.ChromeOptions()
        self.driver = None
        self.chromeOptions = webdriver.ChromeOptions()

    def change_download_folder(self, change_directory, driver=None):
        '''
        Args:
            change_directory: folder need to changed
            driver:  driver os the session

        Returns: driver


        '''
        if driver:
            self.driver = driver
        if not os.path.exists(change_directory):
            try:
                os.makedirs(change_directory, exist_ok=True)
            except Exception as e:
                print(f"Unable to create dictory : {change_directory} to save the Files")
        if os.path.exists(change_directory):
            print(f"Chrome Driver download path changing to : {change_directory}")
            self.driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow',  # Allow downloads
                'downloadPath': change_directory
                # Set the new download directory
            })
            print(f"Chrome Driver download path changed to : {change_directory}")
        else:
            print(f"specified path not exit: {change_directory}")

    '''Open Chrome'''

    def Open_Chrome(self, proxy_need=False, proxy_address=None, proxy_port=None, timezone_need=False,
                    timezone='Asia/Kolkata'):
        """
        :return: Driver session
        """

        print("Driver is Enabled")
        options = webdriver.ChromeOptions()
        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }

        '''change path in 'savefile.default_directory'''''
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            "download.default_directory": outputDir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--kiosk-printing')
        self.chrome_options.add_experimental_option('prefs', {
            'printing.print_preview_sticky_settings.appState': '{"recentDestinations":[{"id":"Save as PDF","origin":"local"}],"selectedDestinationId":"Save as PDF","version":2}',
            'savefile.default_directory': os.path.join(
                os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            ) + r"\Output",
            'printing.default_destination_selection_rules.single_printer': 'Save as PDF',

        })
        self.chrome_options.add_argument('--disable-dev-shm-usage')  # Needed for Linux
        self.chrome_options.add_argument('--headless')
        options.page_load_strategy = 'none'  # Optional: Run Chrome in headless mode
        self.chrome_options.add_argument("--user-data-dir=/path/to/your/chrome/profile")
        self.chrome_options.add_argument("--timezone=UTC")
        if proxy_need:
            self.chrome_options.add_argument(
                f"--proxy-server={proxy_address}:{proxy_port}"
            )
        # Set options to disable PDF viewer
        self.chrome_options.add_argument('--disable-features=ChromePDFViewer')
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        if timezone_need:
            self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': {'Date': timezone}})
            self.driver.execute_cdp_cmd(
                'Emulation.setTimezoneOverride',
                {
                    'timezoneId': timezone
                }
            )

        return self.driver

    '''Close Chrome'''

    def Close_Chrome(self):
        """
        :return: None
        """
        self.driver.close()

    '''click on the xpath '''

    def xpath_Click(self, xpath, driver=None):
        """
        :param xpath: xpath to click
        :param driver: driver session
        :return: Status -> false / true
        """
        if driver is None:
            driver = self.driver
        self.is_page_loaded(driver)
        for i in range(5, 10):
            try:
                element = WebDriverWait(driver, i).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                if element.is_displayed():
                    element.click()
                    return True
            except Exception as e:
                print(f"Retrying {xpath}: {i}")
                continue
        return False

    '''click on the xpath and send sendkeys'''

    def xpath_sendkeys(self, xpath, sendkeys, driver=None):
        """
        :param xpath: xpath of the element
        :param sendkeys:  value need to enter
        :param driver:driver session
        :return: Status -> false / true
        """
        if driver is None:
            driver = self.driver
        self.is_page_loaded(driver)
        for i in range(5, 10):
            try:
                element = WebDriverWait(driver, i).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                if element.is_displayed():
                    element.send_keys(sendkeys)
                    return True
            except Exception as e:
                print(f"Retrying {xpath}: {i}")

                continue
        return False

    def xpath_text(self, xpath,driver=None):
        """
        :param xpath: xpath to click
        :param driver: driver of session
        :return: Status -> text / null values
        """

        if driver is None:
            driver = self.driver
        self.is_page_loaded(driver)
        for i in range(5, 10):
            try:
                element = WebDriverWait(driver, i).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                if element.is_displayed():
                    return element.text

            except Exception as e:
                print(f"Retrying {xpath}: {i}")
                continue
        return ''
    def wait_untill_file_download(self, outputDir, sleep_time, pdf_title, skip_file_name="_ExpenseItemization"):
        # Wait until at least one PDF file is downloaded
        while any(file.endswith(".crdownload") for file in os.listdir(outputDir)):
            time.sleep(sleep_time)  # Wait for 1 second

        # Wait until the last downloaded PDF file has finished downloading
        while True:
            latest_pdf_file = max(glob.glob(os.path.join(outputDir, "*.pdf")), key=os.path.getmtime)
            if skip_file_name not in latest_pdf_file and os.path.getsize(latest_pdf_file) > 0:
                break
            time.sleep(sleep_time)  # Wait for 1 second
        file = [files for files in glob.glob(os.path.join(outputDir, "*.*")) if "ExpenseItemization" not in files]
        for filename in file:
            os.rename(filename, os.path.join(outputDir, pdf_title))

    def is_page_loaded(self, driver, max_wait_time=30):
        start_time = time.time()  # Record the start time

        while True:
            # Check if the document is completely loaded
            if driver.execute_script("return document.readyState") == "complete":
                print("Page is fully loaded.")
                break  # Exit the loop once the page is fully loaded

            # If the maximum wait time has passed, break out of the loop
            if time.time() - start_time > max_wait_time:
                print("Timeout: Page did not load within the maximum wait time.")
                break  # Exit the loop due to timeout

            print("Page is still loading...")
            time.sleep(1)  # Wait for 1 second before checking againait