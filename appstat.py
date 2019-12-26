import argparse
from AppStatus import Node

parser = argparse.ArgumentParser(description='Modify the AppStatus of a deployment node')
parser.add_argument("host", nargs='?', help="the host:port of the application instance to set")
parser.add_argument("status", nargs='?', help="the status to be set")
parser.add_argument("-u", "--username", help="Username credential")
parser.add_argument("-p", "--password", help="Password credential")

args = parser.parse_args()


def show_node_status(host):
    node = Node(host)
    line = "NODE:"
    line = line + node.get_name()
    node.check()
    line = line + " STATUS:"
    line = line + node.get_status()
    line = line + " VERSION:"
    line = line + node.get_version()
    print line


def set_node_status(host, status, username, password):
    node = Node(host)
    node.check()
    # originalState = node.get_status()
    node.set_status(status, username, password)


if not args.host:
    print "No host specified, nothing to do."
else:
    if not args.status:
        show_node_status(args.host)
    else:
        set_node_status(args.host, args.status, args.username, args.password)
