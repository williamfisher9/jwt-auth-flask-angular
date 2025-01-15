import json
from datetime import date
from logging.config import fileConfig, dictConfig

def initialize_logging_configs():
    with open("configs\\app-configs.json", "r") as props_file:
        """
        this will read json config file as json
        then uses json.loads to convert json string to dictionary
        then will read LOG_DIRECTORY and LOGGING_CONFIGS from the dictionary
        and finally, set the file handler file name to the path and file name
        """
        configs_json = props_file.read()
        configs_dict = json.loads(configs_json)
        logging_config_dict = configs_dict['LOGGING_CONFIGS']
        log_directory = configs_dict['LOG_DIRECTORY']
        info_logging_file_name = "info_logs_" + date.today().strftime('%m_%d_%Y') + ".log"
        error_logging_file_name = "error_logs_" + date.today().strftime('%m_%d_%Y') + ".log"
        logging_config_dict['handlers']['info_rotating_file_handler']['filename'] = log_directory + info_logging_file_name
        logging_config_dict['handlers']['error_file_handler']['filename'] = log_directory + error_logging_file_name
        dictConfig(logging_config_dict)

    #fileConfig("configs\logging-config.conf")
    """
    logging-config.conf
    
    [loggers]
keys=root

[handlers]
keys=fileHandler,streamHandler

[formatters]
keys=form01

[logger_root]
level=NOTSET
handlers=fileHandler,streamHandler

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=form01
args=('logs.log', 'w')

[handler_streamHandler]
class=StreamHandler
level=NOTSET
formatter=form01
args=(sys.stdout,)

[formatter_form01]
class=logging.Formatter
format=%(asctime)s %(levelname)s %(name)s: %(message)s %(custom_field)s
datefmt=%m/%d/%Y %I:%M:%S %p
style=%
validate=True
defaults={'custom_field': ''}

    """

    """
        with open("configs\\app-configs.json", "r") as props_file:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=f'{json.load(props_file)["LOGGING_DIRECTORY"]}\\logs_{date.today().strftime('%m_%d_%Y')}.log',
            encoding='utf-8',
            level=logging.DEBUG # minimum logging level
        )
    """