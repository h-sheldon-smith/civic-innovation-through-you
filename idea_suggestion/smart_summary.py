from idea_suggestion.models import Idea
from smart_functionality.pipeline import Ask_AI
from idea_suggestion.admin_inbox_services import Admin_Mark_Read

INBOX_SUMMARY_TASK = "Analyze the provided community feedback and produce the following:" \
"A summary of the most common themes and ideas (e.g. suggestions for improving the community, concerns, or complaints)," \
"Specific callouts for urgent issues that impacts safety or community/municipality finances," \
"Identify any patterns or trends (e.g. time of events, locations, people involved or impacted)" \

INBOX_SUMMARY_FORMAT = "Make a written summary with key insights in bullet points and anything urgent seperate and at the top." \
"Keep everything within 3000 characters. Avoid sounding like generic AI, using technical terms, or overly formal language."


'''
Method to get a smart summary for unread inbox contents
If successful, marks the ideas as read
Returns: a smart summary of inbox contents if successful
         otherwise, a failure message
'''
def Get_Smart_Inbox_Summary():
    ideas = Idea.objects.all().filter(read_status='unread')
    summary = Ask_AI(INBOX_SUMMARY_TASK, INBOX_SUMMARY_FORMAT, ideas)

    #if we get a summary back, we should mark the ideas as read
    if summary:
        Admin_Mark_Read(ideas)
        return summary
    else:
        return "smart summary is not available at this time"