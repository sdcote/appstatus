#!/usr/bin/env python3
import argparse

from AppStatus import Plan

parser = argparse.ArgumentParser(description='Modify the AppStatus of deployment nodes')
parser.add_argument("action",
                    nargs='*',
                    default="status",
                    choices=["forward", "rollback", "commit", "single", "rolling", "goal", "status"],
                    help="the type of action to take (default = status)")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="verbose output")
parser.add_argument("-f", "--file", help="file name for the plan (default = plan.json)")
parser.add_argument("-u", "--username", help="Username credential")
parser.add_argument("-p", "--password", help="Password credential")
parser.add_argument("-n", "--node", help="Execute on one node only")
parser.add_argument("-s", "--status", help="The status to set")

args = parser.parse_args()
if args.verbose:
    print "verbosity turned on"

filename = "plan.json"
if args.file is not None:
    filename = args.file

if args.verbose:
    print("Using a plan file of " + filename)

plan = Plan(filename)

if args.verbose:
    print "The plan contains " + str(len(plan.nodes)) + " nodes"

if args.action[0] == "status":
    plan.show_current()
