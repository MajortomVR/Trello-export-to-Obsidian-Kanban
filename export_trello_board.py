import argparse
import sys

import src.exporter as exporter
import src.util as util
from src.create_obsidian_kanban_board import ObsidianKanban
from src.trello import Trello

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


STRING_TOOL_DESCRIPTION = "A tool for exporting Trello boards and creating Obsidian Kanban boards from the exported data."

# Help messages for command-line arguments
STRING_HELP_TRELLO_API_KEY = "Trello API-Key"
STRING_HELP_TRELLO_API_TOKEN = "Trello API-Token"
STRING_HELP_TRELLO_BOARD_ID = "Optional: Trello Board ID (or URL) for the board you want to export. Omit to get a list of all boards."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=STRING_TOOL_DESCRIPTION)
    parser.add_argument("api_key", help=STRING_HELP_TRELLO_API_KEY)
    parser.add_argument("api_token", help=STRING_HELP_TRELLO_API_TOKEN)
    parser.add_argument("board_id", nargs='?', default=None, help=STRING_HELP_TRELLO_BOARD_ID)

    args = parser.parse_args()
        
    trello = Trello(args.api_key, args.api_token)

    # Check if board_id is a url
    if util.is_url(args.board_id):
        print("Getting board_id from trello.com...")
        args.board_id = trello.get_board_id_from_url(args.board_id)
        
        if not args.board_id:
            print("ERROR: Couldn't get the board_id from the given URL!")
            sys.exit(1)
        else:
            print(f"Board ID: {args.board_id}")
            
    if args.board_id:                
        exporter.export_board(trello, args.board_id)      

        kanban = ObsidianKanban()
        kanban.export(args.board_id)
    else:              
        boards = trello.get_boards()        
        
        if boards:
            print(f"Listing Boards ({len(boards)}):")
            
            for i, board in enumerate(boards, start=1):
                index = f"[{i}]".rjust(4) # Right-align the current index for consistent formatting.
                name = board["name"][:40].ljust(40) # Ensure a fixed width for the board name (max 40 characters) and left-align it for readability.
                board_id = board["id"]
                print(f"{index} Name: {name} Board ID: {board_id}")
        else:
            print("No boards found!")