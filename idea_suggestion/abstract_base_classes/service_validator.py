from __future__ import annotations # forward refereence
from domain.validation_rules import validation_rule
from domain.validation_results import LengthValidationResult, ValueValidationResult, RequirementStatValidationResult

from abc import ABC, abstractmethod

'''
Defines the contract for managing the idea submission backend Service Layer validation functionality
'''
class IdeaServiceValidator(ABC):

    '''
    Checks the length of user input against its length requirement rule
    Args: input_value (str): the user provided input
          rule (str): the requirements for the input
    Returns: LengthValidationResult (enum): the result for length validation 
                                            including details about failures, when applicable
    '''
    @abstractmethod
    def check_input_length(self, input_value: str, rule: validation_rule) -> LengthValidationResult:
        pass


    '''
    Checks the value of user input against its value requirement rule
    Args: input_value (str): the user provided input
          rule (str): the requirements for the input
    Returns: ValueValidationResult (enum): the result for length validation 
                                            including details about failures, when applicable
    '''
    @abstractmethod
    def check_input_value(self, input_value: str, rule: validation_rule) -> ValueValidationResult:
        pass


    '''
    Checks if user input exists against its requirement rule
    Args: input_value (str): the user provided input
          rule (str): the requirements for the input
    Returns: RequirementStatValidationResult (enum): the result for length validation 
                                            including details about failures, when applicable
    '''
    @abstractmethod
    def check_input_required(self, input_value: str, rule: str) -> RequirementStatValidationResult:
        pass


