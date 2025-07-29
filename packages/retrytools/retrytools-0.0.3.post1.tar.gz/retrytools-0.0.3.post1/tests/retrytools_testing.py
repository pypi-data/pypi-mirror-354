import logging
from retrytools import retry

# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,                        # Minimum level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='[%(asctime)s] %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'                # Time format
)

# Example usage
logger = logging.getLogger(__name__)

counter = {"calls": 0}

@retry(ValueError, tries=2, delay=0.01, logger=logger)
def foo(x: int):
    counter["calls"] += 1
    if counter["calls"] < 2:
        raise ValueError("Bang")
    return "success"

x = foo(**{})