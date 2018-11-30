import networkx as nx
from ndlib.viz.bokeh.MultiPlot import MultiPlot

import ndlib.models.ModelConfig as mc
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence


vm = MultiPlot()

g = nx.barabasi_albert_graph(1000,4)
#SI assumes that if, during a generic iteration, a susceptible node comes into contact with an infected one,
# it becomes infected with probability β: once a node becomes infected, it stays infected (the only transition allowed is S→I).
model = si.SIModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter("percentage_infected", 0.05)
model.set_initial_status(cfg)
iterations = model.iteration_bunch(200)
trends=cfg.build_trends(iterations)
plot1=DiffusionTrend(cfg, trends).plot(width=400, height=400)
plot2=DiffusionPrevalence(cfg, trends).plot(width=400, height=400)

#--------------------------------------------------------------------###


model = sis.SISModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.02)
cfg.add_model_parameter('lambda', 0.01)
cfg.add_model_parameter("percentage_infected", 0.05)
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(200)
trends=cfg.build_trends(iterations)
plot1=DiffusionTrend(cfg, trends).plot(width=400, height=400)
plot2=DiffusionPrevalence(cfg, trends).plot(width=400, height=400)