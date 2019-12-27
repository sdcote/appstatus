# This is a collection of functions to help manage application status through the AppStatus API.
# python -m pip install requests
import json
import sys

import requests


class Plan:
    """A plan is a list of Nodes and their desired state."""

    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.usernm = None
        self.passwd = None
        self.read()

    def read(self, ):
        """Read in the JSON containing the nodes and their desired state"""
        with open(self.filename) as json_file:
            data = json.load(json_file)
        if data.has_key('nodes'):
            nodes = data['nodes']
            for n in nodes:
                if n.has_key('host'):
                    node = self.add_node(n['host'])
                    if n.has_key('goal'):
                        node.set_goal(n['goal'])
        if data.has_key('authentication'):
            auth = data['authentication']
            if auth.has_key('username'):
                self.usernm = auth['username']
            if auth.has_key('password'):
                self.passwd = auth['password']

    def add_node(self, host):
        node = Node(host)
        self.nodes.append(node)
        return node

    def write(self, filename):
        """Write the plan to disk"""
        pass

    def execute(self):
        """Execute the plan changing the status of each node"""
        pass

    def show_desired(self):
        pass

    def show_current(self):
        for n in self.nodes:
            line = "NODE:"
            line = line + n.get_name()
            n.check()
            line = line + " STATUS:"
            line = line + n.get_status()
            line = line + " VERSION:"
            line = line + n.get_version()
            g = n.get_goal()
            if g is not None:
                line = line + " GOAL:"
                line = line + g
            print line

    def roll_forward(self):
        pass

    def roll_back(self):
        pass

    def commit(self):
        pass


class Node:
    """A Node is information about the current and desired state of an application host"""

    def __init__(self, name):
        self.name = name
        self.status = "unknown"
        self.version = "unknown"
        self.appid = "unknown"
        self.hostname = "unknown"
        self.goal = "unknown"

    def check(self):
        url = self.get_url()
        r = requests.get(url)
        try:
            if r.status_code < 300:
                data = r.json()
                self.status = data['status']
                if data.has_key('version'):
                    self.version = data['version']
                if data.has_key('appid'):
                    self.appid = data['appid']
                if data.has_key('hostname'):
                    self.hostname = data['hostname']
            else:
                print ("Error retrieving status: (" + url + ") " + str(r.status_code) + " - " + r.reason)
        except requests.exceptions.Timeout:
            print("The connection timed-out: " + url)
        except requests.exceptions.TooManyRedirects:
            print("The host does not seem to be valid: " + url)
        except requests.exceptions.ConnectionError:
            print("The host does not seem to be accepting requests: " + url)
        except BaseException as e:
            e = sys.exc_info()[0]
            print("Fatal: " + e)
            sys.exit(1)

    def set_goal_to_ready(self):
        self.goal = 'ready'

    def set_goal_to_stage(self):
        self.goal = 'stage'

    def set_goal_to_standby(self):
        self.goal = 'stand-by'

    def set_goal(self, username, password):
        self.set_status(self.goal, username, password)

    def get_name(self):
        return self.name

    def get_status(self):
        return self.status

    def get_version(self):
        return self.version

    def get_goal(self):
        return self.goal

    def set_goal(self, status):
        self.goal = status

    def roll_forward(self, username, password):
        self.check()
        if self.status is 'ready':
            self.set_status('stand-by', username, password)
        elif self.status is 'stage':
            self.set_status('ready', username, password)

    def roll_back(self, username, password):
        self.check()
        if self.status is 'ready':
            self.set_status('stage', username, password)
        elif self.status is 'stand-by':
            self.set_status('ready', username, password)

    def commit(self, username, password):
        self.check()
        if self.status is 'stand-by':
            self.set_status('stage', username, password)

    def set_status(self, status, username, password):
        endpoint = self.get_url()
        payload = {'status': status}
        if username is not None:
            r = requests.post(url=endpoint, json=payload, auth=(username, password))
        else:
            r = requests.post(url=endpoint, json=payload)

        if r.status_code < 300:
            print r.json()
        else:
            line = str(r.status_code)
            line = line + " - "
            line = line + r.reason
            print line

    def get_url(self):
        return "http://" + self.name + "/api/appstatus"
