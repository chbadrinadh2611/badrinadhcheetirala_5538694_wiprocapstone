import configparser
import os


class ConfigReader:
    """Utility to read config.properties file."""

    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "config.properties")
        self.config = configparser.RawConfigParser()
        self.config.read(config_path)

    def get(self, key, fallback=None):
        try:
            return self.config["DEFAULT"][key]
        except KeyError:
            return fallback

    def get_browser(self):
        return self.get("browser", "chrome")

    def get_base_url(self):
        return self.get("base_url", "https://www.nykaa.com/")

    def get_mom_baby_url(self):
        return self.get("mom_baby_url", "https://www.nykaa.com/mom-and-baby/c/3165")

    def get_implicit_wait(self):
        return int(self.get("implicit_wait", 10))

    def get_timeout(self):
        return int(self.get("timeout", 20))

    def get_phone_number(self):
        return self.get("phone_number", "9441211174")
