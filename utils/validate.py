import magic
import logging
import tempfile

from fastapi import HTTPException

from settings import ACCEPTABLE_FILE_SUFFIXES, ACCEPTABLE_FILE_FORMATS

logger = logging.getLogger(__name__)


def validate_file_suffix(_file) -> bool:
    """
    [Validate image file suffix to make sure it's acceptable.]

    Args:
        _file ([type]): [Image file.]

    Raises:
        HTTPException: [Unacceptable file suffix.]

    Returns:
        bool: [File suffix validation boolean.]
    """
    logger.info(f'Validating image file {_file.filename} suffix...')
    filename = _file.filename
    suffix = filename.split('.')[-1]
    if suffix not in ACCEPTABLE_FILE_SUFFIXES:
        logger.warning(
            f'Image file {_file.filename} suffix {suffix} is unacceptable.')
        raise HTTPException(
            status_code=400,
            detail=
            f"Image file {_file.filename} suffix {suffix} is unacceptable.")
    logger.info(f'Image file {_file.filename} suffix validated!')
    return True


def validate_file_format(_file) -> bool:
    """
    [Validate image file format to make sure it's acceptable.]

    Args:
        _file ([type]): [Image file.]

    Raises:
        HTTPException: [Unacceptable file format.]

    Returns:
        bool: [File format validation boolean.]
    """
    logger.info(f'Validating image file {_file.filename} format...')
    _spooledtempfile = _file.file
    _namedtempfile = tempfile.NamedTemporaryFile(delete=False)
    _namedtempfile.write(_spooledtempfile.read())
    _tempath = _namedtempfile.name
    fileformat = magic.from_file(_tempath, mime=True)
    if fileformat not in ACCEPTABLE_FILE_FORMATS:
        logger.warning(
            f'Image file {_file.filename} format {fileformat} is unacceptable.'
        )
        raise HTTPException(
            status_code=400,
            detail=
            f"Image file {_file.filename} format {fileformat} is unacceptable."
        )
    logger.info(f'Image file {_file.filename} format validated!')
    return True


def validate_uploaded_file(_file) -> bool:
    """
    [Validate uploaded image file.]

    Args:
        _file ([type]): [Image file to be validated.]

    Returns:
        bool: [Image file validation boolean.]
    """
    logger.info(f'Validating image file {_file.filename}...')
    if (validate_file_suffix(_file) and validate_file_format(_file)):
        logger.info(f'Image file {_file.filename} validated!')
        return True
    else:
        logger.info(f'Image file {_file.filename} validation failed.')
        return False
