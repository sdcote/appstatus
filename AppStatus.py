# This is a collection of functions to help manage application status through the AppStatus API.


class Plan:
    """A plan is a list of Nodes and their desired state."""

    def __init__(self, filename):
        self.filename = filename
        self.read(filename)

    def read(self, filename):
        """Read in the JSON containing the nodes and their desired state"""
        pass

    def write(self, filename):
        pass

    def execute(self):
        pass

    def show_desired(self):
        pass

    def show_current(self):
        pass

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
        self.state = "unknown"
        self.version = "unknown"

    def check(self):
        pass

    def set_to_ready(self):
        pass

    def set_to_stage(self):
        pass

    def set_to_standby(self):
        pass

    def get_state(self):
        pass

    def get_version(self):
        pass

    def roll_forward(self):
        pass

    def roll_back(self):
        pass

    def commit(self):
        pass

