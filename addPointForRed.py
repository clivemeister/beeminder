# adds a datapoint to a named goal, conditional on you having any goals in the red
from beeminder import Beeminder
import datetime, time
import argparse

version=1.0

parser = argparse.ArgumentParser(description=f"Version {version}: Add a datapoint to a named goal, if and only if you have any goals in the red")
parser.add_argument('-g', '--goalred', dest='goalred', required=True, type=str, help="Name of goal where datapoint is added if any other goals are red")
parser.add_argument('-t', '--testrun', dest="testrun", action='store_true', help="Test what the result would be, without adding the datapoint")
parser.add_argument('--ini',dest="ini_filename", type=str, default="beeminder.ini", help="Name of ini file where username and token are stored")
parser.add_argument('-v','--verbose',dest="verbose", action='store_true', help="Chatty listing of all goal colours and deadlines")
args = parser.parse_args()

pyminder = Beeminder(ini_file=args.ini_filename)

print("Retrieving goals...")
goals = pyminder.get_goals()
goalred = (args.goalred).strip()
now = datetime.datetime.now()
red_goal_count=0
for goal in goals:
    goal_losedate = datetime.datetime.fromtimestamp(goal['losedate'])
    delta = goal_losedate-now

    if goal['slug']==goalred:
        if args.verbose:
            print(f"Skipping target goal <{goalred}> ")
        continue

    if (delta.days==0):
        print(f"RED GOAL: <{goal['slug']}> expires at {goal_losedate} in {goal_losedate-now}")
        red_goal_count += 1
    elif args.verbose:
        goal_colour=""
        if delta.days==1:
            goal_colour = "Amber goal:"
        elif delta.days==2:
            goal_colour = "Blue goal:"
        else:
            goal_colour = "Green goal:"
        print(f"{goal_colour} <{goal['slug']}> expires at {goal_losedate} in {goal_losedate-now}")
        

if red_goal_count==0:
    print("No red goals")
    rc=pyminder.create_datapoint(args.goalred, time.mktime(now.timetuple()), 0,   \
                                       comment=f"Added by addPointForRed via API", sendmail='false')
    print(f"Added datapoint of zero to {args.goalred}")
    if args.verbose:
        print(f"Returned {rc}") 
else:
    print(f"Total of {red_goal_count} red goals")
    if args.testrun:
        print(f"We are testing, otherwise we would have added a datapoint of {red_goal_count} to {args.goalred}")
    else:
        rc=pyminder.create_datapoint(args.goalred, time.mktime(now.timetuple()), red_goal_count,   \
                                       comment=f"Added by addPointForRed via API", sendmail='false')
        print(f"Added datapoint {red_goal_count} to {args.goalred}")
        if args.verbose:
            print("Returned {rc}")