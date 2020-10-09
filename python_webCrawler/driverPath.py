# Must be changed :
# https://www.selenium.dev/documentation/fr/getting_started_with_webdriver/third_party_drivers_and_plugins/
import pathlib

absolute_path = str(pathlib.Path(__file__).parent.absolute())
absolute_path = absolute_path.replace("\\", "/")

DRIVER_PATH = absolute_path + '/driver/chromedriver.exe'


def get_driver_path():
    return DRIVER_PATH
