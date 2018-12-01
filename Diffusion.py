
import networkx as nx
from ndlib.viz.bokeh.MultiPlot import MultiPlot
import ndlib.models.epidemics.IndependentCascadesModel as ids
import ndlib.models.ModelConfig as m
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
import ndlib.models.epidemics.ThresholdModel as th
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
import ndlib.models.epidemics.SIModel as si
from ContinuousTime import ContinuousTime
import sys
import ndlib.models.epidemics.SISModel as sis
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
plot2=DiffusionPrevalence(IDCS, trends).plot(width=400, height=400)
vm.add_plot(plot1)
vm.add_plot(plot2)
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
print(Thr.get_info(), iterations)
trends=Thr.build_trends(iterations)
plot3=DiffusionTrend(Thr, trends).plot(width=400, height=400)
plot4=DiffusionPrevalence(Thr, trends).plot(width=400, height=400)
vm.add_plot(plot3)
vm.add_plot(plot4)




#SI assumes that if, during a generic iteration, a susceptible node comes into contact with an infected one,
# it becomes infected with probability β: once a node becomes infected, it stays infected (the only transition allowed is S→I).
model = si.SIModel(g)

# Model Configuration
cfg = m.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter("percentage_infected", 0.05)
model.set_initial_status(cfg)
iterations = model.iteration_bunch(200)
trends=model.build_trends(iterations)
plot5=DiffusionTrend(model, trends).plot(width=400, height=400)
plot6=DiffusionPrevalence(model, trends).plot(width=400, height=400)
vm.add_plot(plot5)
vm.add_plot(plot6)

model = sis.SISModel(g)

# Model Configuration
cfg = m.Configuration()
cfg.add_model_parameter('beta', 0.02)
cfg.add_model_parameter('lambda', 0.01)
cfg.add_model_parameter("percentage_infected", 0.05)
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(200)
trends=model.build_trends(iterations)
plot7=DiffusionTrend(model, trends).plot(width=400, height=400)
plot8=DiffusionPrevalence(model, trends).plot(width=400, height=400)

vm.add_plot(plot7)
vm.add_plot(plot8)


#---------------------------------------------------------------------------------


# for each of the susceptible nodes’ in the neighborhood of a node u in S an unbalanced coin is flipped, the unbalance given by the personal profile of the susceptible node;
# if a positive result is obtained the susceptible node will adopt the behaviour, thus becoming infected.
# if the blocked status is enabled, after having rejected the adoption with probability blocked a node becomes immune to the infection.
# every iteration adopter_rate percentage of nodes spontaneous became infected to endogenous effects.

import ndlib.models.epidemics.ProfileModel as pr

model = pr.ProfileModel(g)
config = m.Configuration()
config.add_model_parameter('blocked', 0)
config.add_model_parameter('adopter_rate', 0)
config.add_model_parameter('percentage_infected', 0.1)

# Setting nodes parameters
profile = 0.15
for i in g.nodes():
    config.add_node_configuration("profile", i, profile)


model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(200)

trends=model.build_trends(iterations)
plot9=DiffusionTrend(model, trends).plot(width=400, height=400)
plot10=DiffusionPrevalence(model, trends).plot(width=400, height=400)

vm.add_plot(plot9)
vm.add_plot(plot10)

#--------------------------------------------------------------
#Continuous time model
Cont=ContinuousTime(g)
config=m.Configuration()
config.add_model_parameter("percentage_infected",0.2)

Cont.set_initial_status(config)
iterations=Cont.iteration_bunch(10, 0)
print(Cont.get_info())
sys.exit()
trends=Cont.build_trends(iterations)
plot5=DiffusionTrend(Cont, trends).plot(width=400, height=400)
plot6=DiffusionPrevalence(Cont, trends).plot(width=400, height=400)
vm.add_plot(plot5)
vm.add_plot(plot6)

m = vm.plot()
show(m)