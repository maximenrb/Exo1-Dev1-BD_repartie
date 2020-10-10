def add(text, path):
    # Open a file with access mode 'a'
    with open(path, "a") as file_object:
        # Append text at the end of file
        file_object.write(text + '\n')


def add_url(text):
    add(text, "data/url_short")


def add_name(text):
    add(text, "data/name")


def add_level(text):
    add(text, "data/level")


def add_components(text):
    add(text, "data/components")


def add_spell_resistance(text):
    add(text, "data/spell_resistance")
