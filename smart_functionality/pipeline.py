from .converters import Convert_Data
#from .batching import Batch_Data
from . import batching
from . import client
from smart_functionality.constants import BATCH_SIZE, CONSOLIDATE_TASK, CONSOLIDATE_FORMAT, AI_HARD_LIMIT

'''
Method to orchestrate processing raw data and receive AI insights
Access point for other apps
Param: task, the instructions for the AI model
       format, the desired output format
       data, the data to be processed by the model
Returns: final_response (list), the consolidated output message(s) from ai. 
         May contain multiple messages depending on size of input.
'''

# MAYBE ADD AN EXLUDE PARAM and update converter
def Ask_AI(task, format, data):
    batched_data, data_count = Get_Batches(task, format, data, BATCH_SIZE)
    responses = Query_AI(batched_data, data_count)
    final_response, loops = Consolidate_Responses(responses, BATCH_SIZE)
    
    return final_response

'''
Method to split input into batches for ai processing
Param: task (string), the instructions for the AI model
       format (string), the desired output format
       data (primitives or model instances), the data to be processed by the model
       batch_size (int), the length of a single batch
Returns: batched_data (list of strings), the input split into batches
         data_weight (list of int), the number of inputs per batch (used for weighting during consolidation)
'''
def Get_Batches(task, format, data, batch_size):
    task_string = Convert_Data(task) + Convert_Data(format)
    batched_data, data_weight = batching.Batch_Data(batch_size, data, task_string)

    return batched_data, data_weight

'''
Method to consolidate ai responses to data batches
Param: data, the response batches
       batch_size (int), the length of a single batch
Returns: response (list of strings), the ai model's response
         loops (int), the number of times consolidation was run
'''
def Consolidate_Responses(data, batch_size):
    loops = 0
    responses = data

    while len(responses) > 1 and loops < AI_HARD_LIMIT:
        batches, weights = Get_Batches(CONSOLIDATE_TASK, CONSOLIDATE_FORMAT, responses, batch_size)
        responses = Query_AI(batches, weights)
        loops = loops + 1

    return responses, loops

'''
Method to for the prompts and send for ai query
Param: batches (list of strings), the contents to be queried
       weights (list of int), the weight for the given batch
Returns: response (list of strings), the ai model's responses
'''
def Query_AI(batches, weights):

    responses = []
    loops = 0

    for index, batch in enumerate(batches):
        prompt = "[METADATA] count: " + str(weights[index]) + " [CONTENT] " + batches[index]
        responses.append(client.Send_Message(prompt))
        if loops >= AI_HARD_LIMIT:
            #TODO: add the remaining, unprocessed batches to responses... or just drop them.
            break

    return responses
