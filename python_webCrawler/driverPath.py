import pathlib
from selenium import webdriver
import platform
import sys

def driver_path(driver_type):
    # Get absolute path
    absolute_path = str(pathlib.Path(__file__).parent.absolute())
    absolute_path = absolute_path.replace("\\", "/")

    # Must be changed if you have some problems :
    # https://www.selenium.dev/documentation/fr/getting_started_with_webdriver/third_party_drivers_and_plugins/
    if driver_type == 1:
        # Driver path for Chrome on Windows
        return absolute_path + '/driver/chromedriver.exe'
    elif driver_type == 2:
        # Driver path for Firefox on Windows
        return absolute_path + '/driver/geckodriver.exe'
    elif driver_type == 3:
        # Driver path for Chrome on Linux
        return absolute_path + '/driver/chromedriver-83.0.4103.39-linux'
    elif driver_type == 4:
        # Driver path for Firefox on Linux
        return absolute_path + '/driver/geckodriver-v0.26-linux'


def get_driver(user_browser=''):
    # See more : https://www.selenium.dev/documentation/fr/webdriver/driver_requirements/

    # https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
    user_os = platform.system()
    print("You are running on " + user_os + " " + platform.release())
    print("")

    while not user_browser == "1" and not user_browser == "2":
        print("Choose your browser:")
        print("  1. Chrome")
        print("  2. Firefox")

        user_browser = input("> ")
        print("")

    if user_os == "Windows":
        if user_browser == "1":
            return webdriver.Chrome(executable_path=driver_path(1))

        elif user_browser == "2":
            return webdriver.Firefox(executable_path=driver_path(2))

    elif user_os == "Linux":
        if user_browser == "1":
            return webdriver.Chrome(executable_path=driver_path(3))

        elif user_browser == "2":
            return webdriver.Firefox(executable_path=driver_path(4))

    else:
        print("Your platform is not currently supported.")
        sys.exit(1)
