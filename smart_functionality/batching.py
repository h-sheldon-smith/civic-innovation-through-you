from .converters import Convert_Data

'''
Method to create batches of data for AI processing
Param: batch_size, the max char length for the batch
Param: data, the data to be separated in batches
Param: task, the instructions for AI processing
Returns: all_batches, a nested list with batched data strings
Returns: data_count, a list of data objects per batch for weighting batche outputs when later combined
'''

def Batch_Data(batch_size, data, task):
    all_batches = []
    batch = []
    batch_char_count = []

    # If there is no data, return empty lists
    if data.count() == 0:
        return all_batches, batch_char_count

    # Batch data
    else:
        batch.append(task)
        count = 0

        for d in data:
            data_string = Convert_Data(d)
                
            # If there's room in the batch, add it to the current batch
            if len(batch) < batch_size:
                batch.append(data_string)
                count += len(data_string)

            # If the current batch is full, add it to the collection of batches and start a new batch
            else:
                batch_char_count.append(count)
                count = 0
                all_batches.append(batch)
                batch = []
                batch.append(task, data_string)

        # Process the final outstanding batch, if it exists
        if len(batch) == len(task):
            return all_batches, batch_char_count
        else:
            all_batches.append(batch)
            batch_char_count.append(count)

    return all_batches, batch_char_count