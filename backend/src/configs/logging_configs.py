import logging
import json
from datetime import date

def initialize_logging_configs():
    with open("configs\\app-configs.json", "r") as props_file:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=f'{json.load(props_file)["LOGGING_DIRECTORY"]}\\logs_{date.today().strftime('%m_%d_%Y')}.log',
            encoding='utf-8',
            level=logging.DEBUG
        )