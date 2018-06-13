
import networkx as nx

# %%

G = nx.Graph()

nodes = [(0,{'name':'boso'}), (1,{'name':'bipo'}), (2, {'name':'bopu'}), (3, {'name':'one'})]
links = [(0,2), (0,3), (1,0), (2,0)]

for n in nodes:
    G.add_node(n[0], name = n[1]["name"])

for edge in links:
    G.add_edge(edge[0], edge[1])

# %%

G.nodes(data=True)

# %%
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.models import HoverTool, Oval, ColumnDataSource, LabelSet

plot = figure(title="Networkx Integration Demonstration",
            plot_width=800,
            plot_height=800,
            x_range=(-100,100), y_range=(-100,100),
            toolbar_location="right",
            tools="pan,wheel_zoom,box_zoom,reset")

hover = HoverTool(tooltips=[("Name", "@name")])
plot.add_tools(hover)

bokeh_graph = from_networkx(G, nx.spring_layout, scale=80)
bokeh_graph.node_renderer.glyph = Oval(height=4, width=4)
bokeh_graph.inspection_policy = NodesAndLinkedEdges()
plot.renderers.append(bokeh_graph)

x, y = zip(*bokeh_graph.layout_provider.graph_layout.values())
node_labels = nx.get_node_attributes(G, 'name')
source = ColumnDataSource({'x': x, 'y': y,
                           'name': [node_labels[i] for i in range(len(x))]})
labels = LabelSet(x='x', y='y', text='name', source=source,
                  background_fill_color='white')

plot.renderers.append(labels)

output_file("networkx_graph.html")
show(plot)
