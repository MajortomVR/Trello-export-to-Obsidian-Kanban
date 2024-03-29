import json
import os
from typing import Any, List, Tuple

from src.kanban_board import Board, BoardList, Card, Label, Checklist, ChecklistItem
import src.file_system as file_system
import src.file_structure as file_structure
from src.util import set_color_brightness, insert_char


class ObsidianKanban:
    color_values = {
            "green": (4, 110, 79),
            "yellow": (130, 95, 20),
            "orange": (172, 73, 19),
            "red": (182, 48, 41),
            "purple": (94, 77, 175),
            "blue": (0, 85, 200),
            "sky": (0, 106, 129),
            "lime": (73, 107, 38),
            "pink": (154, 62, 114),
            "black": (87, 103, 114),
            
            "green_dark": (6, 75, 54),
            "yellow_dark": (85, 63, 13),
            "orange_dark": (117, 47, 9),
            "red_dark": (97, 32, 28),
            "purple_dark": (53, 44, 97),
            "blue_dark": (0, 50, 106),
            "sky_dark": (7, 69, 84),
            "lime_dark": (53, 71, 34),
            "pink_dark": (83, 37, 62),
            "black_dark": (68, 79, 88),
            
            "green_light": (33, 205, 153),
            "yellow_light": (231, 178, 45),
            "orange_light": (255, 164, 105),
            "red_light": (255, 114, 107),
            "purple_light": (159, 143, 235),
            "blue_light": (69, 157, 251),
            "sky_light": (91, 195, 222),
            "lime_light": (143, 199, 84),
            "pink_light": (239, 117, 185),
            "black_light": (138, 155, 170)
        }
    
    
    def export(self, board_id):                
        """
        Export the contents of a Trello board to a Markdown file compatible with Obsidian's Kanban plugin.

        Parameters:
            board_id (str): The ID of the Trello board to export.
        """
        board: Board = self._load_board(board_id)
        self._create_markdown_file(board)
    
    
    def _load_board(self, board_id: str) -> Board:
        """
        Load a Trello board from JSON files and construct a Board object.

        Parameters:
            board_id (str): The ID of the Trello board to load.

        Returns:
            Board: The Board object representing the loaded Trello board.
        """
        board_json = file_system.read_file_json(file_structure.get_board_json_file(board_id))
        lists_json = file_system.read_file_json(file_structure.get_lists_json_file(board_id))
        labels_json = file_system.read_file_json(file_structure.get_labels_json_file(board_id))
        cards_json = file_system.read_file_json(file_structure.get_cards_json_file(board_id))
                
        board:Board = Board(board_id, board_json["name"])
        
        for list in lists_json:
            board_list = BoardList(list["id"], list["name"])

            # Add Cards now
            for card in cards_json:                
                if card["idList"] == board_list.id:
                    board_card = Card(card["id"], 
                                      card["name"],
                                      card["desc"].replace("\n", "<br>")) # Remove ascii line-breaks to html line-breaks                    
                    
                    # Add Labels
                    for label_id in card["idLabels"]:
                        board_card.labels.append(self._get_label_name(label_id, labels_json))
                    
                    # Add Attachments
                    if card["badges"]["attachments"]:
                        id_attachment_cover = card["idAttachmentCover"]
                        attachments_file = file_structure.get_attachments_for_card_json_file(board_id, card["id"])
                        attachment_json = file_system.read_file_json(attachments_file)

                        for attachment in attachment_json:
                            if id_attachment_cover == attachment["id"]:
                                board_card.attachments.insert(0, attachment["fileName"])
                            else:
                                board_card.attachments.append(attachment["fileName"])

                    # Add Checklists
                    for checklist_id in card["idChecklists"]:
                        checklist_filename = file_structure.get_checklist_json_file(board_id, checklist_id)
                        checklist = file_system.read_file_json(checklist_filename)
                        
                        newChecklist = Checklist(checklist["name"])
                        
                        for item in checklist["checkItems"]:
                            checked_state = bool(item["state"] == "complete")
                            newChecklist.items.append(ChecklistItem(item["name"], checked_state))
                            
                        if newChecklist.items:
                            board_card.checklists.append(newChecklist)
                            
                    board_list.cards.append(board_card)
                    
            board.lists.append(board_list)
            
        # Labels with their name and color
        for label in labels_json:
            label_name = self._get_label_name(label["id"], labels_json)            
            
            # Fixes a trello bug. Colors named dark are actually light, and colors named light should be dark!
            color_name = label["color"]
            
            if color_name.endswith("_dark"):
                color_name = color_name.replace("_dark", "_light")
            elif color_name.endswith("_light"):
                color_name = color_name.replace("_light", "_dark")
                
            board.labels.append(Label(label_name, color_name))
            
        return board
        
    
    def _create_markdown_file(self, board: Board):
        """
        Create a Markdown file representing the given Trello board.

        Parameters:
            board (Board): The Board object representing the Trello board.
        """
        # Add header
        text = "---\n\nkanban-plugin: basic\n\n---\n"
        
        for board_list in board.lists:
            # Add List
            text += f"\n\n## {board_list.title}\n\n"
            
            # Add Card to the list
            for card in board_list.cards:
                card_text = "- [ ] "
                
                # Add labels
                if card.labels:
                    for label in card.labels:
                        card_text += f"<br>#{label} "
                        
                    card_text += "<br>"
                                                    
                # Add Attachments
                if card.attachments:
                    card_text += "<br>"
                                        
                    cover_filename: str = ""
                    hidden_attachments_filenames: List[str] = []
                                                            
                    for index, attachment_filename in enumerate(card.attachments):                                                    
                        # Using relative pathing ./attachments/somefile.jpg
                        filename = os.path.join(".", file_structure.ATTACHMENTS_FOLDER, attachment_filename)
                        
                        if index == 0:
                            cover_filename = filename
                        else:
                            hidden_attachments_filenames.append(filename)

                    card_text += f"![[{cover_filename}]]<br>"
                    
                    for filename in hidden_attachments_filenames:
                        card_text += f"![[{filename}]]<br>"                    
                
                card.title = self._fix_hashtags_in_text(card.title)
                card.description = self._fix_hashtags_in_text(card.description)
                
                # Add Card Title
                if card.description:
                    card_text += f"<details><summary>{card.title}</summary> <br>{card.description}</details>"
                else:
                    card_text += card.title

                # Add Checklists
                if card.checklists:
                    card_text += "<br>"
                    
                    for checklist in card.checklists:
                        card_text += f"   <br><u>{self._fix_hashtags_in_text(checklist.title)}:</u><br>"
                        
                        for item in checklist.items:
                            if item.checked:
                                card_text += "- [X] "
                            else:
                                card_text += "- [ ] "
                                
                            card_text += f"{self._fix_hashtags_in_text(item.text)}<br>"
                        
                        card_text += "<br>"
                
                text += card_text + "\n"                
        
        
        text += self._create_kanban_settings(board)
        
        # Export to file
        board_filename = os.path.join(file_structure.get_board_folder(board.board_id), f"{board.title}.md")
        print("Exporting to " + board_filename)
        file_system.write_file(board_filename, text)
        
    
    def _create_kanban_settings(self, board: Board) -> str:
        """
        Create kanban settings (for Obsidian Kanban) for the given board.

        Args:
            board (Board): The board for which to create kanban settings.

        Returns:
            str: Kanban settings in markdown format.
        """
        
        kanban_settings = {
            "kanban-plugin": "basic",
            "tag-colors": [],
            "hide-tags-display": False,
            "hide-tags-in-title": True
        }

        # Add Label Definitions
        for label in board.labels:
            tag_color = {
                "tagKey": f"#{label.title}",
                "color": self._get_text_color(label.color_name),
                "backgroundColor": self._get_background_color(label.color_name)
            }
            
            if not label.title:
                tag_color["color"] = tag_color["backgroundColor"]
            
            kanban_settings["tag-colors"].append(tag_color)
            
        return f"\n%% kanban:settings\n```\n{json.dumps(kanban_settings)}\n```\n%%\n"
    
    
    def _fix_hashtags_in_text(self, description: str) -> str:
        """
        Fix hashtags in the description to prevent Obsidian Kanban from interpreting them as labels.

        Parameters:
            description (str): The description string to fix.

        Returns:
            str: The modified description string.

        This function inserts an invisible character "&#8203" before hashtags not followed by a space in the description string.
        """
        # Go from back to front
        for i in range(len(description) - 1, -1, -1):            
            current_char = description[i]
        
            if current_char == '#' and i + 1 < len(description) and description[i + 1] != ' ':
                description = insert_char("&#8203", description, i)
                        
        return description
    
    
    def _get_text_color(self, color_name: str) -> str:
        """
        Determines the appropriate text color based on the background color.

        Args:
            color_name (str): The name of the background color. Expected to end with "_light" for light 
                                background colors; otherwise, assumes a dark background color.

        Returns:
            str: The RGBA color string representing the appropriate text color for the given background color.
        """
        # If the background is too bright we want a dark color
        if color_name.endswith("_light"):
            return self._get_rgba(*set_color_brightness((255, 255, 255), 0.1))
        else:
            return self._get_rgba(*set_color_brightness((255, 255, 255), 0.95))
        
        
    def _get_background_color(self, color_name: str) -> str:
        """
        Get the RGBA color value for the specified color name.

        Args:
            color_name (str): The name of the color to retrieve.

        Returns:
            str: The RGBA color value in the format "rgba(red, green, blue, 1)".
            
        Note:
            If the specified color name is not supported, the default RGBA color value is black.
        """        
        if color_name in self.color_values:
            red, green, blue = self.color_values[color_name]
            return self._get_rgba(red, green, blue)
        else:
            print(f"ERROR: Color not found [{color_name}]")
            # Default to black for undefined colors
            return self._get_rgba(0, 0, 0)
      
      
    def _get_rgba(self, red: int, green: int, blue: int, alpha: int = 1) -> str:
        """
        Generate an RGBA color string from the provided red, green, and blue values.

        Args:
            red (int): The red component of the color (0-255).
            green (int): The green component of the color (0-255).
            blue (int): The blue component of the color (0-255).

        Returns:
            str: An RGBA color string in the format 'rgba(red, green, blue, 1)'.
        """
        return f"rgba({red}, {green}, {blue}, {alpha})"
    
    
    def _get_label_name(self, label_id: str, labels_json: Any) -> str:
        """
        Retrieve the name of a label based on its ID.

        Args:
            label_id (str): The ID of the label to retrieve the name for.
            labels_json (Any): A (json) list of label objects retrieved from Trello.

        Returns:
            str: The name of the label corresponding to the provided ID.
        """
        for label in labels_json:
            if label["id"] == label_id:
                label_name:str = label["name"].replace(' ', '') # Also removes spaces

                # As a fallback: Use the color name if this label has no name
                if not label_name:
                    return label["color"]

                return label_name
