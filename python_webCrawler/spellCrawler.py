# Must install selenium package
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from python_webCrawler.spellObject import SpellObject
from python_webCrawler.driverPath import get_driver


# Initiate web driver
webDriver = get_driver()


def add_in_file(text, path):
    # Open a file with access mode 'a'
    with open(path, "a") as file_object:
        # Append text at the end of file
        file_object.write(text + '\n')


def add_url_in_file(text):
    add_in_file(text, "data/url_short")


def add_name_in_file(text):
    add_in_file(text, "data/name")


def home_crawler():
    # Go to web page
    webDriver.get('https://aonprd.com/Spells.aspx?Class=Wizard')

    # Wait loading of web page elements
    WebDriverWait(webDriver, 5).until(ec.presence_of_element_located(
        (By.XPATH, "//a[contains(@href,'SpellDisplay')]")))

    # Get all elements with href starting by 'SpellDisplay..."
    spells = webDriver.find_elements_by_xpath("//a[contains(@href, 'SpellDisplay')]")

    for spell in spells:
        # Remove "M" or "V" links
        if len(spell.text) > 2:

            link = str(spell.get_attribute("href"))
            print(link)

            # Remove redundant part of link
            short_link = link[link.find("=")+1:]

            # Save links in file
            add_url_in_file(short_link)
            add_name_in_file(spell.text)


def crawler():
    with open('data/url_short') as f:
        lines = f.read().splitlines()

    nb_links = len(lines)

    spells = []

    for actual_link in range(0, nb_links):
        # Go to web page
        # TODO Add wait
        webDriver.get("https://aonprd.com/SpellDisplay.aspx?ItemName=" + lines[actual_link])

        span_content = webDriver.find_element_by_xpath("//span[@id='ctl00_MainContent_DataListTypes_ctl00_LabelName']")

        string = span_content.get_attribute("innerHTML")

        name_pos = string.find(';"> ') + 4
        h1_pos = string.find("</h1>", name_pos)
        name = string[name_pos:h1_pos]

        wizard_pos = string.find("wizard ") + 7
        h3_pos = string.find("<h3", wizard_pos)
        wizard_level = string[wizard_pos:h3_pos]

        components_pos = string.find("<b>Components</b> ") + 18
        h3_pos = string.find("<h3", components_pos)
        components_list = string[components_pos:h3_pos].split(", ")

        for i in range(0, len(components_list)):

            # Remove unless text in components
            if len(components_list[i]) > 2:
                temp_str = str(components_list[i])
                components_list[i] = temp_str[:temp_str.find(" ")]

        spell_resistance_pos = string.find("<b>Spell Resistance</b> ") + 24
        h3_pos = string.find("<h3", spell_resistance_pos)
        spell_resistance = string[spell_resistance_pos:h3_pos]

        if spell_resistance == "no":
            spell_resistance = False
        elif spell_resistance == "yes":
            spell_resistance = True

        spells.append(SpellObject(name, wizard_level, components_list, spell_resistance))
        print("Name: ", name, " | Level: ", wizard_level, " | Components: ", components_list,
              " | Spell Resistance", spell_resistance, " | ", actual_link, "/", nb_links)

    print(spells)

    # spells2 = webDriver.find_element_by_xpath("//h3[contains(text(),'Casting')]")
    # print(spells2)
