from abc import ABC, abstractmethod
from typing import Callable

'''
Defines the contract for user input controls
including displaying prompts and retrieving data
'''
class InputControl(ABC):

    '''
    Sets an identifier for the input control
    Args: control_id (str): the identifier for the input control
    '''
    @abstractmethod
    def set_id(self, control_id: str):
        pass


    '''
    Gets an identifier for the input control
    Returns: str: the identifier for the input control
    '''
    @abstractmethod
    def get_id(self) -> str:
        pass


    '''
    Sets a user prompt for the input control
    Args: prompt (str): the user prompt for the input control
    '''
    @abstractmethod
    def set_prompt(self, prompt: str):
        pass


    '''
    Gets a user prompt for the input control
    Returns: str: the user prompt for the input control
    '''
    @abstractmethod
    def get_prompt(self) -> str:
        pass


    '''
    Sets a user input for the input control
    Triggers emit_on_change function
    Args: user_input (str): the user prompt for the input control
    '''
    @abstractmethod
    def set_user_input(self, user_input: str):
        pass


    '''
    Gets a current input for the input control
    Return: str: the user input for the input control
    '''
    @abstractmethod
    def get_user_input(self) -> str:
        pass


    '''
    Registers a callback to be invoked when user input value changes
    Args: callback: a function to send data to when the data is updated
          callback requires the control identifier and the user input value as arguments
          callback does not issue a return
    '''
    @abstractmethod
    def set_on_change_callback(self, callback: Callable[[str, str], None]):
        pass


    '''
    Emits a change event indicating that the control's value has been updated.
    Notifies listeners/triggers UI updates
    '''
    @abstractmethod
    def emit_on_change(self):
        pass