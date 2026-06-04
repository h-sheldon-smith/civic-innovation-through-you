from django.db import models
from django.contrib.auth.models import User
from . import choices

# Stores total points for users
class UserPoints(models.Model):
    # Add User as a foreign key
    resident = models.ForeignKey(
       User,
       default = None,
       on_delete = models.CASCADE, # keep the idea even if the user is deleted
       null = True,
       related_name = 'user_points' # lets you look up all earned points by the given resident
    )

    point_type = models.CharField(max_length = choices.POINT_TYPE_MAX_LENGTH,
                                  choices = choices.PointType.choices)
    total_points = models.IntegerField(default = 0)
    
# Log for each time a resident earns points
class PointsLog(models.Model):
    # Add User as a foreign key
    resident = models.ForeignKey(
       User,
       default = None,
       on_delete = models.CASCADE, # keep the idea even if the user is deleted
       null = True,
       related_name = 'points_logs' # lets you look up all earned points by the given resident
    )

    point_type = models.CharField(max_length = choices.POINT_TYPE_MAX_LENGTH,
                                  choices = choices.PointType.choices)
    points_earned = models.IntegerField(null = False)
    timestamp = models.DateTimeField(auto_now_add = True, 
                                      editable = False)

# Log for each time a resident earns badges
class BadgeLog(models.Model):
    resident = models.ForeignKey(
       User,
       default = None,
       on_delete = models.CASCADE, # keep the idea even if the user is deleted
       null = True,
       related_name = 'badges' # lets you look up all user rewards by the given resident
    )

    badge = models.ForeignKey(
       'Badge',
       on_delete = models.CASCADE,
    )

    timestamp = models.DateTimeField(auto_now_add = True, 
                                      editable = False)
    
# The badges that residents can earn
class Badge(models.Model):
    name = models.CharField(max_length = 50, unique = True) #TODO: make a collection of badges
    icon = models.ImageField(
        upload_to='gamification/',
        blank = False,
        null = False,
        )
    message = models.TextField()

# The rules for how badges are earned
class BadgeRule(models.Model):
    badge = models.ForeignKey(
       Badge,
       default = None,
       on_delete = models.CASCADE,
    )

    point_type = models.CharField(max_length = choices.POINT_TYPE_MAX_LENGTH,
                                  choices = choices.PointType.choices,
                                  null = True) #option for just all points of any type
    point_threshold = models.IntegerField()

# How many points are awarded for a given action
class PointRule(models.Model):
    point_type = models.CharField(max_length = choices.POINT_TYPE_MAX_LENGTH,
                                  choices = choices.PointType.choices,
                                  unique = True)
    
    value = models.IntegerField(null = False)