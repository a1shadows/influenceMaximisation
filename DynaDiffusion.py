from ndlib.models.DiffusionModel import DiffusionModel
import numpy as np
import future.utils
import networkx as nx
import math

class DynaDiffusion(DiffusionModel):


    def __init__(self, graph):
        # Call the super class constructor
        super(self.__class__, self).__init__(graph)

        # Method name
        self.name = "DynaDiffusion"

        # Available node statuses
        self.available_statuses = {
            "Susceptible": 0,
            "Infected": 1,
            "removed": 2
        }
        # Exposed Parameters
        self.parameters = {
            "model": {
                "last":{
                    "descr" : "Last Time Allowed",
                    "optional" : True,
                    "default" : 1000


                }
            },
            "nodes":{
                "time": {
                "descr": "Node time",
                "optional": True,
                "default": 10
            },  "deacaying":{
                    "descr": "Node Decay",
                    "optional":True
                }

        },
            "edges":{
                "alpha":{
                    "descr" : "alpha strength",
                    "optional":True,
                    "range":[0,1],
                     "default": 0.4
                }
            }
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



            for u in self.graph.nodes():
                self.actual_iteration+=1
                if self.status[u] != 1:
                    continue
                if self.params['model']['last'] > self.actual_iteration:
                    break
                neighbors = list(self.graph.neighbors(u))
                Time1=self.actual_iteration
                self.params['nodes']['decaying'][u] = Time1

                for v in neighbors:
                    self.actual_iteration+= 1
                    Value=self.params['nodes']['decaying'][u]
                    self.params['nodes']['decaying'][u]= Value*(1+math.e**(self.actual_iteration-Time1))
                    if self.params['nodes']['decaying'][u] < 0.05:
                        self.status['u']=2

                    if actual_status[v] == 0:
                        key = (u, v)

                        if 'alpha' in self.params['edges']:
                            if key in self.params['edges']['alpha']:
                                alpha = self.params['edges']['threshold'][key]
                            elif (v, u) in self.params['edges']['alpha'] and not nx.is_directed(self.graph):
                                alpha = self.params['edges']['threshold'][(v, u)]

                        Time2=self.actual_iteration
                        equation1=math.e**(alpha)*(Time2-Time1)
                        equation2=1-equation1

                        flip = np.random.random_sample()

                        if equation2 >= flip:
                            actual_status[v]=1

                delta, node_count, status_delta = self.status_delta(actual_status)
                self.status = actual_status
                self.actual_iteration += 1

                if node_status:
                    return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                            "node_count": node_count.copy(), "status_delta": status_delta.copy()}
                else:
                    return {"iteration": self.actual_iteration - 1, "status": {},
                            "node_count": node_count.copy(), "status_delta": status_delta.copy()}
