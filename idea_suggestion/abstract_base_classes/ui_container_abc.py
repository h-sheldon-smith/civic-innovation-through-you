from abc import ABC, abstractmethod

'''
Defines the contract for managing the idea submission UI
including orchestrating user input and displaying results to user
'''
class IdeaUI(ABC):

    '''
    Toggles the visiblity state of the UI between shown and hidden
    '''
    @abstractmethod
    def switch_view(self):
        pass

    '''
    Updates internally stored user input data
    Args: input_id (str): the identifier associated with an entry
          input_value (str): the value associated with the entry 
    '''
    @abstractmethod
    def update_user_input(self, input_id: str, input_value: str):
        pass


    '''
    Gets the stored input value for a specific input control
    Args: input_id (str): identifier assciated with the input control
    Returns: str: the input value stored for the given input control
    '''
    @abstractmethod
    def get_user_input(self, input_id: str) -> str:
        pass


    '''
    Sends user input data to be validated and sanitized, then passes to backend
    '''
    @abstractmethod
    def send_user_input(self):
        pass


    '''
    Displays messages to user
    '''
    @abstractmethod
    def display_message(self, message: str):
        pass

