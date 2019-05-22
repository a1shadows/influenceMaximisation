
from bokeh.io import curdoc

curdoc().clear()

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
from DynaDiffusion import DynaDiffusion
import ndlib.models.epidemics.SISModel as sis
import ndlib.models.epidemics.GeneralisedThresholdModel as gth
import numpy
from TimeAware import TimeAware
from DiffAware import DiffAware
import ndlib.models.opinions.MajorityRuleModel as mr

vm = MultiPlot()

g = nx.barabasi_albert_graph(1000,3)

for i in numpy.array([0.3,0.4,0.5,0.6]):
    Cont=DiffAware(g)
    config=m.Configuration()
    config.add_model_parameter("percentage_infected",i)
    Cont.set_initial_status(config)
    iterations=Cont.iteration_bunch(10, 0)
    print(Cont.get_info())
#sys.exit()
    trends=Cont.build_trends(iterations)
    plotTime1=DiffusionTrend(Cont, trends).plot(width=400, height=400)
    plotTime2=DiffusionPrevalence(Cont, trends).plot(width=400, height=400)
    vm.add_plot(plotTime1)
    vm.add_plot(plotTime2)


m = vm.plot()
show(m)