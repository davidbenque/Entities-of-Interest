
#### NEO4J & py2neo ####
#

from py2neo import Graph

# login local ICIJ Neo4j database at http://localhost:7474

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

company_name = "A.C. Futures Inc."

node_query = '''
        MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
        WHERE a.name = {name}
        RETURN a, b, c
        '''

node_results = graph.run(node_query, name = company_name)

nodes = []

for n in node_results:
    for i in n:
        node_desc = (int(i["node_id"]), {"name": i["name"]})

        if node_desc not in nodes:
            nodes.append(node_desc)

print("Nodes: ", len(nodes))


links = []

link_query = '''
        MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
        WHERE a.name = {name}
        RETURN a.node_id, b.node_id, c.node_id
        '''

link_results = graph.run(link_query, name = company_name)

for l in link_results:
    link_1 = (int(l["a.node_id"]), int(l["b.node_id"]))
    link_2 = (int(l["b.node_id"]), int(l["c.node_id"]))
    for link in [link_1, link_2]:
        if link not in links:
            links.append(link)

print("Links: ", len(links))

# %%
import networkx as nx

G = nx.Graph()

for n in nodes:
    G.add_node(n[0], name = n[1]["name"])

for edge in links:
    G.add_edge(edge[0], edge[1])

print(G.number_of_edges())
print(G.number_of_nodes())

# %%
import matplotlib

draw(G)



# %%
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.models import HoverTool, Oval, ColumnDataSource, LabelSet

from collections import OrderedDict

plot = figure(title=company_name,
            plot_width=800,
            plot_height=800,
            x_range=(-100,100), y_range=(-100,100),
            toolbar_location="right",
            tools="pan,wheel_zoom,box_zoom,reset")

node_labels = nx.get_node_attributes(G, 'name')

node_names = []
for node in node_labels:
    name = node_labels[node]
    #name = label(1)
    node_names.append(name)

source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in node_labels.keys()]})

hover = HoverTool(tooltips=[("Name:", "@name")])
plot.add_tools(hover)


bokeh_graph = from_networkx(G, nx.spring_layout, scale=80)
bokeh_graph.node_renderer.glyph = Oval(height=0.5, width=0.5)
bokeh_graph.node_renderer.data_source.data['name'] = node_names

bokeh_graph.inspection_policy = NodesAndLinkedEdges()
plot.renderers.append(bokeh_graph)

# x, y = zip(*bokeh_graph.layout_provider.graph_layout.values())
# node_labels = nx.get_node_attributes(G, 'name')
#
# source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in node_labels.keys()]})
# labels = LabelSet(x='x', y='y', text='name', source=source,
#                   background_fill_color='white')
#
# plot.renderers.append(labels)

output_file("networkx_graph.html")
show(plot)
