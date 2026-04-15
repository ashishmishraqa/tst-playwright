import logging
from datetime import datetime
from pathlib import Path


def get_logger(name):
    # get path of current file
    current_path = Path(__file__).parent
    logs_dir = current_path.parent / "logs"
    # Ensure the directory exists
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Use absolute path string for FileHandler
        file_handler = logging.FileHandler(str(log_file), mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Prevent double logging if the root logger is also configured
        logger.propagate = False

    return logger