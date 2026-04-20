from . import Convert_Data, Batch_Data, Send_Message, BATCH_SIZE, CONSOLIDATE_TASK

'''
Method to orchestrate processing raw data and receive AI insights
Access point for other apps
Param: task, the instructions for the AI model
       format, the desired output format
       data, the data to be processed by the model
Returns: the processed data from the ai model
'''

def Ask_AI(task, format, data):
    task_string = Convert_Data(task) + Convert_Data(format)
    batched_data, data_count = Batch_Data(BATCH_SIZE, data, task_string) #gets initial data batches in string format

    responses = [] #summary for each batch

    for index, batch in enumerate(batched_data):
        prompt = f"[METADATA] count: {data_count[index]} [CONTENT] " + batch
        responses.append(Send_Message(prompt))

    #Now we need to combine the responses...
    while len(responses) > 1:
        batches, counts = Batch_Data(BATCH_SIZE, responses, CONSOLIDATE_TASK)
        responses = []
        for index, batch in enumerate(batches):
            prompt = f"[METADATA] count: {counts[index]} [CONTENT] " + batch
            responses.append(Send_Message(prompt))
    
    return responses[0]