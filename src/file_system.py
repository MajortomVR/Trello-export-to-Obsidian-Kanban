import os
import shutil
import json
from typing import Any


def create_folder(path:str) -> None:
    """
    Create a folder at the given path if it does not exist.

    Args:
        path (str): The path of the folder to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def delete_folder(path: str) -> None:
    """
    Delete a folder at the given path if it exists.

    Args:
        path (str): The path of the folder to delete.
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def write_file(file_path: str, file_content: str) -> None:
    """
    Write data to a file.

    Args:
        file_path (str): The path of the file to write to.
        file_content (str): The contents to write to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)


def read_file(file_path: str) -> str:
    """
    Read data from a file.

    Args:
        file_path (str): The path of the file to read from.

    Returns:
        str: The contents of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
      
      
def write_file_json(file_path: str, data: Any) -> None:
    """
    Write data to a JSON file.

    Args:
        file_path (str): The path of the JSON file to write to.
        data (any): The data to write to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write( json.dumps(data, ensure_ascii=False) )
   
   
def read_file_json(file_path: str) -> Any:
    """
    Read data from a JSON file.

    Args:
        file_path (str): The path of the JSON file to read from.

    Returns:
        any: The data read from the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
