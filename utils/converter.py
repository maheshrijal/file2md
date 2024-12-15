import os
import logging
from markitdown import MarkItDown

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def convert_to_markdown(file_path):
    """
    Convert various file formats to markdown using markitdown library
    """
    try:
        logger.debug(f"Converting file: {file_path}")
        markitdown = MarkItDown()  # Initialize for each conversion
        logger.debug("MarkItDown initialized successfully")
        result = markitdown.convert(file_path)
        logger.debug(f"Conversion successful, content length: {len(result.text_content)}")
        return result.text_content
    except Exception as e:
        logger.error(f"Error converting file: {str(e)}")
        raise Exception(f"Failed to convert file: {str(e)}")