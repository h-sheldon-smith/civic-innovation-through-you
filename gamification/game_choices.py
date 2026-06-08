from django.db import models

class PointType(models.TextChoices):
    LOGIN = 'Login', 'Login'
    SUGGESTION = 'Suggestion', 'Suggestion'
    COMMENT = 'Comment', 'Comment'
    LIKE = 'Like', 'Like'
    RECEIVE_LIKE = 'Receive Like', 'Receive Like'
    VOTE = 'Vote', 'Vote'
    GRAND_TOTAL = 'Grand Total', 'Grand Total'

POINT_TYPE_MAX_LENGTH = max(len(choice.value) for choice in PointType)