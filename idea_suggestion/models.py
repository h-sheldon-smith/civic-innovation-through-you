from django.db import models
from django.contrib.auth.models import User
from common.choices import Topic_Options, TOPIC_MAX_LENGTH, IDEA_FOLDERS, IDEA_FOLDERS_MAX_LENGTH

class Idea(models.Model):
    # Add User as a foreign key
    resident = models.ForeignKey(
       User,
       default = None,
       on_delete = models.SET_NULL, # keep the idea even if the user is deleted
       null = True,
       related_name = 'ideas' # lets you look up all ideas by the given resident
    )

    subject_line = models.CharField(max_length = 50, 
                                    blank = False)
    location = models.CharField(max_length = 50)

    topic = models.CharField(max_length = TOPIC_MAX_LENGTH, 
                             choices = Topic_Options.choices)

    message = models.TextField(blank = False, 
                               max_length=2000)

    picture = models.ImageField(
        upload_to='ideas/',
        blank = True,
        null = True,
        default = None
        )
    
    # these fields will auto populate values to follow default or current time once an instance is created
    time_stamp = models.DateTimeField(auto_now_add = True, 
                                      editable = False)
    read_status = models.BooleanField(default = False)
    file_location = models.CharField(max_length = IDEA_FOLDERS_MAX_LENGTH, 
                                     choices = IDEA_FOLDERS,
                                     default = "Inbox")
    
    # Method to print idea objects as a formatted string
    def __str__(self):
        display_resident = self.resident.username if self.resident is not None else self.resident
        formatted_time = self.time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        return (f"Topic: {self.topic}, "
                f"From: {display_resident}, "
                f"Subject: {self.subject_line}, "
                f"Time: {formatted_time}")
    
    # Method to get the resident who submitted the idea
    def get_resident(self):
        return self.resident.username if self.resident is not None else self.resident