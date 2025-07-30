'''
Author : krishnamurthy S
mail: krishnamurthy.s@hpe.com
'''

import time
from subprocess import PIPE, run

from pywinauto import Application, findwindows
from pywinauto import Desktop
from pywinauto import controls, uia_defines

from .Chrome import Chrome

ch = Chrome()


class SelectCertification:

    def __init__(self, okta_user=True, okta_bot=False, CertificationName="", pin='', driver=None,
                 bot_username='', bot_password='', enter_pin=True, max_time_pin=50, skip_time_pin=2):
        """
        :param okta_user: Boolean flag indicating whether this is an Okta user
        :param okta_bot: Boolean flag indicating whether this is an Okta bot
        :param CertificationName: Name of the certification (default is empty string)
        :param pin: PIN for authentication (default is an empty string)
        :param driver: Driver instance to be used (default is None)
        :param bot_username: Username for bot (default is empty string)
        :param bot_password: Password for bot (default is empty string)
        :param enter_pin: Boolean flag indicating whether PIN should be entered (default is True)
        """
        # Initializing instance variables
        self.okta_user = okta_user
        self.okta_bot = okta_bot
        self.CertificationName = CertificationName
        self.pin = pin
        self.driver = driver
        self.bot_username = bot_username
        self.bot_password = bot_password
        self.enter_pin = enter_pin
        self.max_time_out_Enter_Pin = max_time_pin
        self.skip_time_pin = skip_time_pin

        # If driver is provided, assign to `ch.driver` (assuming `ch` is a valid object in your code)
        if driver is not None:
            ch.driver = driver  # Ensure `ch` is defined somewhere in your code

        # You can add additional methods for functionality as needed

    def okta_login(self):
        """
        :return: nothing
        """
        try:
            # Printing for debugging purposes
            print("Username entry started")

            # Attempt to send the username to the input field identified by XPath
            element = ch.xpath_sendkeys(xpath='//input[@autocomplete="username"]', sendkeys='a@hpe.com')

            # If element is None or not found, raise an exception
            if not element:
                raise Exception("Unable to enter username")

            print("Username entered successfully")

            # Attempt to click the 'Sign in with Virtual Digitalbadge' button
            print("Attempting to click Virtual Digital badge sign-in button...")
            element = ch.xpath_Click(xpath="//a[contains(text(), 'Sign in with Virtual Digitalbadge')]")

            # If the element is None or not found, raise an exception
            if not element:
                raise Exception("Unable to click on Virtual Digital button")

            print("Virtual Digital badge sign-in button clicked successfully")

        except Exception as e:
            # If any error occurs during login process, log the error message
            print(f"An error occurred during Okta login: {str(e)}")
            # You can re-raise the exception or handle it based on your needs
            raise

    def okta_bot_login(self):
        """
        Log in to Okta using bot credentials.
        :return: None
        """
        try:
            # Printing for debugging purposes
            print("Bot name entry started")

            # Attempt to send the bot's username to the input field
            element = ch.xpath_sendkeys(xpath='//input[@autocomplete="username"]', sendkeys=self.bot_username)
            if not element:
                raise Exception("Failed to enter Bot name")
            print("Bot name entered successfully")

            # Attempt to click the 'Sign in with Password or Okta Verify' button
            print("Attempting to click 'Sign in with Password or Okta Verify' button...")
            element = ch.xpath_Click(xpath='//input[@value="Sign in with Password or Okta Verify"]')
            if not element:
                raise Exception("Failed to click on 'Sign in with Password or Okta Verify'")
            print("'Sign in with Password or Okta Verify' clicked successfully")

            # Attempt to send the bot's password to the password input field
            print("Attempting to enter password...")
            element = ch.xpath_sendkeys(xpath='//input[@type="password"]', sendkeys=self.bot_password)
            if not element:
                raise Exception("Failed to enter password")
            print("Password entered successfully")

            # Attempt to click the 'Verify' button
            print("Attempting to click 'Verify' button...")
            element = ch.xpath_Click(xpath='//input[@value="Verify"]')
            if not element:
                raise Exception("Failed to click on 'Verify details'")
            print("'Verify details' clicked successfully")

        except Exception as e:
            # Handle any errors during the login process
            print(f"An error occurred during bot login: {str(e)}")
            # You can choose to re-raise the exception or handle it differently
            raise

    def wait_for_window(self, title, timeout=20):
        """
        Waits for a window with the specified title to appear within the given timeout period.

        :param title: The title of the window to wait for.
        :param timeout: The maximum time (in seconds) to wait for the window. Default is 20 seconds.
        :return: The Application object connected to the window if found.
        :raises TimeoutError: If the window is not found within the given timeout.
        """
        # Record the start time
        start_time = time.time()

        # Continuously check for the window until the timeout is reached
        while time.time() - start_time < timeout:
            try:
                # Try to connect to the window using the provided title
                return Application(backend='uia').connect(title=title)
            except findwindows.ElementNotFoundError:
                # Wait briefly before trying again
                time.sleep(0.5)

        # Raise an error if the window is not found within the timeout
        raise TimeoutError(f"Window with title '{title}' not found within {timeout} seconds.")

    def get_windows_title(self):
        """
        Get the title of the first window that matches specific criteria ('Select a certificate' or 'Sign In').

        :return: The title of the first matching window or 'Select a certificate' if no match is found.
        """
        # Get the desktop object to interact with the windows
        desktop = Desktop(backend="uia")

        # Sort windows by position on screen (optional), prioritize visible windows with a top position
        sorted_windows = sorted(
            desktop.windows(), key=lambda w: w.rectangle().top if w.is_visible() else float('inf'), reverse=True
        )

        # Iterate through sorted windows and check for matching titles
        for window in sorted_windows:
            title = window.window_text()

            # Check if the title matches either 'Select a certificate' or 'Sign In'
            if 'Select a certificate' in title or 'Sign In' in title:
                return title  # Return the matched title

        # Return a default value if no matching window is found
        return 'Select a certificate'  # This can be customized to return None or other value if needed

    def select_certification(self, max_timeout=120, skip_time=1):
        """
        Selects a certification from the list of certificates based on the configured `CertificationName`.

        This method follows these steps:
        1. Logs in using Okta credentials (based on whether `okta_user` or `okta_bot` is set).
        2. Waits for a window with the title corresponding to the certificate selection.
        3. Searches for the list of certificates and attempts to match the specified `CertificationName`.
        4. Iterates through the certificate rows, selects the correct one, and performs the required action.
        5. Optionally enters a PIN if `enter_pin` is set to `True`.

        :param max_timeout: Maximum time (in seconds) to wait for the window and list elements. Default is 120 seconds.
        :param skip_time: Time (in seconds) to wait between retries when trying to find the list element. Default is 1 second.
        :return: `True` if the certificate is selected successfully, `False` otherwise.
        :raises TimeoutError: If the list element is not found within the specified timeout period.
        """
        if self.okta_user:
            self.okta_login()
        elif self.okta_bot:
            self.okta_bot_login()
        list_element = None
        title = self.get_windows_title()
        app = self.wait_for_window(title, max_timeout)
        start_time = time.time()
        while time.time() - start_time < max_timeout:
            try:
                dlg = app.window(title=title)
                app_window = app.top_window()
                app_window.set_focus()
                list_element = dlg.child_window(top_level_only=False, control_type="List", found_index=0)
                if list_element:
                    break  # Exit the loop if the list element is found
            except Exception as e:
                print(f"Error: {e}. Retrying...")
            time.sleep(skip_time)  # Wait for 1 second before retrying

        if not list_element:
            raise TimeoutError(f"List element not found within {max_timeout} seconds.")
        # Retry logic for obtaining list element information
        for i in range(5, 30):
            try:
                list_element_info = list_element.wrapper_object().element_info
                break
            except Exception as e:
                print(f"Attempt {i - 4}: Failed to get list element info. Error: {e}")
                time.sleep(i)
        cert_count = int((run(['powershell.exe',
                               '(Get-ChildItem -path Cert:\CurrentUser\My -Recurse | Where-Object { $_.Subject -like "*Hewlett Packard Enterprise*" }).Count'],
                              stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)).stdout)
        cert_row = controls.uia_controls.ListViewWrapper(list_element_info)
        for i in range(cert_count):
            try:
                selected_row = cert_row.get_selection()
                if len(selected_row) > 0:
                    custom = list_element.child_window(control_type="Custom", found_index=i)
                    if custom:
                        data_items = custom.children(control_type="DataItem")
                        if not data_items:
                            custom = list_element.child_window(control_type="Custom", found_index=i + 1)
                            data_items = custom.children(control_type="DataItem")
                        if data_items:
                            first_item = data_items[0]  # Access the first DataItem
                            if first_item.window_text().lower().strip() == self.CertificationName.strip().lower():
                                uia_defines.get_elem_interface(list_element_info.element,
                                                               "LegacyIAccessible").DoDefaultAction()
                                print(f"Success Fully Selected the Certification :{self.CertificationName}")
                                break
                            else:
                                list_element.type_keys('{DOWN}')
                    else:
                        list_element.type_keys('{DOWN}')
            except Exception as e:
                print(f"Error while processing certificate row {i}: {e}")
                list_element.type_keys('{DOWN}')  # Move down even if there was an error

        if self.enter_pin:
            self.Enter_pin()
        return True

    def Enter_pin(self):
        """
        Enters the specified PIN into the 'Windows Security' window and clicks the OK button.

        This method performs the following steps:
        1. Waits for the "Windows Security" window to appear.
        2. Tries to locate the PIN input field and enters the specified PIN.
        3. Clicks the OK button to submit the PIN.
        4. Retries the process until the specified timeout is reached.
        :return: `True` if the PIN is successfully entered and the OK button is clicked, `False` if the PIN field is not found.
        :raises TimeoutError: If the PIN is not entered and the OK button is not clicked within the specified timeout period.
        """

        print(self.pin)
        start_time = time.time()

        # Loop to try entering PIN within the specified time
        while time.time() - start_time < self.max_time_out_Enter_Pin:
            try:
                # Wait for the "Windows Security" window
                app = self.wait_for_window("Windows Security")
                app.top_window().set_focus()
                dlg = app.window()

                print("Entering PIN")

                # Try to find the PIN input field (password field)
                try:
                    edit_element = dlg.child_window(top_level_only=False, control_type="Edit", found_index=0,
                                                    auto_id="PasswordField_0")
                except:
                    edit_element = dlg.child_window(top_level_only=False, control_type="Edit", found_index=0,
                                                    auto_id="PasswordField_1")

                # If the PIN input field is found, type the PIN
                if edit_element:
                    edit_element.type_keys(self.pin)
                    print("Entering OK")

                    # Find and click the OK button
                    ok_button = dlg.child_window(top_level_only=False, control_type="Button", found_index=0, title="OK")
                    ok_button.click()
                    return True  # Successfully entered PIN and clicked OK button

                else:
                    return False  # If the PIN input field was not found
            except Exception as e:
                print(f"Error entering PIN and clicking OK: {e}. Retrying...")
                time.sleep(self.skip_time_pin)  # Wait before retrying

        # Raise an error if the PIN was not entered successfully within the time limit
        raise TimeoutError("Failed to enter PIN and click OK within the specified time.")
