#Instructions for consolidating batches
CONSOLIDATE_TASK = "Combine the following information into one consolidated document." \

CONSOLIDATE_FORMAT = "Preserve the overall structure, format, and meaning of the input data."
"Weight each section of input according to the given data counts."

#Batches sized by characters
BATCH_SIZE = 8000

#How many tokens the model is allowed to respond with (1 token = 4 char)
RESPONSE_TOKENS = 1024

AI_HARD_LIMIT = 5