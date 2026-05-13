from .converters import Convert_Data

'''
Method to create batches of data for AI processing
Param: batch_size, the max char length for the batch
Param: data, the data to be separated in batches
Param: task, the instructions for AI processing
Returns: all_batches, a nested list with batched data strings
Returns: data_count, a list of data objects per batch for weighting batche outputs when later combined
'''

def Batch_Data(batch_size, data, task, exclude):
    all_batches = []
    batch = ""
    batch_weight = []
    count = 0

    # If there is no data, return empty lists
    if not data:
        return all_batches, batch_weight

    # Batch data
    else:
        batch = task + " "

        for d in data:
            data_string = Convert_Data(d, exclude)
                
            # If there's room in the batch, add it to the current batch
            if (len(batch) + len(data_string)) < batch_size:
                batch = batch + data_string
                count = count + 1

            # If the current batch is full, add it to the collection of batches and start a new batch
            else:
                batch_weight.append(count)
                count = 1
                all_batches.append(batch)
                batch = task + " " + data_string

        # Process the final outstanding batch
        all_batches.append(batch)
        batch_weight.append(count)

    return all_batches, batch_weight