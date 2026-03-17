
from boto3 import client

bedrock = client("bedrock-runtime")

# bedrock.invoke_model(...) #send a request. like client.send(command)
# in js, it would be: InvokeModelCommand
# Params: modelId="anthropic.claude-3-sonnet" and body="...."
# for model id: 
# for body: { "prompt": "...", "ideas": [{"topic": <>, "message": "...",}, ... ], "max_tokens":... }

#1. Query Django model
# Iterate over instances in idea table for batch processing
# Idea.objects.all().iterator(chunk_size=50)

#2. Serialize instances into structured JSON list
# {
# "ideas":[
# {"id": 1, "topic": "<topic", "location": "<location>", "message": "<message>"}, ...
#],
# "limited_choices": "topic"}

#Prompt(chunk): "Identify topics that have a relatively high level of representation in the subdataset"
#Prompt(chunk): "Identify recurring themes and overlapping ideas in message"
#Prompt(chunk): "Flag any items that appear urgent or are important and time sensitive. Explain why"
#Prompt(final): "Combine the fequency patterns for topic from all chunk summaries to identify global trends"
#Prompt(final): "Combine the themes from all chunk summaries and identify the strongest cross-dataset patterns"
#Prompt(final): "Summarize all urgent items across the dataset and highlight the most critical issues"


#3. Send JSON to AWS Bedrock in a single prompt
#4. Store the summary in a JSON
#5. Repeat until no more instances
#6. send the summary JSON for final summary

