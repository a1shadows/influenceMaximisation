import math
import time

import future.utils
import numpy as np
from ndlib.models.DiffusionModel import DiffusionModel


class TimeAware(DiffusionModel):

    def __init__(self, graph):

        # Call the super class constructor
        super(self.__class__, self).__init__(graph)

        # Method name
        self.name = "TimeAware"

        # Available node statuses
        self.available_statuses = {
            "Susceptible": 0,
            "Infected": 1,
        }
        # Exposed Parameters
        self.parameters = {
            "model": {},
            "nodes": {
                "Time": {  # Activation Time fo each node
                    "descr": "Time Node",
                    "range": [0, 1],
                    "optional": True,
                    "default": 0
                }
            },
            "edges": {
                "alpha": {  # Alpha denotes the strength
                    "descr": "Alpha Value",
                    "range": [0, 1],
                    "optional": True,
                    "default": 0.3
                }
            },
        }

    def iteration(self, node_status=True):

        self.clean_initial_status(self.available_statuses.values())

        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}  # Copy of Statuses

        # if first iteration return the initial node status
        if self.actual_iteration == 0:
            self.actual_iteration += 1

            for u in self.graph.nodes():
                timeActivated = time.time()
                self.params['nodes']['Time'][u] = timeActivated

            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}

        # iteration inner loop
        for u in self.graph.nodes():
            if actual_status[u] == 1:  # Check if not  Infected
                continue

            if self.params['nodes']['Time'][u] == 0:
                Time = time.time()
                self.params['nodes']['Time'][u] = Time
            else:
                Time = self.params['nodes']['Time'][u]

            neighbors = list(self.graph.neighbors(u))  # Neighbours of U

            for v in neighbors:
                if actual_status[v] == 1:  # If already Infected Continue
                    continue

                if (self.params['nodes']['Time'][v] == 0):
                    Time1 = time.time()
                    self.params['nodes']['Time'][v] = Time1
                else:
                    Time1 = self.params['nodes']['Time'][v]
                if (u, v) not in self.params['edges']['alpha']:
                    continue
                Alpha = self.params['edges']['alpha'][(u, v)]
                Equation1 = -Alpha * (Time1 - Time)
                Equation2 = Alpha * (math.e ** Equation1)

                flip = np.random.random_sample()
                if (Equation2 >= flip):
                    actual_status[v] = 1

        delta, node_count, status_delta = self.status_delta(actual_status)

        # update the actual status and iterative step
        self.status = actual_status
        self.actual_iteration += 1

        # return the actual configuration (only nodes with status updates)
        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
