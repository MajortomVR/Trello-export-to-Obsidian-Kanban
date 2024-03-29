import os

# Export structure
# ├── Boards
# │   ├── Board ID
# │   │   ├── attachments
# │   │   │   └── media files
# │   │   ├── checklists
# │   │   │   └── checklists_cardid.json
# │   │   ├── board.json
# │   │   ├── lists.json
# │   │   ├── cards.json
# │   │   └── labels.json

BOARDS_FOLDER = "boards"
ATTACHMENTS_FOLDER = "attachments"
CHECKLISTS_FOLDER = "checklists"


def get_board_folder(board_id: str) -> str:
    """
    Get the folder path for a specific board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The folder path for the board.
    """
    return os.path.join(BOARDS_FOLDER, board_id)


def get_attachment_folder(board_id: str) -> str:
    """
    Get the folder path for attachments of a specific board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The folder path for attachments of the board.
    """
    return os.path.join(get_board_folder(board_id), ATTACHMENTS_FOLDER)


def get_checklists_folder(board_id: str) -> str:
    """
    Get the folder path for checklists of a specific board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The folder path for checklists of the board.
    """
    return os.path.join(get_board_folder(board_id), CHECKLISTS_FOLDER)


def get_board_json_file(board_id: str) -> str:
    """
    Get the file path for the JSON file containing board information.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The file path for the JSON file containing board information.
    """
    return os.path.join(get_board_folder(board_id), "board.json")


def get_cards_json_file(board_id: str) -> str:
    """
    Get the file path for the JSON file containing card information.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The file path for the JSON file containing card information.
    """
    return os.path.join(get_board_folder(board_id), "cards.json")


def get_lists_json_file(board_id: str) -> str:
    """
    Get the file path for the JSON file containing list information.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The file path for the JSON file containing list information.
    """
    return os.path.join(get_board_folder(board_id), "lists.json")


def get_labels_json_file(board_id: str) -> str:
    """
    Get the file path for the JSON file containing label information.

    Args:
        board_id (str): The ID of the board.

    Returns:
        str: The file path for the JSON file containing label information.
    """
    return os.path.join(get_board_folder(board_id), "labels.json")


def get_checklists_for_card_json_file(board_id: str, card_id: str) -> str:
    """
    Get the file path for the JSON file containing checklists for a specific card.

    Args:
        board_id (str): The ID of the board.
        card_id (str): The ID of the card.

    Returns:
        str: The file path for the JSON file containing checklists for the card.
    """
    return os.path.join(get_board_folder(board_id), f"checklists_{card_id}.json")


def get_checklist_json_file(board_id: str, checklist_id: str) -> str:
    """
    Get the file path for the JSON file containing a specific checklist.

    Args:
        board_id (str): The ID of the board.
        checklist_id (str): The ID of the checklist.

    Returns:
        str: The file path for the JSON file containing the checklist.
    """
    return os.path.join(get_checklists_folder(board_id), f"{checklist_id}.json")


def get_attachments_for_card_json_file(board_id: str, card_id: str) -> str:
    """
    Get the file path for the JSON file containing attachments for a specific card.

    Args:
        board_id (str): The ID of the board.
        card_id (str): The ID of the card.

    Returns:
        str: The file path for the JSON file containing attachments for the card.
    """
    return os.path.join(get_attachment_folder(board_id), f"attachments_{card_id}.json")


def get_attachment_file(board_id: str, attachment_filename: str) -> str:
    """
    Get the file path for a specific attachment.

    Args:
        board_id (str): The ID of the board.
        attachment_filename (str): The filename of the attachment.

    Returns:
        str: The file path for the attachment.
    """
    return os.path.join(get_attachment_folder(board_id), attachment_filename)