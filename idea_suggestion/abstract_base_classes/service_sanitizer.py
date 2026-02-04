from abc import ABC, abstractmethod

'''
Defines the contract for managing the idea submission backend Service Layer sanitizing input functionality
'''
class IdeaServiceSanitizer(ABC):

    '''
    Removes scripts from user input to prevent injection attacks and cross-site scripting
    (eg: <script>alert("Hacked!")</script> becomes harmless: alert("Hacked!"))
    (eg: <img src="x" onerror="stealCookies()"> becomes <imag src="x">)
    NOTE: Do this first
    Args: input_value (str): the value to be sanitized
    Returns: str: the sanitized value
    '''
    @abstractmethod
    def remove_scripts(self, input_value: str) -> str:
        pass


    '''
    Strips HTML tags/mark ups from user input to prevent cross-site scripting and UI breaks
    (eg: <tag>Hello</tag> becomes Hello)
    NOTE: Does not reliably remove scripts. Do this second.
    Args: input_value (str): the value to be sanitized
    Returns: str: the sanitized value
    '''
    @abstractmethod
    def strip_html(self, input_value: str) -> str:
        pass


    '''
    Add escapes for dangerous characters
    (eg: \t becomes \\t, " becomes \")
    Args: input_value (str): the value to be sanitized
    Returns: str: the sanitized value
    '''
    @abstractmethod
    def add_escape_chars(self, input_value: str) -> str:
        pass

    '''
    Removes extra white spaces
    Args: input_value (str): the value to be sanitized
    Returns: str: the sanitized value
    '''
    @abstractmethod
    def normalize_white_sapces(self, input_value: str) -> str:
        pass

