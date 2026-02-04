from __future__ import annotations # forward refereence
from domain.business_rule_results import RateResult, ActionResult
from domain.user import user
from domain.action import action

from abc import ABC, abstractmethod



'''
Defines the contract for managing the idea submission backend Service Layer 
enforcing business rules for input functionality
'''
class IdeaServiceBusinessRuleEnforcer(ABC):



    '''
    Checks if an action is allowed based on the user's permissions
    Args: a_user (user): the user who is trying to perform an action
          an_action (action): the action the user is trying to perform
    Returns: ActionResult: Indicates success or failure and the reason why it failed
    '''
    @abstractmethod
    def check_permission(self, a_user: user, an_action:action) -> ActionResult:
        pass


    '''
    Checks if an action is allowed based on a rate result
    Args: a_user (user): the user who is trying to perform an action
         an_action (action): the action they are trying to perform
    Returns: RateResult: Indicates success or failure and the reason why it failed
    '''
    @abstractmethod
    def check_rate_limit(self, a_user: user, an_action:action) -> RateResult:
        pass


     