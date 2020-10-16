def add_with_line_feed(text, path):
    # Open a file with access mode 'a'
    with open(path, "a") as file_object:
        # Append text at the end of file
        file_object.write(text + '\n')


def add(text, path):
    # Open a file with access mode 'a'
    with open(path, "a") as file_object:
        # Append text at the end of file
        file_object.write(text)


def add_url(url):
    add_with_line_feed(url, "data/all_url_short")


def add_name(name):
    add_with_line_feed(name, "data/all_name")


def add_name_for_json(name):
    add_with_line_feed(name, "data/all_name_for_json")


def add_level(level):
    add_with_line_feed(level, "data/all_level")


def add_components(components):
    add_with_line_feed(components, "data/all_components")


def add_spell_resistance(spell_resistance):
    add_with_line_feed(spell_resistance, "data/all_spell_resistance")


def add_json(name, level, components, spell_resistance):
    level_json = ""

    if not str(level) == "":
        level_list = str(level).split(", ")

        for level_elm in level_list:
            level_json += "\"" + level_elm[:len(level_elm)-2] + "\": " + level_elm[len(level_elm)-1:] + ","

        level_json = level_json.rstrip(",")

    json = "{\"name\": \"" + name + "\"," \
            "\"level\": {" + level_json + "}," \
            "\"components\": [" + str(components).replace("\'", "\"") + "]," \
            "\"spell_resistance\": " + str(spell_resistance).lower() + "}"

    add(json, 'data/spells.json')


def get_list(path):
    with open(path) as f:
        elm_list = f.read().splitlines()

    return elm_list


def get_name_list():
    return get_list('data/all_name')


def get_name_for_json_list():
    return get_list('data/all_name_for_json')


def get_url_list():
    return get_list('data/all_url_short')


def get_level_list():
    return get_list('data/all_level')


def get_components_list():
    return get_list('data/all_components')


def get_spell_resistance_list():
    return get_list('data/all_spell_resistance')
