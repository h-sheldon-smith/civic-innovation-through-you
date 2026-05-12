from django.db import models

class Topic_Options(models.TextChoices):
    ART = 'Arts & Culture', 'Arts & Culture'
    BUSINESS = 'Business', 'Business'
    CHILD = 'Childcare & Youth Programs', 'Childcare & Youth Programs'
    CONSTRUCTION = 'Construction', 'Construction'
    EVENTS = 'Community Events', 'Community Events'
    GOV = 'Local Government', 'Local Government'
    HEALTH = 'Health & Community Services', 'Health & Community Services'
    HOUSE = 'Housing & Dev', 'Housing & Development'
    PARKS = 'Parks & Green Spaces', 'Parks & Green Spaces'
    PLAN = 'Urban Planning', 'Urban Planning'
    SAFE = 'Public Safety', 'Public Safety'
    SENIOR = 'Senior Services', 'Senior Services'
    TRANSPORT = 'Transportation & Infrastructure', 'Transportation & Infrastructure'
    VOLUNTEER = 'Volunteering', 'Volunteering Opportunities'

TOPIC_MAX_LENGTH = max(len(choice.value) for choice in Topic_Options)

IDEA_FOLDERS = [('Inbox', 'Inbox')] + list(Topic_Options.choices)

IDEA_FOLDERS_MAX_LENGTH = max(len(value) for value, _ in IDEA_FOLDERS)

class Account_Status(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'
    SUSPENDED = 'Suspended', 'Suspended'
    BANNED = 'Banned', 'Banned'

ACCT_STATUS_MAX_LENGTH = max(len(choice.value) for choice in Account_Status)

RES_GROUP_NAME = 'residents'
MOD_GROUP_NAME = 'moderators'
ADMIN_GROUP_NAME = 'site_admin'