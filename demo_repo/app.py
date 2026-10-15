


import logging
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_status(url):
    """Return the HTTP status code for a valid HTTP or HTTPS URL."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("A valid HTTP or HTTPS URL is required.")

    try:
        response = requests.get(url, timeout=5)
        return response.status_code

    except requests.exceptions.Timeout:
        logger.exception("Request timed out for URL: %s", url)
        raise

    except requests.exceptions.ConnectionError:
        logger.exception("Connection failed for URL: %s", url)
        raise

    except requests.RequestException:
        logger.exception("Failed to retrieve URL: %s", url)
        raise

