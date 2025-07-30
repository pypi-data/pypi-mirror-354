from unittest import TestCase

from artless_core import Config


class TestConfig(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.default_config = {
            "debug": False,
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": "[{asctime}] [{process:d}] [{levelname}] {message}",
                        "datefmt": "%Y-%m-%d %H:%M:%S",
                        "style": "{",
                    },
                },
                "handlers": {
                    "stdout": {
                        "formatter": "default",
                        "level": "INFO",
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                    }
                },
                "loggers": {
                    "artless_core": {
                        "level": "INFO",
                        "handlers": ["stdout"],
                        "propagate": False,
                    }
                },
                "root": {"level": "WARNING", "handlers": ["stdout"]},
            },
        }

    def test_singleton(self):
        config1 = Config()
        config2 = Config()
        self.assertIs(config1, config2)

    def test_default_config(self):
        self.assertDictEqual(Config().current, self.default_config)
