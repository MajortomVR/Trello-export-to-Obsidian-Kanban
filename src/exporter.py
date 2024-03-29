from typing import Any

from src.trello import Trello
import src.file_system as file_system
import src.file_structure as file_structure


def export_board(trello: Trello, board_id: str) -> None:
    """
    Export a Trello board to the file system.

    Args:
        trello (Trello): The Trello instance used to fetch board data.
        board_id (str): The ID of the Trello board to export.
    """
    
    # Cleanup if there was a previous export
    file_system.delete_folder(file_structure.get_board_folder(board_id))

    # Create necessary folders
    _create_folders(board_id)

    # Fetch board data
    print("Getting board...")
    board_json = trello.get_board(board_id)
    cards_json = trello.get_all_cards(board_id)
    lists_json = trello.get_lists(board_id)
    labels_json = trello.get_labels(board_id)
    
    
    if board_json:
        print(f"Board Title: {board_json['name']}")
    else:
        print(f"ERROR getting Board: {board_id}")

    # Write board data to files
    file_system.write_file_json(file_structure.get_board_json_file(board_id), board_json)
    file_system.write_file_json(file_structure.get_cards_json_file(board_id), cards_json)
    file_system.write_file_json(file_structure.get_lists_json_file(board_id), lists_json)
    file_system.write_file_json(file_structure.get_labels_json_file(board_id), labels_json)
   
    # Process cards, checklists and attachments
    print(f"Getting cards ({len(cards_json)})...")
        
    for card in cards_json:
        _get_checklists(trello, board_id, card["id"], card["idChecklists"])
        _get_attachments(trello, board_id, card["id"], card["badges"]["attachments"])
        
        
def _create_folders(board_id: str) -> None:
    """
    Create necessary folders for the Trello board export.

    Args:
        board_id (str): The ID of the Trello board.

    """
    folders = [
            file_structure.BOARDS_FOLDER,
            file_structure.get_board_folder(board_id),
            file_structure.get_attachment_folder(board_id),
            file_structure.get_checklists_folder(board_id)
        ]
    
    for folder in folders:
        file_system.create_folder(folder)


def _get_checklists(trello: Trello, board_id: str, card_id: str, checklists: Any) -> None:
    """
    Fetch and write checklists data for a Trello card to the file system.

    Args:
        trello (Trello): An instance of the Trello class used to fetch data.
        board_id (str): The ID of the Trello board.
        card_id (str): The ID of the Trello card.
        checklists (Any): The checklists data associated with the card.
    """
    if checklists:
        file_system.write_file_json(file_structure.get_checklists_for_card_json_file(board_id, card_id), checklists)

        for checklist_id in checklists:
            checklist_json = trello.get_checklist(checklist_id)
            file_system.write_file_json(
                file_structure.get_checklist_json_file(board_id, checklist_id),
                checklist_json)


def _get_attachments(trello: Trello, board_id: str, card_id: str, attachments: Any) -> None:
    """
    Fetch and write attachments data for a Trello card to the file system.

    Args:
        trello (Trello): An instance of the Trello class used to fetch data.
        board_id (str): The ID of the Trello board.
        card_id (str): The ID of the Trello card.
        attachments (Any): The attachments data associated with the card.
    """
    if attachments:
        # TODO: HANDLE EXTERNAL LINKS!
        attachments_json = trello.get_attachments(card_id)

        file_system.write_file_json(file_structure.get_attachments_for_card_json_file(board_id, card_id), attachments_json)
        
        for attachment in attachments_json:
            url:str = attachment["url"].replace("trello.com", "api.trello.com")                
            
            print("Downloading:", url)
            # TODO: Retry download if it failed
            trello.download_attachment(
                url,
                file_structure.get_attachment_file(board_id, attachment["fileName"]))

