from . import models
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
    

'''
Method to award points to a user
@param user, the user who earned points
@param action, the action that earns points
@return True if points were awarded, otherwise False
If successful, adds a record to the PointsLog and updates UserPoints
'''
def award_points(user, action):

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
    try:
        return models.PointRule.objects.get(point_type=action).value
    except models.PointRule.DoesNotExist:
        return 0
    

'''
Method to create a record for points earned
@param user, the user who earned points
@param action, the action that earns points
@param points, the earned points
'''
def create_points_record(user, action, points):
        record = models.PointsLog(resident=user, point_type=action, points_earned=points)
        record.save()


'''
Method to update a user's running point total
@param user, the user who earned points
@param action, the action that earns points
@param points, the earned points
'''
def update_user_points(user, action, points):
        # Update Category Points
        user_points, created = models.UserPoints.objects.get_or_create(resident=user, point_type=action)
        user_points.total_points = F("total_points") + points # F prevents race conditions
        user_points.save()

        # Update Grand Total Points (all categories)
        user_grand_total, created = models.UserPoints.objects.get_or_create(resident=user, point_type="Grand Total")
        user_grand_total.total_points = F("total_points") + points # F prevents race conditions
        user_grand_total.save()