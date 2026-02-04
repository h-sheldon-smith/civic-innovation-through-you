from django.db import models
from common.choices import Topic_Options, TOPIC_MAX_LENGTH

# Create your models here (db)
# Classes/models represent tables in a DB
# Attributes = fields

# class Name(models.Model):
class Idea(models.Model):
    # field_name = models.TypeOfField(optional_constraints = some_value)
    subject_line = models.CharField(max_length = 50, blank = False)
    location = models.CharField(max_length = 50)

    #for our defined options, put in common.options and import it to the model
    topic = models.CharField(max_length = TOPIC_MAX_LENGTH, choices = Topic_Options.choices)
    message = models.CharField(max_length = 500, blank = False)
    time_stamp = models.DateTimeField()
    read_status = models.BooleanField()
