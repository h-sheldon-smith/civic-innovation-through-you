from abc import ABC, abstractmethod

'''
Defines the contract for managing the idea submission Form State (Logic)
including validating and preparing user input for idea submission.
'''
class IdeaFormState(ABC):

    '''
    Validates a dictionary of user inputs
    Args: input (dict): a dictionary containing input controls identifiers 
                        to their correpsonding user provided input values
    Returns: bool: true if all values are valid, otherwise false
    '''
    @abstractmethod
    def validate_user_input(self, input: dict) -> bool:
        pass


    '''
    Validates a single input entry.
    Updates error log if the entry is not valid.
    Args: input_id (str): the identifier associated with an entry
          input_value (str): the value associated with the entry 
    '''
    @abstractmethod
    def update_user_input_helper(self, input_id: str, input_value: str):
        pass


    '''
    Adds an error for the given input control
    Args: input_id (str): the identifier of the input control
          input_value (str): the value associated with the control
    '''
    @abstractmethod
    def add_error(self, input_id: str, input_value: str):
        pass


    '''
    Gets error log
    Returns: dict: An error log mapping input control identifiers to their associated errors, 
                   or None if errors aren't present
    '''
    @abstractmethod
    def get_errors(self) -> dict | None:
        pass


    '''
    Removes all entries from the error log
    '''
    @abstractmethod
    def clear_errors(self):
        pass


    '''
    Generates final payload to be sent to the backend
    Returns: dict: validated user input if no errors are present
                   or an error log mapping error messages with input controls if errors are present
    '''
    @abstractmethod
    def build_payload(self) -> dict:
        pass


