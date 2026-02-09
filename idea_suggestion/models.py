from django.db import models
from common.models import User
from common.choices import Topic_Options, TOPIC_MAX_LENGTH, IDEA_FOLDERS, IDEA_FOLDERS_MAX_LENGTH

# Create your models here (db)
# Classes/models represent tables in a DB
# Attributes = fields

# class Name(models.Model):
class Idea(models.Model):
    # using another model as an attribute in this model
    resident = models.ForeignKey(
        User,
        on_delete = models.SET_NULL, # keep the idea even if the user is deleted
        null = True,
        related_name = 'ideas' # lets you look up all ideas by the given resident
    )

    # field_name = models.TypeOfField(optional_constraints = some_value)
    subject_line = models.CharField(max_length = 50, blank = False)
    location = models.CharField(max_length = 50)

    #for our defined options, put in common.options and import it to the model
    topic = models.CharField(max_length = TOPIC_MAX_LENGTH, choices = Topic_Options.choices)
    message = models.CharField(max_length = 1000, blank = False)
    time_stamp = models.DateTimeField(auto_now_add = True, editable = False)
    read_status = models.BooleanField(default = False)
    file_location = models.CharField(max_length = IDEA_FOLDERS_MAX_LENGTH, 
                                     choices = IDEA_FOLDERS)
    
    # Method to print idea objects as a formatted string
    def __str__(self):
        return (f"From: {self.resident.user_name}, Subject: {self.subject_line}")