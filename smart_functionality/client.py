import anthropic
import os
from .constants import RESPONSE_TOKENS

'''
Method to consult AI about a given dataset
Param: prompt, the instructions and dataset to be sent to AI for processing
Return: the AI model's response, based on the prompt 
'''
def Send_Message(prompt):
    client = anthropic.Anthropic(api_key = os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        max_tokens = RESPONSE_TOKENS,
        messages= [{
            "role":"user",
            "content":prompt}],
        model = "claude-sonnet-4-6" # check this
    )

    #response = "TEST RESPONSE: Full implementation and anthropic call pending."
    #return response

    return response.content[0].text if response else "Unable to reach AI at this time"