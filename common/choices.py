from django.db import models

class Topic_Options(models.TextChoices):
    ART = 'Art', 'Arts & Culture'
    BUSINESS = 'Bus', 'Business'
    CHILD = 'Child', 'Childcare & Youth Programs'
    CONSTRUCTION = 'Construction', 'Construction'
    EVENTS = 'Events', 'Community Events'
    GOV = 'Gov', 'Local Government'
    HEALTH = 'Health', 'Health & Community Services'
    HOUSE = 'House', 'Housing & Development'
    PARKS = 'Parks', 'Parks & Green Spaces'
    PLAN = 'Plan', 'Urban Planning'
    SAFE = 'Safe', 'Public Safety'
    SENIOR = 'Senior', 'Senior Services'
    TRANSPORT = 'Transport', 'Transportation & Infrastructure'
    VOLUNTEER = "Volunteer", "Volunteering Opportunities"

TOPIC_MAX_LENGTH = max(len(Topic_Options.value) for choice in Topic_Options)
   