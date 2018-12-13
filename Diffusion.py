import ndlib.models.ModelConfig as m
import ndlib.models.epidemics.IndependentCascadesModel as ids
import ndlib.models.epidemics.SEIRModel as seir
import ndlib.models.epidemics.SIModel as si
import ndlib.models.epidemics.SISModel as sis
import ndlib.models.epidemics.SWIRModel as swir
import ndlib.models.epidemics.ThresholdModel as th
import ndlib.models.opinions.AlgorithmicBiasModel as ab
import ndlib.models.opinions.MajorityRuleModel as mr
import ndlib.models.opinions.VoterModel as vt
import networkx as nx
from bokeh.io import show
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.MultiPlot import MultiPlot

from DiffDyna import DynaDiffuse
# from EpinionsGraph import makeEpinionsGraph as makeEGraph
from TimeAware import TimeAware
from Triggering import Triggering

vm = MultiPlot()
g = nx.barabasi_albert_graph(20000, 3)
# g = makeEGraph()

# When node v becomes active in step t, it is given a single chance to activate each currently inactive neighbor w; it succeeds with a probability p(v,w).
# If w has multiple newly activated neighbors, their attempts are sequenced in an arbitrary order.
# If v succeeds, then w will become active in step t + 1; but whether or not v succeeds, it cannot make any further attempts to activate w in subsequent rounds.
# The process runs until no more activations are possible.
IDCS = ids.IndependentCascadesModel(g)
config = m.Configuration()
config.add_model_parameter("percentage_infected", 0.20)
for e in g.edges():
    config.add_edge_configuration("threshold", e, 0.4)

IDCS.set_initial_status(config)
iterations = IDCS.iteration_bunch(10, 0)
print(IDCS.get_info())
trends = IDCS.build_trends(iterations)
# Diﬀusion Trend plots describe the evolution of a diﬀusion process as time goes by from the classes distribution point of view
# Diffusion Prevalence one that captures, for each iteration, the variation of the nodes of each class
plot1 = DiffusionTrend(IDCS, trends).plot(width=400, height=400)
plot2 = DiffusionPrevalence(IDCS, trends).plot(width=400, height=400)
vm.add_plot(plot1)
vm.add_plot(plot2)
# ------------------------------------------------------

# In this model during an epidemics, a node has two distinct and mutually exclusive behavioral alternatives,
# e.g., the decision to do or not do something, to participate or not participate in a riot.
# Node’s individual decision depends on the percentage of its neighbors have made the same choice, thus imposing a threshold.
# The model works as follows: - each node has its own threshold; - during a generic iteration every node is observed:
# If the percentage of its infected neighbors is grater than its threshold it becomes infected as well.


Thr = th.ThresholdModel(g)
config = m.Configuration()
config.add_model_parameter("percentage_infected", 0.2)

for i in g.nodes():
    config.add_node_configuration("threshold", i, 0.05)

Thr.set_initial_status(config)
iterations = Thr.iteration_bunch(10, 0)
print(Thr.get_info())
trends = Thr.build_trends(iterations)
plot3 = DiffusionTrend(Thr, trends).plot(width=400, height=400)
plot4 = DiffusionPrevalence(Thr, trends).plot(width=400, height=400)
vm.add_plot(plot3)
vm.add_plot(plot4)

# --------------------------------------------------------


# SI assumes that if, during a generic iteration, a susceptible node comes into contact with an infected one,
# it becomes infected with probability β: once a node becomes infected, it stays infected (the only transition allowed is S→I).
model = si.SIModel(g)

# Model Configuration
cfg = m.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter("percentage_infected", 0.05)
model.set_initial_status(cfg)
iterations = model.iteration_bunch(100)
trends = model.build_trends(iterations)
plot5 = DiffusionTrend(model, trends).plot(width=400, height=400)
plot6 = DiffusionPrevalence(model, trends).plot(width=400, height=400)
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
iterations = model.iteration_bunch(100)
trends = model.build_trends(iterations)
plot7 = DiffusionTrend(model, trends).plot(width=400, height=400)
plot8 = DiffusionPrevalence(model, trends).plot(width=400, height=400)

vm.add_plot(plot7)
vm.add_plot(plot8)

# The Voter model is one of the simplest models of opinion dynamics, originally introduced to analyse competition of species [1] and soon after applied to model elections [2].
# The model assumes the opinion of an individual to be a discrete variable ±1.
# The state of the population varies based on a very simple update rule: at each iteration, a random individual is selected, who then copies the opinion of one random neighbour.
# Starting from any initial configuration, on a complete network the entire population converges to consensus on one of the two options. The probability that consensus is reached on opinion +1 is equal to the initial fraction of individuals holding that opinion [3].

Voter = vt.VoterModel(g)
config = m.Configuration()
config.add_model_parameter('percentage_infected', 0.1)

Voter.set_initial_status(config)

iterations = Voter.iteration_bunch(100)
trends = Voter.build_trends(iterations)
plotX1 = DiffusionTrend(Voter, trends).plot(width=400, height=400)
plotX2 = DiffusionPrevalence(Voter, trends).plot(width=400, height=400)

vm.add_plot(plotX1)
vm.add_plot(plotX2)

# The Sznajd mode is a variant of spin model employing the theory of social impact, which takes into account the fact that a group of individuals with the same opinion can influence their neighbours more than one single individual.
# In the original model the social network is a 2-dimensional lattice, however we also implemented the variant on any complex networks.
# Each agent has an opinion σi = ±1. At each time step, a pair of neighbouring agents is selected and, if their opinion coincides, all their neighbours take that opinion.
# The model has been shown to converge to one of the two agreeing stationary states, depending on the initial density of up-spins (transition at 50% density).
import ndlib.models.opinions.SznajdModel as sn

Sznajd = sn.SznajdModel(g)
config = m.Configuration()
config.add_model_parameter('percentage_infected', 0.1)
Sznajd.set_initial_status(config)
iterations = Sznajd.iteration_bunch(100)
trends = Sznajd.build_trends(iterations)
plotX3 = DiffusionTrend(Sznajd, trends).plot(width=400, height=400)
plotX4 = DiffusionPrevalence(Voter, trends).plot(width=400, height=400)

vm.add_plot(plotX3)
vm.add_plot(plotX4)

# ---------------------------------------------------------------------------------


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
iterations = model.iteration_bunch(100)

trends = model.build_trends(iterations)
plot9 = DiffusionTrend(model, trends).plot(width=400, height=400)
plot10 = DiffusionPrevalence(model, trends).plot(width=400, height=400)

vm.add_plot(plot9)
vm.add_plot(plot10)

# The Algorithmic Bias model considers a population of individuals, where each individual holds a continuous opinion in the interval [0,1].
# Individuals are connected by a social network, and interact pairwise at discrete time steps. The interacting pair is selected from the population at each time point in
# such a way that individuals that have close opinion values are selected more often, to simulate algorithmic bias.
# The parameter gamma controls how large this effect is. Specifically, the first individual in the interacting pair is selected randomly,
# while the second individual is selected based on a probability that decreases with the distance from the opinion of the first individual,
# i.e. directly proportional with the distance raised to the power -gamma.

# After interaction, the two opinions may change, depending on a so called bounded confidence parameter, epsilon. This can be seen as a measure of the open-mindedness of individuals in a population.


Algorithmic = ab.AlgorithmicBiasModel(g)

config = m.Configuration()
config.add_model_parameter("epsilon", 0.02)
config.add_model_parameter("gamma", 1)
config.add_model_parameter('percentage_infected', 0.2)
Algorithmic.set_initial_status(config)

iterations = Algorithmic.iteration_bunch(100, 0)

trends = Algorithmic.build_trends(iterations)
plotA1 = DiffusionTrend(Algorithmic, trends).plot(width=400, height=400)
plotA2 = DiffusionPrevalence(Algorithmic, trends).plot(width=400, height=400)
vm.add_plot(plotA1)
vm.add_plot(plotA2)

# In this model, during the epidemics, a node is allowed to change its status from Susceptible (S) to Weakened (W) or Infected (I), then to Removed (R).

# The model is instantiated on a graph having a non-empty set of infected nodes.

# At time t a node in the state I is selected randomly and the states of all neighbors are checked one by one.
# If the state of a neighbor is S then this state changes either i) to I with probability kappa or ii) to W with probability mu. If the state of a neighbor is W
# then the state W changes to I with probability nu.
# We repeat the above process for all nodes in state I and then changes to R for each associated node.

SWIREN = swir.SWIRModel(g)
cfg = m.Configuration()
cfg.add_model_parameter('kappa', 0.01)
cfg.add_model_parameter('mu', 0.005)
cfg.add_model_parameter('nu', 0.05)
cfg.add_model_parameter("percentage_infected", 0.05)

SWIREN.set_initial_status(cfg)
iterations = SWIREN.iteration_bunch(100, 0)

trends = SWIREN.build_trends(iterations)

plotSW1 = DiffusionTrend(SWIREN, trends).plot(width=400, height=400)
plotSW2 = DiffusionPrevalence(SWIREN, trends).plot(width=400, height=400)
vm.add_plot(plotSW1)
vm.add_plot(plotSW2)

# In the SEIR model [1], during the course of an epidemics, a node is allowed to change its status from Susceptible (S) to Exposed (E) to Infected (I), then to Removed (R).
# The model is instantiated on a graph having a non-empty set of infected nodes.
# SEIR assumes that if, during a generic iteration, a susceptible node comes into contact with an infected one,
# it becomes infected after an exposition period with probability beta, than it can switch to removed with probability gamma (the only transition allowed are S→E→I→R).

SEIRI = seir.SEIRModel(g)

cfg = m.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter('gamma', 0.005)
cfg.add_model_parameter('alpha', 0.05)
cfg.add_model_parameter("percentage_infected", 0.05)
SEIRI.set_initial_status(cfg)

iterations = SEIRI.iteration_bunch(100)

print(SEIRI.get_info())

trends = SEIRI.build_trends(iterations)

plotSE1 = DiffusionTrend(SEIRI, trends).plot(width=400, height=400)
plotSE2 = DiffusionPrevalence(SEIRI, trends).plot(width=400, height=400)

vm.add_plot(plotSE1)
vm.add_plot(plotSE2)

# The Majority Rule model is a discrete model of opinion dynamics, proposed to describe public debates [1].
# Agents take discrete opinions ±1, just like the Voter model. At each time step a group of r agents is selected randomly and they all take the majority opinion within the group.
# The group size can be fixed or taken at each time step from a specific distribution. If r is odd, then the majority opinion is always defined, however if r is even there could be tied situations. To select a prevailing opinion in this case, a bias in favour of one opinion (+1) is introduced.
# This idea is inspired by the concept of social inertia


Majority = mr.MajorityRuleModel(g)
config = m.Configuration()
config.add_model_parameter('percentage_infected', 0.1)
config.add_model_parameter('q', 20)

Majority.set_initial_status(config)

trends = Majority.build_trends(iterations)

plotMAJ1 = DiffusionTrend(Majority, trends).plot(width=400, height=400)
plotMAJ2 = DiffusionPrevalence(Majority, trends).plot(width=400, height=400)

vm.add_plot(plotMAJ1)
vm.add_plot(plotMAJ2)
# --------------------------------------------------------------
# Continuous time model
TAmodel = TimeAware(g)
config = m.Configuration()
config.add_model_parameter("percentage_infected", 0.2)

TAmodel.set_initial_status(config)
iterations = TAmodel.iteration_bunch(100, 0)
print(TAmodel.get_info())
trends = TAmodel.build_trends(iterations)
plot5 = DiffusionTrend(TAmodel, trends).plot(width=400, height=400)
plot6 = DiffusionPrevalence(TAmodel, trends).plot(width=400, height=400)
vm.add_plot(plot5)
vm.add_plot(plot6)

# --------------------------------------------------------------
# Triggering Model

Trigg = Triggering(g)
config = m.Configuration()
config.add_model_parameter("percentage_infected", 0.2)

Trigg.set_initial_status(config)
iterations = Trigg.iteration_bunch(100, 0)
print(Trigg.get_info(), iterations)
trends = Trigg.build_trends(iterations)
plotTrigg1 = DiffusionTrend(Trigg, trends).plot(width=400, height=400)
plotTrigg2 = DiffusionPrevalence(Trigg, trends).plot(width=400, height=400)
vm.add_plot(plotTrigg1)
vm.add_plot(plotTrigg2)
# ----------------Dyna Diffusiion-----------------------
DynaDiffMod = DynaDiffuse(g)
config = m.Configuration()
config.add_model_parameter("percentage_infected", 0.2)

DynaDiffMod.set_initial_status(config)
iterations = DynaDiffMod.iteration_bunch(100, 0)
print(DynaDiffMod.get_info())
trends = DynaDiffMod.build_trends(iterations)
plot5 = DiffusionTrend(DynaDiffMod, trends).plot(width=400, height=400)
plot6 = DiffusionPrevalence(DynaDiffMod, trends).plot(width=400, height=400)
vm.add_plot(plot5)
vm.add_plot(plot6)

m = vm.plot()
show(m)
