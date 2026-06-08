from gamification import game_services, game_choices

def Save_Resident_Idea(resident, idea_form):
    idea_instance = idea_form.save(commit = False) # django makes an instance of the form
    idea_instance.resident = resident #request.user # add the logged in user
    idea_instance.save()


def Process_Rewards(resident):
    points_result = game_services.award_points(resident, game_choices.PointType.SUGGESTION)

    if points_result:
        game_services.process_badge_awards(resident, game_choices.PointType.SUGGESTION)