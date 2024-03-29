from typing import List, Any

"""
    Board:
        - Lists
            - Cards
                - Name
                - Description
                - Labels
                - Attachments
                - Checklists
                    - ChecklistItems
        
        - List of all defined Labels
"""

class Board:
    def __init__(self, board_id: str, title: str) -> None:
        self.board_id: str = board_id        
        self.title: str = title
        self.lists: List[BoardList] = []
        self.labels: List[Label] = []


class BoardList:
    def __init__(self, id: str, title: str) -> None:
        self.id: str = id
        self.title: str = title
        self.cards: List[Card] = []        


class Card:
    def __init__(self, card_id: str, title: str, description: str) -> None:
        self.card_id: str = card_id
        self.title: str = title
        self.description: str = description
        self.labels: List[str] = []
        self.attachments: List[str] = []
        self.checklists: List[Checklist] = []
        
        
class Checklist:
    def __init__(self, title: str) -> None:
        self.title: str = title
        self.items: List[ChecklistItem] = []
        

class ChecklistItem:
    def __init__(self, text: str = "", checked: bool = False) -> None:
        self.checked: bool = checked
        self.text: str = text
        

class Label:
    def __init__(self, title: str, color_name: str) -> None:
        self.title: str = title
        self.color_name: str = color_name

