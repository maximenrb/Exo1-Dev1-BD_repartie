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


def add_level_in_file(text):
    add_in_file(text, "data/level")


def add_components_in_file(text):
    add_in_file(text, "data/components")


def add_spell_resistance_in_file(text):
    add_in_file(text, "data/spell_resistance")


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
        url_list = f.read().splitlines()

    with open('data/name') as f:
        name_list = f.read().splitlines()

    nb_links = len(url_list)

    spells = []

    for actual_link in range(0, nb_links):
        # Go to web page
        # TODO Add wait
        webDriver.get("https://aonprd.com/SpellDisplay.aspx?ItemName=" + url_list[actual_link])

        WebDriverWait(webDriver, 5).until(ec.presence_of_element_located(
            (By.XPATH, "//span[contains(@id, '_MainContent_DataListTypes_ct')]")))

        span_div_list = webDriver.find_elements_by_xpath(
            "//span[contains(@id, '_MainContent_DataListTypes_ct')]")

        for span_div in span_div_list:
            span_div_html = span_div.get_attribute("innerHTML")

            if not span_div_html == "":
                start_index_find = span_div_html.find(name_list[actual_link])

                wizard_pos = span_div_html.find("wizard", start_index_find) + 6
                h3_pos = span_div_html.find("<h3", wizard_pos)
                wizard_level = str(span_div_html[wizard_pos:h3_pos]).strip()

                wizard_level = wizard_level[:1]

                components_pos = span_div_html.find("<b>Components</b> ", start_index_find) + 18
                h3_pos = span_div_html.find("<h3", components_pos)
                components_string = str(span_div_html[components_pos:h3_pos])

                if components_string.find("(") > 0:
                    components_string = components_string[:components_string.find("(")]

                components_list = components_string.split(", ")

                for i in range(0, len(components_list)):
                    # Remove unless text in components
                    if len(components_list[i]) > 1:

                        or_position = str(components_list[i]).find("or")

                        if or_position > 0:
                            components_list[i] = components_list[i][:or_position-1] + "/" + \
                                                 components_list[i][or_position+3:]

                        components_list[i] = str(components_list[i]).strip()

                spell_resistance = False

                if not span_div_html.find("Spell Resistance", start_index_find,
                                          span_div_html.find("Description", start_index_find)) == -1:

                    spell_resistance_pos = span_div_html.find("<b>Spell Resistance</b>") + 23
                    h3_pos = span_div_html.find("<h3", spell_resistance_pos)
                    string_spell_resistance = str(span_div_html[spell_resistance_pos:h3_pos])

                    if string_spell_resistance.find("(") > 0:
                        spell_resistance = string_spell_resistance[:string_spell_resistance.find("(")]

                    if string_spell_resistance.lower().find("no") > 0:
                        spell_resistance = False
                    elif string_spell_resistance.lower().find("yes") > 0:
                        spell_resistance = True

                # spells.append(SpellObject(name_list[actual_link], wizard_level, components_list, spell_resistance))

                add_level_in_file(str(wizard_level))
                add_components_in_file(str(components_list).strip('[]'))
                add_spell_resistance_in_file(str(spell_resistance))

                print("Name: ", name_list[actual_link], " | Level: ", wizard_level, " | Components: ", components_list,
                      " | Spell Resistance: ", spell_resistance, " | ", actual_link, "/", nb_links)

    print(spells)

    # spells2 = webDriver.find_element_by_xpath("//h3[contains(text(),'Casting')]")
    # print(spells2)