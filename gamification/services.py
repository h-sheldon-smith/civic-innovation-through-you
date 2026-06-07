from . import models, choices
from django.db.models import F
from django.contrib.auth.models import User
    

'''
Method to process points to a user
@param user, the user who earned points
@param action, the action that earns points
@return True if points were awarded, otherwise False
If successful, adds a record to the PointsLog and updates UserPoints
'''
def award_points(user, action):

    if not isinstance(user, models.User) or not isinstance(action, choices.PointType):
        return False

    points = get_points_for_action(action)

    if points > 0:
        create_points_record(user, action, points)
        update_user_points(user, action, points)

        return True
    
    return False


'''
Method to get points value for a specific type of action that earns points
@param action, the action that earns points
@return the points value for the action
If successful, it returns the points for the given action, otherwise it returns 0
'''
def get_points_for_action(action):

    if not isinstance(action, choices.PointType):
        return 0

    point_rule = models.PointRule.objects.filter(point_type=action).first()

    if not point_rule:
         return 0
    
    return point_rule.value
    

'''
Method to create a record for points earned
@param user, the user who earned points
@param action, the action that earns points
@param points, the earned points
'''
def create_points_record(user, action, points):
    
    if not isinstance(user, models.User) or not isinstance(action, choices.PointType):
        return
    
    if not isinstance(points, int) or points < 0:
        return 

    record = models.PointsLog(resident=user, point_type=action, points_earned=points)
    record.save()


'''
Method to update a user's running point total
@param user, the user who earned points
@param action, the action that earns points
@param points, the earned points
'''
def update_user_points(user, action, points):

    if not isinstance(user, models.User) or not isinstance(action, choices.PointType):
        return 
    
    if not isinstance(points, int) or points < 0:
        return

    # Update Category Points
    user_points, created = models.UserPoints.objects.get_or_create(resident=user, point_type=action)
    user_points.total_points = F("total_points") + points # F prevents race conditions
    user_points.save()

    # Update Grand Total Points (all categories)
    user_grand_total, created = models.UserPoints.objects.get_or_create(resident=user, point_type=choices.PointType.GRAND_TOTAL)
    user_grand_total.total_points = F("total_points") + points # F prevents race conditions
    user_grand_total.save()


'''
Method to award a badge to a user
@param user, the user who may have earned a badge
@param action, the action that earns points, triggering a potential badge award
@return True if a badge was awarded, otherwise False
If successful, adds a record to the BadgesLog and updates UserBadges
'''
def process_badge_awards(user, action):

    if not isinstance(user, models.User) or not isinstance(action, choices.PointType):
        return False

    points = get_points_by_user(user, action)
    if points is None or points==0:
        return False

    badge = get_badge_by_points(action, points)
    if not badge:
        return False

    create_badge_record(user, action)

    return True


'''
Method to get a badge based on an action and set of points
@param action, the type of action that earns badges
@param points, the number of points won for the action
@return the badge associated with the action and points total or None if no such badge exists
'''
def get_points_by_user(user, action):

    if not isinstance(user, models.User) or not isinstance(action, choices.PointType):
        return 0

    user_points = models.UserPoints.objects.filter(resident=user, point_type=action).first()
    return user_points.total_points if user_points else 0


'''
Method to get a badge based on an action and set of points
@param action, the type of action that earns badges
@param points, the number of points won for the action
@return the badge associated with the action and points total or None if no such badge exists
'''
def get_badge_by_points(action, points):

    if not isinstance(action, choices.PointType) or not isinstance(points, int):
        return None
    
    badge_rule = models.BadgeRule.objects.filter(point_type=action, point_threshold=points).first()
    return badge_rule.badge if badge_rule else None


'''
Method to create a record for badges earned
@param user, the user who earned the badge
@param badge, the badge the user earned
'''
def create_badge_record(user, badge):

    if not isinstance(badge, models.Badge) or not isinstance(user, models.User):
        return
    
    record = models.BadgeLog(resident=user, badge=badge)
    record.full_clean()
    record.save()



'''
Method to get all of a user's badges
@param user, the user who earned the badge
@return the user's badges if they exist, otherwise None
'''
def get_user_badges(user):

    if not isinstance(user, models.User):
        return None

    records = models.BadgeLog.objects.filter(resident=user)

    if not records:
        return None
    
    badges = []
    
    for r in records:
        badges.append(r.badge)

    return badges if badges else None