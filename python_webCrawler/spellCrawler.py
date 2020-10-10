# Must install selenium package
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import threading

from python_webCrawler import fileFunc
from python_webCrawler.spellObject import SpellObject
from python_webCrawler.driverPath import get_driver


def home_crawler():
    # Initiate web driver
    web_driver = get_driver()

    # Go to web page
    web_driver.get('https://aonprd.com/Spells.aspx?Class=Wizard')

    # Wait loading of web page elements
    WebDriverWait(web_driver, 5).until(ec.presence_of_element_located(
        (By.XPATH, "//a[contains(@href,'SpellDisplay')]")))

    # Get all "a" divs with href field starting by 'SpellDisplay..."
    spells = web_driver.find_elements_by_xpath("//a[contains(@href, 'SpellDisplay')]")

    for spell in spells:
        # Remove "M", "FMR" or "V" links
        if len(spell.text) > 2 and not str(spell.text) == "FMR":

            # Get the link of the current div
            link = str(spell.get_attribute("href"))
            print(link)

            # Remove redundant part of link
            short_link = link[link.find("=")+1:]

            # Save links in file
            fileFunc.add_url(short_link)
            fileFunc.add_name(spell.text)


def crawler(url_list, name_list):
    # Initiate web driver
    # You can define values for multithreading like get_driver("1", "1") for chrome Windows driver
    web_driver = get_driver()

    nb_links = len(url_list)

    for actual_link in range(0, nb_links):
        # Go to web page
        # TODO Add wait
        web_driver.get("https://aonprd.com/SpellDisplay.aspx?ItemName=" + url_list[actual_link])

        WebDriverWait(web_driver, 5).until(ec.presence_of_element_located(
            (By.XPATH, "//span[contains(@id, '_MainContent_DataListTypes_ct')]")))

        span_div_list = web_driver.find_elements_by_xpath(
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

                        # Remove useless components for page like :
                        #   https://aonprd.com/SpellDisplay.aspx?ItemName=Memory%20of%20Function
                        if not str(components_list[i]).isupper():
                            components_list.remove(components_list[i])

                spell_resistance = False

                if not span_div_html.find("Spell Resistance", start_index_find,
                                          span_div_html.find("Description", start_index_find)) == -1:

                    spell_resistance_pos = span_div_html.find("<b>Spell Resistance</b>") + 23
                    h3_pos = span_div_html.find("<h3", spell_resistance_pos)
                    string_spell_resistance = str(span_div_html[spell_resistance_pos:h3_pos])

                    if string_spell_resistance.find("(") > 0:
                        string_spell_resistance = string_spell_resistance[:string_spell_resistance.find("(")]

                    if string_spell_resistance.lower().find("no") > 0:
                        spell_resistance = False
                    elif string_spell_resistance.lower().find("yes") > 0:
                        spell_resistance = True

                # spells.append(SpellObject(name_list[actual_link], wizard_level, components_list, spell_resistance))

                # fileFunc.add_level(str(wizard_level))
                # fileFunc.add_components(str(components_list).strip('[]'))
                # fileFunc.add_spell_resistance(str(spell_resistance))

                print("Name: ", name_list[actual_link], " | Level: ", wizard_level, " | Components: ", components_list,
                      " | Spell Resistance: ", spell_resistance, " | ", actual_link, "/", nb_links-1)

    # spells2 = webDriver.find_element_by_xpath("//h3[contains(text(),'Casting')]")
    # print(spells2)


def multi_thread_crawler():
    with open('data/url_short') as f:
        url_list = f.read().splitlines()

    with open('data/name') as f:
        name_list = f.read().splitlines()

    nb_thread = 4

    div_result = (len(url_list) - 1) // nb_thread
    mod_result = (len(url_list) - 1) % nb_thread

    inf = 0
    sup = div_result

    for i in range(0, nb_thread):
        crawler_thread = threading.Thread(target=crawler, args=(url_list[inf:sup], name_list[inf:sup]))
        print("Prepare thread")
        crawler_thread.start()
        print("Thread start for slice:", inf, ":", sup)

        inf = sup + 1
        sup += div_result

        if i == nb_thread - 2:
            sup += mod_result


def mono_thread_crawler():
    with open('data/url_short') as f:
        url_list = f.read().splitlines()

    with open('data/name') as f:
        name_list = f.read().splitlines()

    # url_list = ["Memory%20of%20Function"]
    # name_list = ["Memory of Function"]

    crawler(url_list, name_list)
