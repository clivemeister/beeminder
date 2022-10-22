# Retrieves the road for a goal and stores it in a CSV file
import datetime
from beeminder import Beeminder
import argparse

version=1.0

parser = argparse.ArgumentParser(description=f"Version {version}: Retrieves the goal road matrix for a given goal, writing it to a CSV file")
parser.add_argument('-g', '--goalname', dest='goalname', type=str, default="dinner", required=True, help="Name of goal whose road is to be retrieved")
parser.add_argument('-f', '--file', dest='road_file_name', type=str, default='road.csv', help="File where road goal is to be written in CSV format")
parser.add_argument('--ini',dest="ini_filename", type=str, default="beeminder.ini", help="Name of ini file where username and token are stored")
parser.add_argument('-v','--verbose',dest="verbose", action='store_true', help="Display version of this program")
args = parser.parse_args()

pyminder = Beeminder(ini_file=args.ini_filename)
print(f"Retrieving the existing road for {args.goalname.strip()}:")

goal = pyminder.get_goal(args.goalname)
with open(args.road_file_name,"w") as csvfile:
    if args.verbose:
        print(goal['roadall']) 

    for line in goal['roadall']:
        thisline = f"{datetime.datetime.fromtimestamp(line[0]).date()}, {line[1]!s:>8}, {line[2]!s:>}"
        if args.verbose: 
            print(thisline)
        csvfile.write(thisline+"\n")

