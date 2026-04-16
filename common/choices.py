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
    VOLUNTEER = 'Volunteer', 'Volunteering Opportunities'

TOPIC_MAX_LENGTH = max(len(choice.value) for choice in Topic_Options)

IDEA_FOLDERS = [('Inbox', 'Inbox')] + list(Topic_Options.choices)

IDEA_FOLDERS_MAX_LENGTH = max(len(value) for value, _ in IDEA_FOLDERS)

class Account_Status(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'
    SUSPENDED = 'Suspended', 'Suspended'
    BANNED = 'Banned', 'Banned'

ACCT_STATUS_MAX_LENGTH = max(len(choice.value) for choice in Account_Status)