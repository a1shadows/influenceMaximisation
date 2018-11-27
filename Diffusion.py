
import networkx as nx
from ndlib.viz.bokeh.MultiPlot import MultiPlot
import ndlib.models.epidemics.IndependentCascadesModel as ids
import ndlib.models.ModelConfig as m
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
import ndlib.models.epidemics.ThresholdModel as th
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
import numpy
vm = MultiPlot()

g = nx.barabasi_albert_graph(1000,3)
#When node v becomes active in step t, it is given a single chance to activate each currently inactive neighbor w; it succeeds with a probability p(v,w).
#If w has multiple newly activated neighbors, their attempts are sequenced in an arbitrary order.
#If v succeeds, then w will become active in step t + 1; but whether or not v succeeds, it cannot make any further attempts to activate w in subsequent rounds.
#The process runs until no more activations are possible.
IDCS = ids.IndependentCascadesModel(g)
config= m.Configuration()
config.add_model_parameter("percentage_infected",0.20)
for e in g.edges():
    config.add_edge_configuration("threshold",e,0.6)

IDCS.set_initial_status(config)
iterations=IDCS.iteration_bunch(10, 0)
print(IDCS.get_info())
trends=IDCS.build_trends(iterations)
#Diﬀusion Trend plots describe the evolution of a diﬀusion process as time goes by from the classes distribution point of view
#Diffusion Prevalence one that captures, for each iteration, the variation of the nodes of each class
plot1=DiffusionTrend(IDCS, trends).plot(width=400, height=400)
plot3=DiffusionPrevalence(IDCS, trends).plot(width=400, height=400)
vm.add_plot(plot1)

#------------------------------------------------------

#In this model during an epidemics, a node has two distinct and mutually exclusive behavioral alternatives,
# e.g., the decision to do or not do something, to participate or not participate in a riot.
#Node’s individual decision depends on the percentage of its neighbors have made the same choice, thus imposing a threshold.
#The model works as follows: - each node has its own threshold; - during a generic iteration every node is observed:
# If the percentage of its infected neighbors is grater than its threshold it becomes infected as well.


Thr=th.ThresholdModel(g)
config=m.Configuration()
config.add_model_parameter("percentage_infected",0.2)

for i in g.nodes():
    config.add_node_configuration("threshold", i, 0.05)

Thr.set_initial_status(config)
iterations=Thr.iteration_bunch(10, 0)
print(Thr.get_info())
trends=Thr.build_trends(iterations)
plot2=DiffusionTrend(Thr, trends).plot(width=400, height=400)
plot4=DiffusionPrevalence(Thr, trends).plot(width=400, height=400)
vm.add_plot(plot2)
vm.add_plot(plot3)
vm.add_plot(plot4)

m = vm.plot()
show(m)



