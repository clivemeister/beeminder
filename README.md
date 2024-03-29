# Clive's Beeminder utility functions
A bunch of tools that work with Beeminder to do various interesting things.

## Setup
Assuming you've got Python installed, you'd start by cloning the repo to your machine.  Then you need to rename the "beeminder sample.ini" to "beeminder.ini" and add your Beeminder 
 authorisation token in the new beeminder.ini file

### Extra to use the Todoist integration
You'll need to add your Todoist authorisation token to the beeminder.ini file as well, if you want to use that integration.
You'll also need to install the todoist integration using `pip install todoist_api_python`

## Use
You can check out the help for a function by adding the `-h` or `--help` flag.  Plus of course they're python, so you'll need to pass the function to the python interpreter, something like this:
```
py getTodoistOverdue.py --help
```
That will show you (in this case) that you can use for example a `-t` flag for a test run (which doesn't update the goal), and pass the goal name to be updated with the `-g` flag:
```
py getTodoistOverdue.py -t -g myOverdueTasksGoal
```
That'll show you how many overdue tasks you currently have (use the `-v` flag for a verbose run, which actually prints them out), but won't update the goal.  Run without the `-t` flag to actually update the Beeminder goal.
