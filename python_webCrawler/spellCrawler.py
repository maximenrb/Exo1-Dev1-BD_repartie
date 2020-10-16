# Must install selenium package
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import threading

from python_webCrawler import fileFunc
from python_webCrawler.spellObject import SpellObject
from python_webCrawler.driverPath import get_driver
from python_webCrawler.driverPath import get_browser


global_lock = threading.Lock()


def home_crawler():
    # Initiate web driver
    browser = get_browser()
    web_driver = get_driver(browser)

    # Go to web page
    web_driver.get('https://aonprd.com/Spells.aspx?Class=All')

    # Get all "a" divs with href field starting by 'SpellDisplay..."
    spells = web_driver.find_elements_by_xpath("//a[contains(@href, 'SpellDisplay')]")

    for spell in spells:
        # Remove "M", "FMR" or "V" links
        if len(spell.text) > 2 and not str(spell.text) == "FMR" and not str(spell.text) == "FRT":

            # Get the link of the current div
            link = str(spell.get_attribute("href"))
            print(link)

            # Remove redundant part of link
            short_link = link[link.find("=")+1:]

            # Save links in file
            fileFunc.add_url(short_link)
            fileFunc.add_name(spell.text)


def get_level(span_div_html, start_find_index):
    level = ""

    # Get information from div
    level_pos = span_div_html.find("<b>Level</b>", start_find_index)

    if level_pos > 0:
        level_pos += 12
        h3_pos = span_div_html.find("<h3", level_pos)
        level = str(span_div_html[level_pos:h3_pos]).strip()

        if level.rfind(")")+1 == len(level):
            level = level[:level.rfind("(")]
            level = level.strip()

    # Return only the first element of the string to avoid error (because level is a digit)
    return level


def get_components(span_div_html, start_find_index):
    # Get information from div
    components_pos = span_div_html.find("<b>Components</b> ", start_find_index) + 18
    h3_pos = span_div_html.find("<h3", components_pos)
    components_string = str(span_div_html[components_pos:h3_pos])

    # Remove bracket part and content if exist before split string
    if components_string.find("(") > 0:
        components_string = components_string[:components_string.find("(")]

    components_list = components_string.split(", ")

    for i in range(0, len(components_list)):
        # Remove useless text in components

        if len(components_list[i]) > 1:

            # Detect if we have something like : "V or D"
            or_position = str(components_list[i]).find("or")

            # And concatenate to have : "V/D"
            if or_position > 0:
                components_list[i] = components_list[i][:or_position-1] + "/" + \
                                 components_list[i][or_position+3:]

            # Remove leading and trailing space if exist
            components_list[i] = str(components_list[i]).strip()

            # Remove useless components for page like :
            #   https://aonprd.com/SpellDisplay.aspx?ItemName=Memory%20of%20Function
            if not str(components_list[i]).isupper():
                components_list.remove(components_list[i])

    return components_list


def get_spell_resistance(span_div_html, start_find_index):
    spell_resistance = False

    # Check if "Spell resistance" is present in div content
    if not span_div_html.find(
            "Spell Resistance", start_find_index, span_div_html.find("Description", start_find_index)) == -1:

        # Get information from div
        spell_resistance_pos = span_div_html.find("<b>Spell Resistance</b>") + 23
        h3_pos = span_div_html.find("<h3", spell_resistance_pos)
        spell_resistance_str = str(span_div_html[spell_resistance_pos:h3_pos])

        # Remove bracket part and content if exist
        if spell_resistance_str.find("(") > 0:
            spell_resistance_str = spell_resistance_str[:spell_resistance_str.find("(")]

        # Detect if "yes" or "no" is present in retrieved information
        if spell_resistance_str.lower().find("no") > 0:
            spell_resistance = False
        elif spell_resistance_str.lower().find("yes") > 0:
            spell_resistance = True

    return spell_resistance


def crawler(url_list, name_list, web_driver):
    nb_links = len(url_list)

    for actual_link in range(0, nb_links):
        # Go to web page
        web_driver.get("https://aonprd.com/SpellDisplay.aspx?ItemName=" + url_list[actual_link])

        # Get all span divs with an id that contain "_MainContent_DataListTypes_ct"
        # Because content is in "_MainContent_DataListTypes_ct100..." in somme pages, or for instance
        # in "_MainContent_DataListTypes_ct102..." for other pages
        span_div_list = web_driver.find_elements_by_xpath(
            "//span[contains(@id, '_MainContent_DataListTypes_ct')]")

        for span_div in span_div_list:
            # Get HTML code of retrieved element
            span_div_html = span_div.get_attribute("innerHTML")

            # Detect if span is not empty (present in some pages)
            if not span_div_html == "":

                # Search and use this index because one page can regroup different spells
                start_find_index = span_div_html.find(name_list[actual_link])

                level = get_level(span_div_html, start_find_index)
                components_list = get_components(span_div_html, start_find_index)
                spell_resistance = get_spell_resistance(span_div_html, start_find_index)

                # spells.append(SpellObject(name_list[actual_link], wizard_level, components_list, spell_resistance))

                while global_lock.locked():
                    continue

                global_lock.acquire()

                # fileFunc.add_level(str(level))
                # fileFunc.add_components(str(components_list).strip('[]'))
                # fileFunc.add_spell_resistance(str(spell_resistance))
                fileFunc.add_json(name_list[actual_link], level, components_list, spell_resistance)

                print("Name: ", name_list[actual_link], " | Level: ", level, " | Components: ", components_list,
                      " | Spell Resistance: ", spell_resistance, " | ", actual_link, "/", nb_links-1)

                global_lock.release()


def mono_thread_crawler():
    browser = get_browser()

    crawler(fileFunc.get_url_list(), fileFunc.get_name_list(), get_driver(browser))


def multi_thread_crawler(nb_thread=4):
    url_list = fileFunc.get_url_list()
    name_list = fileFunc.get_name_list()

    div_result = (len(url_list) - 1) // nb_thread
    mod_result = (len(url_list) - 1) % nb_thread

    inf = 0
    sup = div_result

    browser = get_browser()
    threads_list = []

    for i in range(0, nb_thread):
        crawler_thread = threading.Thread(target=crawler,
                                          args=(url_list[inf:sup], name_list[inf:sup], get_driver(browser)))
        print("Thread ", i+1, " is ready")
        threads_list.append(crawler_thread)

        crawler_thread.start()
        print("Thread ", i+1, " started for spells from ", inf+1, " to ", sup+1, "\n")

        inf = sup + 1
        sup += div_result

        if i == nb_thread - 2:
            sup += mod_result

    for thread in threads_list:
        # Wait until thread terminates its task
        thread.join()

    print("\nAll threads completed")
