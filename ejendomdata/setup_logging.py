from __future__ import annotations
import logging.config
import yaml


def _setup_logging(debug=False):
    with open("logging.yaml", "rt") as f:
        config = yaml.safe_load(f.read())
    
    if debug:
        config["loggers"]["mylib"]["level"] = "DEBUG"
        config["handlers"]["console"]["level"] = "DEBUG"
    else:
        config["loggers"]["mylib"]["level"] = "INFO"
        config["handlers"]["console"]["level"] = "INFO"
    
    logging.config.dictConfig(config)

