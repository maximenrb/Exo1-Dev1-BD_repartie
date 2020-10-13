class SpellObject:
    def __init__(self, name, level, components, spell_resistance):
        self.name = name
        self.level = level
        self.components = components
        self.spell_resistance = spell_resistance

    def export_to_json(self):
        json = "{\"name\": \"" + self.name + "\", " \
                "\"level\": " + self.level + ", " \
                "\"components\": " + str(self.components) + ", " \
                "\"spell_resistance\": " + str(self.spell_resistance).lower() + "}"

        print(json)
