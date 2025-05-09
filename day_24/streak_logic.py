def check_milestones(habit, habit_data):
    streak = habit_data['current_streak']
    milestones = habit_data['milestones']
    for milestone in ['3', '7', '30']:
        if streak >= int(milestone) and not milestones[milestone]:
            milestones[milestone] = True
            print(f"🎉 Congrats! '{habit}' reached a {milestone}-day streak!")