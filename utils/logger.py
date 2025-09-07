import logging
import json
from typing import Dict, Any

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('api_tests.log'),
            logging.StreamHandler()
        ]
    )

def log_request(method: str, url: str, headers: Dict[str, Any] = None, data: Dict[str, Any] = None):
    logger = logging.getLogger('API_Logger')
    logger.info(f"Request: {method} {url}")
    if headers:
        logger.debug(f"Headers: {json.dumps(headers, indent=2)}")
    if data:
        logger.debug(f"Body: {json.dumps(data, indent=2)}")

def log_response(response):
    logger = logging.getLogger('API_Logger')
    logger.info(f"Response: {response.status_code} - {response.reason}")
    logger.info(f"URL: {response.url}")
    try:
        if response.json():
            logger.debug(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except:
        logger.debug(f"Response Text: {response.text}")
    logger.debug(f"Response Headers: {dict(response.headers)}")

def log_cleanup(booking_id, success=True):
    logger = logging.getLogger('Cleanup_Logger')
    if success:
        logger.info(f"Successfully cleaned up booking {booking_id}")
    else:
        logger.warning(f"Failed to clean up booking {booking_id}")
