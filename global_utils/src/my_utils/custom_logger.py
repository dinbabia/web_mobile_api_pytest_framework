"""
Custome Loggers with logging and allure during test reports.
"""

import logging
import inspect
from datetime import datetime
import os


def create_directory_if_not_exist(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' is ensured to exist (created or already existed)")


class SingletonLogger:
    _logger = None

    @classmethod
    def get_logger(cls):
        """
        Custom Singleton Logger which will create a `{current_day}.log` file under _reports folder.
        This will be instantiated once only.

         How to use
        ----------
        >>> from your_directory_folder/customer_logger import SingletonLogger
        >>> logger = SingletonLogger.get_logger()
        """
        if cls._logger is None:
            now = datetime.now()
            current_day = now.strftime("%b-%d-%Y")

            # Get the class / method name from where this customLogger method is called
            log_name = inspect.stack()[1][3]

            # Create the logging object and pass the logName in it
            cls._logger = logging.getLogger(log_name)

            # Set the Log level
            cls._logger.setLevel(logging.DEBUG)

            # Create Logs and Reports Folder if not yet created
            logs_folder = os.path.join(os.getcwd(), "_logs")
            reports_folder = os.path.join(os.getcwd(), "_reports")

            create_directory_if_not_exist(logs_folder)
            create_directory_if_not_exist(reports_folder)

            # Create the filehandler to save the logs in the file
            filehandler = logging.FileHandler(f"_logs/{current_day}.log", mode='a')

            # Set the loglevel of filehandler
            filehandler.setLevel(logging.DEBUG)

            # Create the formatter in which format do you like to save the logs
            formatter = logging.Formatter('%(asctime)s [Pytest]-[' + log_name + '] [%(levelname)s]: %(message)s', datefmt='%b-%d-%Y %I:%M:%S %p') # noqa

            # Set the formatter to filehandler
            filehandler.setFormatter(formatter)

            # Add file handler to logging
            cls._logger.addHandler(filehandler)

        return cls._logger
