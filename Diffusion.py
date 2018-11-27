
import networkx as nx
from ndlib.viz.bokeh.MultiPlot import MultiPlot
import ndlib.models.epidemics.IndependentCascadesModel as ids
import ndlib.models.ModelConfig as m
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
import ndlib.models.epidemics.ThresholdModel as th

vm = MultiPlot()

g = nx.barabasi_albert_graph(1000,3)

model = ids.IndependentCascadesModel(g)
config= m.Configuration()
config.add_model_parameter("percentage_infected",0.15)
for e in g.edges():
    config.add_edge_configuration("threshold",e,0.15)

model.set_initial_status(config)
iterations=model.iteration_bunch(200,0)
print(model.get_info())
trends=model.build_trends(iterations)
plot1=DiffusionTrend(model,trends).plot(width=400,height=400)
vm.add_plot(plot1)

#------------------------------------------------------


model1=th.ThresholdModel(g)
config=m.Configuration()
config.add_model_parameter("percentage_infected",0.15)

for i in g.nodes():
    config.add_node_configuration("threshold", i, 0.15)

model1.set_initial_status(config)
iterations=model1.iteration_bunch(200,0)
print(model1.get_info())
trends=model1.build_trends(iterations)
plot2=DiffusionTrend(model1,trends).plot(width=400,height=400)
vm.add_plot(plot2)

m = vm.plot()
show(m)



