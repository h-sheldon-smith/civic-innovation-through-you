from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from freezegun import freeze_time
from gamification import game_choices, game_services, models

# Test Methods Relating to Points
class TestPoints(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

        self.action = game_choices.PointType.SUGGESTION
        self.points = 5

        self.action2 = game_choices.PointType.LOGIN
        self.points2 = 1

    def test_award_points(self):
        expected = True
        actual = game_services.award_points(self.user, self.action)
        self.assertEquals(actual, expected)

        record = models.PointsLog.objects.filter(resident=self.user, point_type=self.action).first()

        expected_user = self.user
        actual_user = record.resident
        self.assertEqual(actual_user, expected_user)

        expected_action = self.action
        actual_action = record.point_type
        self.assertEqual(actual_action, expected_action)

    def test_award_points_invalid_action(self):
        expected = False
        actual = game_services.award_points(self.user, "random action")
        self.assertEquals(actual, expected)

    def test_award_points_invalid_user(self):
        expected = False
        actual = game_services.award_points("invalid user", self.action)
        self.assertEquals(actual, expected)
    
    def test_get_points_for_action_valid(self):
        expected = 5
        actual = game_services.get_points_for_action(self.action)
        self.assertEqual(actual, expected)

    def test_get_points_for_action_not_valid(self):
        expected = 0
        actual = game_services.get_points_for_action("random word")
        self.assertEqual(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_create_points_record(self):
        game_services.create_points_record(self.user, self.action, self.points)
        record = models.PointsLog.objects.get(resident=self.user, point_type=self.action, timestamp=timezone.now())

        expected_user = self.user
        actual_user = record.resident
        self.assertEqual(actual_user, expected_user)

        expected_point_type = self.action
        actual_point_type = record.point_type
        self.assertEqual(actual_point_type, expected_point_type)

        expected_timestamp = timezone.now()
        actual_timestamp = record.timestamp
        self.assertEqual(actual_timestamp, expected_timestamp)

    def test_create_points_record_invalid_user(self):
        game_services.create_points_record("invalid user", self.action, self.points)
        record = models.PointsLog.objects.filter(resident=self.user, point_type=self.action, timestamp=timezone.now()).first()

        expected = None
        actual = record
        self.assertEqual(actual, expected)

    def test_create_points_record_invalid_action(self):
        game_services.create_points_record(self.user, "invalid action", self.points)
        record = models.PointsLog.objects.filter(resident=self.user, point_type=self.action, timestamp=timezone.now()).first()

        expected = None
        actual = record
        self.assertEqual(actual, expected)

    def test_create_points_record_invalid_point_type(self):
        game_services.create_points_record(self.user, self.action, 2.0)
        record = models.PointsLog.objects.filter(resident=self.user, point_type=self.action, timestamp=timezone.now()).first()

        expected = None
        actual = record
        self.assertEqual(actual, expected)

    def test_create_points_record_invalid_point_value(self):
        game_services.create_points_record(self.user, self.action, -1)
        record = models.PointsLog.objects.filter(resident=self.user, point_type=self.action, timestamp=timezone.now()).first()

        expected = None
        actual = record
        self.assertEqual(actual, expected)

    def test_update_user_points(self):
        game_services.update_user_points(self.user, self.action, self.points)
        suggestion_record= models.UserPoints.objects.get(resident=self.user, point_type=self.action)

        expected_cat_points = 5
        actual_cat_points = suggestion_record.total_points
        self.assertEqual(actual_cat_points, expected_cat_points)

        grand_total_record= models.UserPoints.objects.get(resident=self.user, point_type=game_choices.PointType.GRAND_TOTAL)

        expected_grand_total_points = 5
        actual_grand_total_points = grand_total_record.total_points
        self.assertEqual(actual_grand_total_points, expected_grand_total_points)


    def test_update_user_points_new_category_total(self):
        game_services.update_user_points(self.user, self.action, self.points)
        suggestion_record= models.UserPoints.objects.get(resident=self.user, point_type=self.action)

        expected_cat_points = 5
        actual_cat_points = suggestion_record.total_points
        self.assertEqual(actual_cat_points, expected_cat_points)

        game_services.update_user_points(self.user, self.action, self.points)
        updated_suggestion_record= models.UserPoints.objects.get(resident=self.user, point_type=self.action)

        expected_cat_points_updated = 10
        actual_cat_points_updated = updated_suggestion_record.total_points
        self.assertEqual(actual_cat_points_updated, expected_cat_points_updated)

    def test_update_user_points_new_grand_total(self):
        game_services.update_user_points(self.user, self.action, self.points)
        grand_total_record = models.UserPoints.objects.get(resident=self.user, point_type=game_choices.PointType.GRAND_TOTAL)

        expected_grand_total_points = 5
        actual_grand_total_points = grand_total_record.total_points
        self.assertEqual(actual_grand_total_points, expected_grand_total_points)

        game_services.update_user_points(self.user, self.action2, self.points2)
        updated_grand_total_record = models.UserPoints.objects.get(resident=self.user, point_type=game_choices.PointType.GRAND_TOTAL)

        expected_updated_grand_total_points = 6
        actual_updated_grand_total_points = updated_grand_total_record.total_points
        self.assertEqual(actual_updated_grand_total_points, expected_updated_grand_total_points)

    def test_update_user_points_invalid_action(self):
        game_services.update_user_points(self.user, self.action, self.points)
        before = models.UserPoints.objects.filter(resident=self.user, point_type=self.action).first()

        expected_before = 5
        actual_before = before.total_points
        self.assertEqual(actual_before, expected_before)

        game_services.update_user_points(self.user, "some action", self.points)
        after = models.UserPoints.objects.filter(resident=self.user, point_type=self.action).first()

        expected_after = 5
        actual_after = after.total_points
        
        self.assertEqual(actual_after, expected_after)

    def test_get_points_by_user_valid(self):
        game_services.update_user_points(self.user, self.action, self.points)
        expected = 5
        actual = game_services.get_points_by_user(self.user, self.action)
        self.assertEqual(actual, expected)

    def test_get_points_by_user_invalid_action(self):
        expected = 0
        actual = game_services.get_points_by_user(self.user, "random word")
        self.assertEqual(actual, expected)

    def test_get_points_by_user_invalid_user(self):
        expected = 0
        actual = game_services.get_points_by_user("random user input", self.action)
        self.assertEqual(actual, expected)

    def test_remove_points(self):
        game_services.award_points(self.user, self.action)
        expected_add_points = 5
        actual_add_points = game_services.get_points_by_user(self.user, self.action)
        self.assertEqual(actual_add_points, expected_add_points)

        expected_result = True
        actual_result = game_services.remove_points(self.user, self.action)
        self.assertEqual(actual_result, expected_result)

        expected_remove_points = 0
        actual_remove_points = game_services.get_points_by_user(self.user, self.action)
        self.assertEqual(actual_remove_points, expected_remove_points)

    def test_remove_points_more_than_user_has(self):
        expected_result = False
        actual_result= game_services.remove_points(self.user, self.action)
        self.assertEqual(actual_result, expected_result)

        expected_remove_points = 0
        actual_remove_points = game_services.get_points_by_user(self.user, self.action)
        self.assertEqual(actual_remove_points, expected_remove_points)


# Test Methods Relating to Badges
class TestBadges(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

        self.action = game_choices.PointType.SUGGESTION
        self.points = 5
        self.badge = models.Badge.objects.filter(name="Brainstormer").first()
        self.badge2 = models.Badge.objects.filter(name="New Resident").first()

    def test_process_badge_awards(self):
        game_services.update_user_points(self.user, self.action, self.points*3)
        expected = True
        actual = game_services.process_badge_awards(self.user, self.action)
        self.assertEquals(actual, expected)

    def test_process_badge_awards_invalid_action(self):
        expected = False
        actual = game_services.process_badge_awards(self.user, "random action")
        self.assertEquals(actual, expected)

    def test_test_award_points_insufficient_points(self):
        game_services.update_user_points(self.user, self.action, 1)
        expected = False
        actual = game_services.award_points(self.user, "random action")
        self.assertEquals(actual, expected)

    def test_get_badge_by_points_valid(self):
        actual = game_services.get_badge_by_points(self.action, self.points * 3)
        
        expected_name = "Brainstormer"
        actual_name = actual.name
        self.assertEquals(actual_name, expected_name)

    def test_get_badge_by_points_no_points(self):
        expected = None
        actual = game_services.get_badge_by_points(self.action, 0)
        self.assertEquals(actual, expected)

    def test_get_badge_by_points_invalid_action(self):
        expected = None
        actual = game_services.get_badge_by_points("invalid action", 15)
        self.assertEquals(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_create_badge_record(self):
        game_services.create_badge_record(self.user, self.badge)
        record = models.BadgeLog.objects.filter(resident=self.user, badge=self.badge, timestamp=timezone.now()).first()

        expected_user = self.user
        actual_user = record.resident
        self.assertEqual(actual_user, expected_user)

        expected_badge_name = self.badge.name
        actual_badge_name = record.badge.name
        self.assertEqual(actual_badge_name, expected_badge_name)

        expected_timestamp = timezone.now()
        actual_timestamp = record.timestamp
        self.assertEqual(actual_timestamp, expected_timestamp)

    @freeze_time("2026-01-01 11:55:55")
    def test_create_badge_record_invalid_badge(self):
        expected = models.BadgeLog.objects.count()
        game_services.create_badge_record(self.user, "invalid badge")
        actual = models.BadgeLog.objects.count()

        self.assertEqual(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_get_user_badges_no_badge(self):
        expected = None
        actual = game_services.get_user_badges(self.user)
        self.assertEqual(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_get_user_badges_one_badge(self):
        game_services.create_badge_record(self.user, self.badge)
        expected = [self.badge]
        actual = game_services.get_user_badges(self.user)
        self.assertEqual(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_get_user_badges_multiple_badges(self):
        game_services.create_badge_record(self.user, self.badge)
        game_services.create_badge_record(self.user, self.badge2)
        expected = [self.badge, self.badge2]
        actual = game_services.get_user_badges(self.user)
        self.assertEqual(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_get_user_badges_invalid_user_input(self):
        expected = None
        actual = game_services.get_user_badges("some user")
        self.assertEqual(actual, expected)