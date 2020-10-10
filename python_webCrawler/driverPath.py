import pathlib
from selenium import webdriver

# Get absolute path
absolute_path = str(pathlib.Path(__file__).parent.absolute())
absolute_path = absolute_path.replace("\\", "/")

# Must be changed if you have some problems :
# https://www.selenium.dev/documentation/fr/getting_started_with_webdriver/third_party_drivers_and_plugins/
DRIVER_PATH_WINDOWS_CHROME = absolute_path + '/driver/chromedriver.exe'
DRIVER_PATH_WINDOWS_FIREFOX = absolute_path + '/driver/geckodriver.exe'

DRIVER_PATH_LINUX_CHROME = absolute_path + '/driver/chromedriver-83.0.4103.39-linux'
DRIVER_PATH_LINUX_FIREFOX = absolute_path + '/driver/geckodriver-v0.26-linux'


def get_driver(user_os='', user_browser=''):
    # See more : https://www.selenium.dev/documentation/fr/webdriver/driver_requirements/

    while not user_os == "1" and not user_os == "2":
        print("Choose your OS:")
        print("  1. Windows")
        print("  2. Linux")

        user_os = input("> ")
        print("")

    while not user_browser == "1" and not user_browser == "2":
        print("Choose your browser:")
        print("  1. Chrome")
        print("  2. Firefox")

        user_browser = input("> ")
        print("")

    if user_os == "1":
        if user_browser == "1":
            return webdriver.Chrome(executable_path=DRIVER_PATH_WINDOWS_CHROME)

        elif user_browser == "2":
            return webdriver.Firefox(executable_path=DRIVER_PATH_WINDOWS_FIREFOX)

    elif user_os == "2":
        if user_browser == "1":
            return webdriver.Chrome(executable_path=DRIVER_PATH_LINUX_CHROME)

        elif user_browser == "2":
            return webdriver.Firefox(executable_path=DRIVER_PATH_LINUX_FIREFOX)
