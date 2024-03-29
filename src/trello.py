import requests
from typing import Optional, Any, Tuple

# Trello API
# https://developer.atlassian.com/cloud/trello/rest/


class Trello:
    def __init__(self, api_key: str, api_token: str) -> None:
        """
        Set up a Trello instance using the supplied API key and API token.

        Args:
            api_key (str): The API key used for authentication with Trello.
            api_token (str): The API token used for authentication with Trello.
        """
        self.api_key = api_key
        self.api_token = api_token
        

    def get_boards(self) -> Optional[Any]:
        """
        Retrieve the boards associated with the authenticated user.

        Returns:
            Any: A dictionary containing the JSON response from the Trello API, or None if the request fails.
        """
        response = self._execute_get_request("/members/me/boards")
        
        if response.status_code == 200:
            return response.json()

        return None
    

    def get_board(self, board_id: str) -> Optional[Any]:
        """
        Retrieve information about a Trello board using its ID.

        Args:
            board_id (str): The ID of the Trello board.

        Returns:
            Optional[Any]: The JSON representation of the board if the request is successful,
                        or None if the request fails.
        """
        response = self._execute_get_request(f"/boards/{board_id}")
        
        if response.status_code == 200:
            return response.json()
        
        return None
    

    def get_lists(self, board_id: str) -> Optional[Any]:
        """
        Retrieve information about all lists in a Trello board.

        Args:
            board_id (str): The ID of the Trello board.

        Returns:
            Optional[Any]: The JSON representation of the lists if the request is successful,
                        or None if the request fails.
        """
        response = self._execute_get_request(f"/boards/{board_id}/lists")

        if response.status_code == 200:
            return response.json()

        return None
    

    def get_list(self, list_id: str) -> Optional[Any]:      
        """
        Retrieve information about a specific Trello list using its ID.

        Args:
            list_id (str): The ID of the Trello list.

        Returns:
            Optional[Any]: The JSON representation of the list if the request is successful,
                        or None if the request fails.
        """
        response = self._execute_get_request(f"/lists/{list_id}")

        if response.status_code == 200:
            return response.json()
        
        return None
    
    
    def get_labels(self, board_id: str) -> Optional[Any]:
        """
        Retrieve information about all labels in a Trello board.

        Args:
            board_id (str): The ID of the Trello board.

        Returns:
            Optional[Any]: The JSON representation of the labels if the request is successful,
                        or None if the request fails.
        """
        response = self._execute_get_request(f"/boards/{board_id}/labels")
        
        if response.status_code == 200:
            return response.json()

        return None
    
    
    def get_checklist(self, checklist_id: str) -> Optional[Any]:
        """
        Retrieve information about a specific Trello checklist using its ID.

        Args:
            checklist_id (str): The ID of the Trello checklist.

        Returns:
            Optional[Any]: The JSON representation of the checklist if the request is successful,
                        or None if the request fails.
        """
        response = self._execute_get_request(f"/checklists/{checklist_id}")

        if response.status_code == 200:
            return response.json()
    
        return None

    
    def get_all_cards(self, board_id: str) -> Optional[Any]:
        """
        Retrieve information about all cards in a Trello board.

        Args:
            board_id (str): The ID of the Trello board.

        Returns:
            Optional[Any]: The JSON representation of the cards if the request is successful,
                        or None if the request fails.
        """
        response = self._execute_get_request(f"/boards/{board_id}/cards")

        if response.status_code == 200:
            return response.json()
        
        return None

    
    def get_attachments(self, card_id: str) -> Optional[Any]:      
        """
        Retrieve information about all attachments on a Trello card.

        Args:
            card_id (str): The ID of the Trello card.

        Returns:
            Optional[Any]: The JSON representation of the attachments if the request is successful,
                        or None if the request fails.
        """
        # https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-id-attachments-get
        response = self._execute_get_request(f"/cards/{card_id}/attachments")

        if response.status_code == 200:
            return response.json()
        
        return None

        
    def download_attachment(self, attachment_url: str, filename: str) -> bool:        
        """
        Download an attachment from a Trello card.

        Args:
            attachment_url (str): The URL of the attachment to download.
            filename (str): The name of the file to save the attachment to.
            
        Returns:
            bool: True if the download is successful, False otherwise.
        """        
        headers = {
            'Authorization': f'OAuth oauth_consumer_key="{self.api_key}", oauth_token="{self.api_token}"'
        }
        
        # TODO: HANDLE EXTERNAL LINKS?!
        response = requests.get(attachment_url, headers=headers)
        
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
                
            return True
        else:
            print(f"ERROR downloading Attachment [{response.status_code}]")
            print(f"   {response.url}")
            
            return False
        
    
    def get_board_id_from_url(self, url: str) -> Optional[str]:
        """
        Get the board ID from the given Trello board URL.

        Args:
            url (str): The URL of the Trello board.

        Returns:
            Optional[str]: The ID of the Trello board if found, otherwise None.
        """
        url = f"{url}.json" # adding .json to get to the json file of the board
        _, headers, params = self._create_get_request("")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:                        
            try:
                json_response = response.json()
            
                if "id" in json_response:
                    return json_response["id"]
            except requests.exceptions.JSONDecodeError:
                pass
        
        return None
        
    
    def _create_get_request(self, url_path: str) -> Tuple[str, str, str]:        
        """
        Create a GET request with the specified URL path.

        Args:
            url_path (str): The path for the GET request.

        Returns:
            Tuple[str, str, str]: A tuple containing the URL, headers, and parameters for the request.
        """
        BASE_URL = "https://api.trello.com/1"
        #url = f"{BASE_URL}/members/me/boards"
        url = BASE_URL + url_path

        headers = {"Accept": "application/json"}      
        params = {
            'key': self.api_key,
            'token': self.api_token
        }
        
        # Only if there is a api_key and api_token available
        if self.api_key and self.api_token:
            return (url, headers, params)
        else:
            return (url, headers, "{}")


    def _execute_get_request(self, url_path:str) -> requests.Response:
        """
        Execute a GET request with the specified URL path.

        Args:
            url_path (str): The path for the GET request.

        Returns:
            requests.Response: The response object from the GET request.
        """
        url, headers, params = self._create_get_request(url_path)
        return requests.get(url, headers=headers, params=params)