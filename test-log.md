# Test Log

|Test ID| Feature| Steps Taken | Expected Result | Actual Result | Pass/Fail | Notes|
|-------|--------|-------------|-----------------|---------------|-----------|------|

|T-00   | Sever Startup - idea_suggestion | Run python manage.py runserver | Server starts without errors | Server started and displayed placeholder value from views.py | Pass| - |
|T-01   | idea_suggestion - urls | Run python test idea_suggestion | URL tests resolve to correct views| All tests in idea_suggestion.test_urls.py passed | Pass| Tested routes:<br>- admin/inbox/<br>- admin/idea_detail/<int:pk>/<br>- resident/submission/  |
|T-02   | idea_suggestion - models, fields | Run python test idea_suggestion.tests.test_models | Field values in Idea model follow defaults and constraints | All TestField tests passed | Pass| Tested: <br>- test_delete_user <br>- test_topic_valid <br>- test_time_stamp_default_value <br>- test_read_status_default_value <br>- test_file_location_default_value |
|T-03   | idea_suggestion - models, methods | Run python test idea_suggestion.tests.test_models | Methods in Idea model return expected values | All TestMethods tests passed | Pass| Tested: <br>- test__str__no_resident <br>- test__str__with_resident <br>- test__get_resident__no_resident <br>- test__get_resident__with_resident |
|T-04   | idea_suggestion - views | Run python test idea_suggestion.tests.test_views | Views return 200 code status and load correct template | All TestView tests passed | Pass| Tested: <br>- test_resident_submission <br>- test_admin_inbox <br>- test_admin_idea_detail |
|T-05   | idea_suggestion - forms (Submit Idea Form) | Run python test idea_suggestion.tests.test_forms | Forms are valid when fields are filled with legal inputs and not valid when empty or filled with illegal contents | All TestForms tests passed | Pass| Tested: <br>- test_idea_form_is_valid <br>- test_idea_form_empty <br>- test_idea_form_illegal_topic |
|T-06   | idea_suggestion - views | Run python test idea_suggestion.tests.test_views | Views return 200 code status and load correct template | All TestView tests passed | Pass| Tested: <br>- test_resident_submission <br>- test_admin_inbox <br>- test_admin_idea_detail <br>- test_admin_smart_summary. Note: admin logic was moved from view to admin_inbox_services and mark read functionality was updated to include handling for querysets |
|T-07   | idea_suggestion - urls | Run python test idea_suggestion.tests.test_url | URL tests resolve to correct views| All tests in idea_suggestion.test_urls.py passed | Pass| Tested routes:<br>- admin/inbox/<br>- admin/idea_detail/<int:pk>/<br>- resident/submission/ <br>- admin/inbox_smart_summary  |
|T-08   | smart_functionality - converters | Run python manage.py test smart_functionality.tests.test_converters | Strings with predictable values | All tests in smart_functionality.tests.test_converters.py passed | Pass| Primitives, empty strings, and instances of idea model with and without a picture convert to string |
|T-09   | smart_functionality - batching | Run python manage.py test smart_functionality.tests.test_batching | lists of strings and numbers | All tests in smart_functionality.tests.test_batching.py passed | Pass| Tested empty input, single input, and multi input for correct counts, weights, batch size, and output values |
|T-10 | gamification services | used valid arguments for award_points() | PointsLog object created with anticipated user and point type, Returns True | Points Log created, Return=True | Pass | All values match expected |
|T-11 | gamification services | used invalid action for award_points() | Returns False |Return=False | Pass | Returns expected |
|T-12 | gamification services | used invalid user for award_points() | Returns False |Return=False | Pass | Returns expected |
|T-13 | gamification services | used valid input for get_points_for_action() | Return=5 |Return=5 | Pass | Returns expected value |
|T-14 | gamification services | used invalid action for get_points_for_action() | Return=0 |Return=0 | Pass | Returns expected value |
|T-15 | gamification services | used valid input for create_points_record() | Creates Point Log with expected values | User matches test, point type matches test, timestamp matches test | Pass | Returns expected values |
|T-16 | gamification services | used invalid user for create_points_record() | Does not create Point Log, returns None| Return=None | Pass | Returns expected value |
|T-17 | gamification services | used invalid point type for create_points_record() | Does not create Point Log, returns None| Return=None | Pass | Returns expected value |
|T-18 | gamification services | used valid input for update_user_points() | Updates UserPoints for category point type and grand total| UserPoints updated for point type and grand total | Pass | Values match expected |
|T-19 | gamification services | used valid input for update_user_points(), single update | Updates UserPoints for category point type and grand total| UserPoints updated for point type and grand total | Pass | Values match expected |
|T-20 | gamification services | used valid input for update_user_points(), multiple updates same point type | Updates UserPoints for category point type and grand total| UserPoints updated for point type and grand total | Pass | Values match expected |
|T-21 | gamification services | used valid input for update_user_points(), multiple updates different point type | Updates UserPoints for both category point types and grand total| UserPoints updated for point types and grand total | Pass | Values match expected |
|T-22 | gamification services | used invalid point type for update_user_points() | No updates made to UserPoints | UserPoints are not updated | Pass | Values match expected |
|T-22 | gamification services | used invalid point type for update_user_points() | No updates made to UserPoints | UserPoints are not updated | Pass | Values match expected |
|T-23 | gamification services | used valid input for get_points_by_user() | Returns UserPoints for given inputs | UserPoints returned | Pass | Values match expected |
|T-24 | gamification services | used invalid point type for get_points_by_user() | Returns 0 | Return=0 | Pass | Value match expected |
|T-25 | gamification services | used invalid user for get_points_by_user() | Returns 0 | Return=0 | Pass | Value match expected |
|T-26 | gamification services | used valid input for process_badge_awards() | Returns True | Return=True | Pass | Value match expected |
|T-27 | gamification services | used invalid point type for process_badge_awards() | Returns False | Return=False | Pass | Value match expected |
|T-28 | gamification services | used invalid point amount for process_badge_awards() | Returns False | Return=False | Pass | Value match expected |
|T-29 | gamification services | used 0 points (invalid) for process_badge_awards() | Returns False | Return=False | Pass | Value match expected |
|T-30 | gamification services | used invalid point type for process_badge_awards() | Returns False | Return=False | Pass | Value match expected |
|T-31 | gamification services | used valid input for create_badge_record() | BadgeLog is created with anticipated fields | BadgeLog was created, user, badge name, timestamp match expected values| Pass | Values match expected |
|T-32 | gamification services | used invalid for badge for create_badge_record() | BadgeLog not created | BadgeLog was not created | Pass | Count of user badges matches before and after test |
|T-33 | gamification services | used no for badge for get_badge_record() | Returns None | Return=None | Pass | Value matches expected |
|T-34 | gamification services | used one for badge for get_badge_record() | Returns a list with one badge | Returned a list with one badge | Pass | Value matches expected |
|T-35 | gamification services | used multipe for badge for get_badge_record() | Returns a list with multiple badges | Returned a list with multipe badges | Pass | Values match expected |
|T-36 | gamification services | used invalid user input for get_badge_record() | ReturnsNone | Return=None | Pass | Value matches expected |