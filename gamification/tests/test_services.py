from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from freezegun import freeze_time
from gamification import models, choices, services

# Test Methods Relating to Points
class TestPoints(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

        self.action = "Suggestion"
        self.points = 5

        self.action2 = "Login"
        self.points2 = 1

    # def test__award_points(self):
    #     expected = 
    #     self.assertEquals(, expected)
    
    def test_get_points_for_action_valid(self):
        expected = 5
        actual = services.get_points_for_action(self.action)
        self.assertEqual(actual, expected)

    def test_get_points_for_action_not_valid(self):
        expected = 0
        actual = services.get_points_for_action("random word")
        self.assertEqual(actual, expected)

    @freeze_time("2026-01-01 11:55:55")
    def test_create_points_record(self):
        services.create_points_record(self.user, self.action, self.points)
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


    def test__update_user_points(self):
        services.update_user_points(self.user, self.action, self.points)
        suggestion_record= models.UserPoints.objects.get(resident=self.user, point_type=self.action)

        expected_cat_points = 5
        actual_cat_points = suggestion_record.total_points
        self.assertEqual(actual_cat_points, expected_cat_points)

        grand_total_record= models.UserPoints.objects.get(resident=self.user, point_type="Grand Total")

        expected_grand_total_points = 5
        actual_grand_total_points = grand_total_record.total_points
        self.assertEqual(actual_grand_total_points, expected_grand_total_points)


    def test__update_user_points_new_category_total(self):
        services.update_user_points(self.user, self.action, self.points)
        suggestion_record= models.UserPoints.objects.get(resident=self.user, point_type=self.action)

        expected_cat_points = 5
        actual_cat_points = suggestion_record.total_points
        self.assertEqual(actual_cat_points, expected_cat_points)

        services.update_user_points(self.user, self.action, self.points)
        updated_suggestion_record= models.UserPoints.objects.get(resident=self.user, point_type=self.action)

        expected_cat_points_updated = 10
        actual_cat_points_updated = updated_suggestion_record.total_points
        self.assertEqual(actual_cat_points_updated, expected_cat_points_updated)

    def test__update_user_points_new_grand_total(self):
        services.update_user_points(self.user, self.action, self.points)
        grand_total_record = models.UserPoints.objects.get(resident=self.user, point_type="Grand Total")

        expected_grand_total_points = 5
        actual_grand_total_points = grand_total_record.total_points
        self.assertEqual(actual_grand_total_points, expected_grand_total_points)

        services.update_user_points(self.user, self.action2, self.points2)
        updated_grand_total_record = models.UserPoints.objects.get(resident=self.user, point_type="Grand Total")

        expected_updated_grand_total_points = 6
        actual_updated_grand_total_points = updated_grand_total_record.total_points
        self.assertEqual(actual_updated_grand_total_points, expected_updated_grand_total_points)