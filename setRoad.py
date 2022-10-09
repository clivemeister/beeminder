import datetime
import argparse
from beeminder import Beeminder

parser = argparse.ArgumentParser(description="Sets the goal road matrix for a given goal, based on a CSV file")
parser.add_argument('-g', '--goalname', dest='goalname', type=str, default="tomatoes", required=True, help="Name of goal whose road is to be retrieved")
parser.add_argument('-f', '--file', dest='road_file_name', type=str, default='road.csv', help="File where road goal is to be written in CSV format")
parser.add_argument('--ini',dest="ini_filename", type=str, default="beeminder.ini", help="Name of ini file where username and token are stored")
args = parser.parse_args()

pyminder = Beeminder(ini_file=args.ini_filename)

import csv
with open(args.road_file_name, "r", newline='') as csvfile:
    rdr = csv.reader(csvfile)
    for row in rdr:
        print(row)

#goal = pyminder.get_goal(args.goalname)
#pyminder.set_goal(args.goalname)