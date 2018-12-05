
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
import ndlib.models.opinions.VoterModel as vt
import ndlib.models.epidemics.SISModel as sis
import ndlib.models.epidemics.GeneralisedThresholdModel as gth
import numpy
from TimeAware import TimeAware
from DynaDiff import DynaDiff
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

#--------------------------------------------------------


#he model is instantiated on a graph having a non-empty set of infected nodes.

#The model is defined as follows:

#At time t nodes become Infected with rate mu t/tau
#Nodes for which the ratio of the active friends dropped below the threshold are moved to the Infected queue
#Nodes in the Infected queue become infected with rate tau. If this happens check all its friends for threshold



Generalised = gth.GeneralisedThresholdModel(g)
config = mc.Configuration()
config.add_model_parameter('percentage_infected', 0.1)
config.add_model_parameter('tau', 5)
config.add_model_parameter('mu', 5)

threshold = 0.25
for i in g.nodes():
    config.add_node_configuration("threshold", i, threshold)

Generalised.set_initial_status(config)
iterations = model.iteration_bunch(10,0)
print(Generalised.get_info(), iterations)
trends=Generalised.build_trends(iterations)
plotX=DiffusionTrend(Generalised,trends).plot(width=400,height=400)
plotY=DiffusionPrevalence(Generalised,trends).plot(width=400,height=400)
vm.add_plot(plotX)
vm.add_plot(plotY)



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

#The Voter model is one of the simplest models of opinion dynamics, originally introduced to analyse competition of species [1] and soon after applied to model elections [2].
#The model assumes the opinion of an individual to be a discrete variable ±1.
#The state of the population varies based on a very simple update rule: at each iteration, a random individual is selected, who then copies the opinion of one random neighbour.
#Starting from any initial configuration, on a complete network the entire population converges to consensus on one of the two options. The probability that consensus is reached on opinion +1 is equal to the initial fraction of individuals holding that opinion [3].

Voter = vt.VoterModel(g)
config = mc.Configuration()
config.add_model_parameter('percentage_infected', 0.1)

Voter.set_initial_status(config)

iterations=Voter.iteration_bunch(200)
trends=Voter.build_trends(iterations)
plotX1=DiffusionTrend(Voter,trends).plot(width=400,height=400)
plotX2=DiffusionPrevalence(Voter,trends).plot(width=400,height=400)

vm.add_plot(plotX1)
vm.add_plot(plotX2)


#The Sznajd model [1] is a variant of spin model employing the theory of social impact, which takes into account the fact that a group of individuals with the same opinion can influence their neighbours more than one single individual.
#In the original model the social network is a 2-dimensional lattice, however we also implemented the variant on any complex networks.
#Each agent has an opinion σi = ±1. At each time step, a pair of neighbouring agents is selected and, if their opinion coincides, all their neighbours take that opinion.
#The model has been shown to converge to one of the two agreeing stationary states, depending on the initial density of up-spins (transition at 50% density).
import ndlib.models.opinions.SznajdModel as sn

Sznajd=sn.SznajdModel(g)
config = mc.Configuration()
config.add_model_parameter('percentage_infected', 0.1)
Sznajd.set_initial_status(config)
iterations=Sznajd.iteration_bunch(200)
trends=Sznajd.build_trends(iterations)
plotX3=DiffusionTrend(Sznajd,trends).plot(width=400,height=400)
plotX4=DiffusionPrevalence(Voter,trends).plot(width=400,height=400)

vm.add_plot(plotX3)
vm.add_plot(plotX4)


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
Cont=DynaDiff(g)
config=m.Configuration()
config.add_model_parameter("percentage_infected",0.2)

Cont.set_initial_status(config)
iterations=Cont.iteration_bunch(10, 0)
print(Cont.get_info())
#sys.exit()
trends=Cont.build_trends(iterations)
plot5=DiffusionTrend(Cont, trends).plot(width=400, height=400)
plot6=DiffusionPrevalence(Cont, trends).plot(width=400, height=400)
vm.add_plot(plot5)
vm.add_plot(plot6)

m = vm.plot()
show(m)