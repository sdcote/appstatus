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

    def read(self):
        """Read in the JSON containing the nodes and their desired state"""
        with open(self.filename) as json_file:
            data = json.load(json_file)
        if 'nodes' in data:
            nodes = data['nodes']
            for n in nodes:
                if 'host' in n:
                    node = self.add_node(n['host'])
                    if 'goal' in n:
                        node.set_goal(n['goal'])
        if 'authentication' in data:
            auth = data['authentication']
            if 'username' in auth:
                self.usernm = auth['username']
            if 'password' in auth:
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
            if g is not None and g > "": line = line + " GOAL:" + g

            print(line)

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
        try:
            r = requests.get(url, verify=False)
            if r.status_code < 300:
                data = r.json()
                self.status = data['status']
                if 'version' in data:
                    self.version = data['version']
                if 'appid' in data:
                    self.appid = data['appid']
                if 'hostname' in data:
                    self.hostname = data['hostname']
            else:
                print("Error retrieving status: (" + url + ") " + str(r.status_code) + " - " + r.reason)
        except requests.exceptions.Timeout:
            print("The connection timed-out: " + url)
        except requests.exceptions.TooManyRedirects as e:
            print("The host does not seem to be valid: " + url + " - " + e)
        except requests.exceptions.ConnectionError as e:
            print("The host does not seem to be accepting requests: " + url + " - " + str(e))
        except Exception as e:
            e = sys.exc_info()[0]
            print("Fatal: " + str(e))
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
        if self.status.equals('ready'):
            self.set_status('stand-by', username, password)
        elif self.status.equals('stage'):
            self.set_status('ready', username, password)

    def roll_back(self, username, password):
        self.check()
        if self.status.equals('ready'):
            self.set_status('stage', username, password)
        elif self.status.equals('stand-by'):
            self.set_status('ready', username, password)

    def commit(self, username, password):
        self.check()
        if self.status.equals('stand-by'):
            self.set_status('stage', username, password)

    def set_status(self, status, username, password):
        endpoint = self.get_url()
        payload = {'status': status}
        if username is not None:
            r = requests.post(url=endpoint, json=payload, auth=(username, password), verify=False)
        else:
            r = requests.post(url=endpoint, json=payload, verify=False)

        if r.status_code < 300:
            print(r.json())
        else:
            line = str(r.status_code)
            line = line + " - "
            line = line + r.reason
            print(line)

    def get_url(self):
        tokens = self.name.split(":");
        retval = "http://" + self.name + "/api/appstatus"

        if (len(tokens) == 2) and (tokens[1] == "443"):
            retval = "https://" + tokens[0] + "/api/appstatus"

        return retval
