import configparser
from typing import Union


class Settings:
    """
    Wrapper for the settings file
    """

    # Default values
    DEFAULT = {"REF_RESIST": 10, "REF_RESIST_UNIT": " ", "REF_VOLT": 5.099, "NOISE_REDUCE": 1}
    SETTINGS_FILE = "settings.ini"

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()

        # Create file if none
        if len(self.config.read(self.SETTINGS_FILE)) <= 0:
            self.setup()
            # Reload
            self.config.read(self.SETTINGS_FILE)

    def setup(self):
        """
        Creates the file if it does not exist
        """
        f = open(self.SETTINGS_FILE, "w")
        f.write(
            f"""[DEFAULT]\nref_resist={self.DEFAULT["REF_RESIST"]}\nref_resist_unit={self.DEFAULT["REF_RESIST_UNIT"]}\nref_volt={self.DEFAULT["REF_VOLT"]}\nnoise_reduce={self.DEFAULT["NOISE_REDUCE"]}"""
        )
        f.close()

    def get_setting(self, key: str, default: str=None) -> Union[str, None]:
        """
        Read settings
        """
        if key in self.config["DEFAULT"]:
            return self.config["DEFAULT"][key] or " "
        else:
            # Auto write if not found
            if default is not None:
                self.update_setting(key, default)
            return default

    def update_setting(self, key: str, value):
        """
        Write to settings
        """
        self.config["DEFAULT"][key] = value
        # Save
        with open(self.SETTINGS_FILE, "w") as configfile:
            self.config.write(configfile)
