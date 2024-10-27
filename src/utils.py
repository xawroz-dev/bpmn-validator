import os
import logging
from datetime import datetime

# Configure logging
def setup_logging(log_file=None):
    """
    Sets up logging for the application.
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    if log_file:
        # Ensure the log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(filename=log_file, level=logging.INFO, format=log_format)
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)

def get_timestamp():
    """
    Returns the current timestamp as a string.
    """
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def read_file_lines(file_path):
    """
    Reads a file and returns a list of lines without newline characters.
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def write_to_file(file_path, content):
    """
    Writes the given content to a file.
    """
    with open(file_path, 'w') as f:
        f.write(content)
