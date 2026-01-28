from abc import ABC, abstractmethod

'''
Defines the contract for managing the idea submission API Service (Network)
including building requests, sending infomration to the backend, and parsing backend responses
'''
class IdeaAPIService(ABC):

    '''
    Builds a request object to be sent to the backend
    Args: payload (dict): the validated and sanitized payload to be sent
    Returns: dict: the request object to be sent
    '''
    @abstractmethod
    def build_request(self, payload: dict) -> dict:
        pass


    '''
    Sends the payload to the backend
    Returns a status message
    Args: payload (dict): the payload to be sent
    Returns: str: a message indicating the success or failure of sending
    '''
    @abstractmethod
    def send_to_backend(self, payload: dict) -> str:
        pass


    '''
    Parses responses from backend and extracts a natural language message
    Args: response (dict): the response from the backend to be parsed
    Returns: str: a message indicating sending success or failure
    '''
    @abstractmethod
    def parse_response(self, input_value: str) -> str:
        pass