from typing import Tuple
from urllib.parse import urlparse


def is_url(url: str) -> bool:
    """
    Check if the given string is an url.

    Args:
        url (str): The string to check.

    Returns:
        bool: True if it is an url, else false.
    """
    return bool(urlparse(url).scheme)


def set_color_brightness(rgb: Tuple[int, int, int], brightness_factor: float) -> Tuple[int, int, int]:
    """
    Adjusts the brightness of an RGB color.

    Args:
        rgb (Tuple[int, int, int]): The RGB color represented as a tuple of three integers (0-255) 
                                    corresponding to red, green, and blue components.
        brightness_factor (float): The factor by which to adjust the brightness. Should be a value 
                                    between 0 and 1.

    Returns:
        Tuple[int, int, int]: The adjusted RGB color represented as a tuple of three integers (0-255) 
                                corresponding to the adjusted red, green, and blue components.
    """
    max_val = max(rgb)
    
    if max_val > 0:
        scale_factor = (brightness_factor * 255) / max_val    
        return [min(255, int(x * scale_factor)) for x in rgb]
    else:
        return [min(255, int(brightness_factor * 255)) for i in range(3)]
    
    
def get_color_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Calculate the relative luminance of a color represented by its RGB components.

    Args:
        rgb (Tuple[int, int, int]): A tuple representing the RGB components of the color.
            Each component should be an integer value in the range [0, 255].

    Returns:
        float: The relative luminance of the color, a value between 0 and 1.
            A value closer to 0 indicates a darker color, while a value closer to 1 indicates a lighter color.
    """
    red, green, blue = [x / 255 for x in rgb]
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def insert_char(character, string:str, index:int) -> str:
    return string[:index] + character + string[index:]
