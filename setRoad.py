# Reads the road for a goal from a CSV file and sends it to beeminder
import datetime
import argparse
from beeminder import Beeminder
import json

version=1.0

parser = argparse.ArgumentParser(description=f"Version {version}: Sets the goal road matrix for a given goal, based on a CSV file")
parser.add_argument('-g', '--goalname', dest='goalname', type=str, default="test_newroad", required=True, help="Name of goal whose road is to be retrieved")
parser.add_argument('-f', '--file', dest='road_file_name', type=str, default='road.csv', help="File where road goal is to be written in CSV format")
parser.add_argument('--ini',dest="ini_filename", type=str, default="beeminder.ini", help="Name of ini file where username and token are stored")
parser.add_argument('-v','--verbose',dest="verbose", action='store_true', help="Display version of this program")
args = parser.parse_args()

pyminder = Beeminder(ini_file=args.ini_filename)

# import the csv and turn it into a "roadall":
# Array of arrays that can be used to construct the Red Line, aka the graph matrix
#   - To construct roadall, start with an initial row consisting of [initday, initval, None]
#   - and then each row of the graph matrix specifies 2 out of 3 of [t,v,r] which gives the segment ending at time t
#   - and then a final row consisting of [goaldate, goalval, rate]
import csv
import dateutil.parser as dp
roadall=[]
with open(args.road_file_name, "r", newline='') as csvfile:
    rdr = csv.DictReader(csvfile,fieldnames=('date','val','slope'))
    for row in rdr:
        rowtimestamp = (dp.parse(row['date'])).timestamp() + 86400/2   # timestamp is mid-day on this YYYY-MM-DD date
        row_val = row['val'].strip()
        row_rate = row['slope'].strip()
        newrow = [int(rowtimestamp), None if row_val=='None' else float(row_val), None if row_rate=='None' else float(row_rate)]
        roadall.append(newrow)
        if args.verbose:
            print(f"({row['date']}, {row['val']}, {row['slope']}) => {newrow}")

json_road = json.JSONEncoder().encode(roadall)
if args.verbose:
    print(json_road)
resulting_goal = pyminder.update_road((args.goalname).strip(), json_road)
