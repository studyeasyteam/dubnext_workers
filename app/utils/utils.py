import random
import string
import mimetypes
import os


def generate_random_string(length=10):
    """Generate a random log string of a given length."""
    characters = string.ascii_letters + string.digits  # Include both letters and digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_file_type(file_name):
    # Extract the file extension
    extension = file_name.lower().split('.')[-1]

    # Determine the file type based on the extension
    if extension == 'pdf':
        return 'PDF'
    elif extension in ['xls', 'xlsx']:
        return 'EXCEL'
    else:
        return 'UNKNOWN'
