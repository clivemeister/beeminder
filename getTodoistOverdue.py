# get a list (and count) of the overdue goals in Todoist
from todoist_api_python.api import TodoistAPI
import argparse
import configparser
from beeminder import Beeminder

version=1.0

parser = argparse.ArgumentParser(description=f"Version {version}: Retrieves and counts your overdue goals from Todoist")
parser.add_argument('--ini',dest="ini_filename", type=str, default="beeminder.ini", help="Name of ini file where username and token are stored")
parser.add_argument('-g', '--goal', dest='goal', required=True, type=str, help="Name of goal where datapoint with count of overdue tasks is added")
parser.add_argument('-t', '--test', dest="test", action='store_true', help="Test what the result would be, without adding the datapoint")
parser.add_argument('-v','--verbose',dest="verbose", action='store_true', help="Chatty listing of all overdue tasks")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.ini_filename)

pyminder = Beeminder(ini_file=args.ini_filename)

api = TodoistAPI( config['USER']['todoist_token'] )

try:
    tasks = api.get_tasks(filter="Overdue")
    if args.verbose:
        for t in tasks:
            print(t.due.date, t.content)
    overdue_count = len(tasks)

except Exception as error:
    print(error)
    exit(-1)

if overdue_count==0:
    print("No overdue tasks")
    if args.test:
        print(f"We are testing, otherwise we would have added a datapoint of 0 to goal {args.goal}")
    else:
        rc=pyminder.create_datapoint(args.goal, time.mktime(now.timetuple()), 0,   \
                                        comment=f"Added by getTodoistOverdue via API", sendmail='false')
        print(f"Added datapoint of zero to {args.goal}")
        if args.verbose:
            print(f"Returned {rc}") 
else:
    print(f"Total of {overdue_count} overdue items")
    if args.test:
        print(f"We are testing, otherwise we would have added a datapoint of {overdue_count} to goal {args.goal}")
    else:
        rc=pyminder.create_datapoint(args.goal, time.mktime(now.timetuple()), overdue_count,   \
                                       comment=f"Added by getTodoistOverdue via API", sendmail='false')
        print(f"Added datapoint {overdue_count} to {args.goal}")
        if args.verbose:
            print("Returned {rc}")
