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
        # Driver path for Chrome on Linux
        return absolute_path + '/driver/chromedriver-83.0.4103.39-linux'

    elif driver_type == 3:
        # Driver path for Firefox on Windows
        return absolute_path + '/driver/geckodriver.exe'

    elif driver_type == 4:
        # Driver path for Firefox on Linux
        return absolute_path + '/driver/geckodriver-v0.26-linux'


def get_driver(user_browser):
    # See more : https://www.selenium.dev/documentation/fr/webdriver/driver_requirements/

    # https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
    user_os = platform.system()

    if user_browser == "1":
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.page_load_strategy = 'eager'

        # chrome_opt.headless = True
        if user_os == "Windows":
            return webdriver.Chrome(executable_path=driver_path(1), options=chrome_opt)

        elif user_os == "Linux":
            return webdriver.Chrome(executable_path=driver_path(2), options=chrome_opt)

    elif user_browser == "2":
        firefox_opt = webdriver.FirefoxOptions()
        firefox_opt.page_load_strategy = 'eager'

        # firefox_opt.headless = True
        if user_os == "Windows":
            return webdriver.Firefox(executable_path=driver_path(3), options=firefox_opt)

        elif user_os == "Linux":
            return webdriver.Firefox(executable_path=driver_path(4), options=firefox_opt)

    else:
        print("Your platform is not currently supported.")
        sys.exit(1)


def get_browser():
    user_browser = ""

    print("You are running on ", platform.system(), platform.release())
    while not user_browser == "1" and not user_browser == "2":
        print("Choose your browser:\n\t1. Chrome\n\t2. Firefox")

        user_browser = input("> ")
        print("")

    return user_browser
