import pathlib
from selenium import webdriver


absolute_path = str(pathlib.Path(__file__).parent.absolute())
absolute_path = absolute_path.replace("\\", "/")

# Must be changed :
# https://www.selenium.dev/documentation/fr/getting_started_with_webdriver/third_party_drivers_and_plugins/
#
# Change to '/driver/geckodriver.exe' if you want to use Firefox
DRIVER_PATH = absolute_path + '/driver/chromedriver.exe'
#DRIVER_PATH = absolute_path + '/driver/geckodriver.exe'
#DRIVER_PATH = absolute_path + '/driver/chromedriver-83.0.4103.39-linux'
#DRIVER_PATH = absolute_path + '/driver/geckodriver-v0.26-linux'

def get_driver():
    # Change to '.Firefox()' if you use Firefox
    # See more : https://www.selenium.dev/documentation/fr/webdriver/driver_requirements/
    return webdriver.Chrome(executable_path=DRIVER_PATH)
