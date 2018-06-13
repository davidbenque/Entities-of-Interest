
import networkx as nx

G = nx.Graph()

nodes = [(1,'one'), (2,'two'), (3, 'three'), (4, 'four')]
links = [(1,2), (1,3), (1,4), (2,4)]

for n in nodes:
    G.add_node(n[0], attr_dict=n[1])

for edge in links:
    G.add_edge(edge[0], edge[1])

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx

plot = figure(title="Networkx Integration Demonstration",
            plot_width=800,
            plot_height=800,
            x_range=(-100,100), y_range=(-100,100),
            toolbar_location="right",
            tools="pan,wheel_zoom,box_zoom,reset")

bokeh_graph = from_networkx(G, nx.spring_layout, scale=80)

plot.renderers.append(bokeh_graph)

output_file("networkx_graph.html")
show(plot)
