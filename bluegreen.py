import argparse
from AppStatus import Plan

parser = argparse.ArgumentParser(description='Modify the AppStatus of deploument nodes')
parser.add_argument("method", nargs='*', default="status",
                    choices=["forward", "back", "commit", "single", "rolling", "status"],
                    help="the type of deployment (default = status)")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="verbose output")
parser.add_argument("-f", "--file", help="file name for the plan (default = plan.json)")
parser.add_argument("-u", "--username", help="Username credential")
parser.add_argument("-p", "--password", help="Password credential")

args = parser.parse_args()
if args.verbose:
    print "verbosity turned on"

filename = "plan.json"
if args.file != None:
    filename = args.file

if args.verbose:
    print("Using a plan file of " + filename)

plan = Plan(filename)

if args.verbose:
    print "The plan contains " + str(len(plan.nodes)) + " nodes"

plan.show_current()
