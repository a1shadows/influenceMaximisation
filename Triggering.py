from ndlib.models.DiffusionModel import DiffusionModel
import future.utils
import networkx as nx
import numpy as np

class Triggering(DiffusionModel):

        def __init__(self, graph):

                # Call the super class constructor
                super(self.__class__, self).__init__(graph)

                # Method name
                self.name = "Triggering"

                # Available node statuses
                self.available_statuses = {
                        "Susceptible": 0,
                        "Infected": 1
                }
                # Exposed Parameters
                self.parameters = {
                        "model": {},
                        "nodes":{
                                "probability": {
                                        "descr": "probability of getting selected in set",
                                        "range": [0,1],
                                        "default": 0.5,
                                        "optional": True
                                        },
                                "iterActivated": {
                                    "descr": "Description 2",
                                    "default": 0,
                                    "optional": True
                                },
                        },
                        "edges": {}
                }

        def iteration(self, node_status=True):

            self.clean_initial_status(self.available_statuses.values())
            actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}
            # if first iteration return the initial node status
            if self.actual_iteration == 0:
                self.actual_iteration += 1
                delta, node_count, status_delta = self.status_delta(actual_status)
                if node_status:
                    return {"iteration": 0, "status": actual_status.copy(),
                            "node_count": node_count.copy(), "status_delta": status_delta.copy()}
                else:
                    return {"iteration": 0, "status": {},
                            "node_count": node_count.copy(), "status_delta": status_delta.copy()}


            # iteration inner loop
            for u in self.graph.nodes():
                if actual_status[u] == 1:
                    continue

                neighbors = list(self.graph.neighbors(u))
                if isinstance(self.graph, nx.DiGraph):
                    neighbors = list(self.graph.predecessors(u))

                for v in neighbors:
                    flip = np.random.random_sample()
                    iter_no = self.params['nodes']['iterActivated'][v]
                    prob = self.params['nodes']['probability'][v]
                    if prob <= flip and iter_no == self.actual_iteration - 1 and \
                            actual_status[v] == 1:
                        #actual_status[u] = 1
                        self.params['nodes']['iterActivated'][u] = self.actual_iteration
                        break

            # identify the changes w.r.t. previous iteration
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