# Lists all the goals for your account, highlighting the red onesimport time,datetime
from beeminder import Beeminder
import datetime

pyminder = Beeminder(ini_file="beeminder.ini")

print("Retrieving goals...")
goals = pyminder.get_goals()
now = datetime.datetime.now()
for goal in goals:
    goal_losedate = datetime.datetime.fromtimestamp(goal['losedate'])
    delta = goal_losedate-now
    print(f"{goal['slug']} expires at {goal_losedate} in {goal_losedate-now}",end=" ")
    if delta.days==0:
        print("- RED GOAL")
    elif delta.days==1:
        print("- amber goal")
    elif delta.days==2:
        print("- blue goal")
    else:
        print("- green goal")
    

