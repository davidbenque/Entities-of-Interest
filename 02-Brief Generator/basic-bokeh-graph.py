
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

focus_node = nodes[0]
print("Focus node: "+ str(focus_node))
print("Nodes: ", len(nodes))


links = []

link_query = '''
        MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
        WHERE a.name = {name}
        RETURN a.node_id, b.node_id, c.node_id
        '''

link_results = graph.run(link_query, name = company_name)

def weight(start, end):
    ''' a = array of nodes to check for either start or end at focus node'''
    if focus_node[0] in [start, end]:
        return 1
    else:
        return 0.1

for l in link_results:
    a = int(l["a.node_id"])
    b = int(l["b.node_id"])
    c = int(l["c.node_id"])

    link_1 = (a, b, {'weight': weight(a,b)})
    link_2 = (b, c, {'weight': weight(b,c)})
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
    G.add_edge(edge[0], edge[1], weight = edge[2]['weight'])

print(G.number_of_edges())
print(G.number_of_nodes())


# %%
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.models import HoverTool, Circle, ColumnDataSource, LabelSet

from collections import OrderedDict

node_labels = nx.get_node_attributes(G, 'name')

node_names = []
for node in node_labels:
    name = node_labels[node]
    #name = label(1)
    node_names.append(name)



plot = figure(title=company_name,
            plot_width=600,
            plot_height=600,
            x_range=(-100,100), y_range=(-100,100),
            toolbar_location="right",
            tools="pan,wheel_zoom, hover, box_zoom,reset")



bokeh_graph = from_networkx(G, nx.spring_layout, scale=80, iterations=15, weight='weight')


bokeh_graph.node_renderer.glyph = Circle(size=10)


bokeh_graph.node_renderer.data_source.data['name'] = node_names

# Tooltip with name on hover
hover =plot.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([("Name", "@name")])
bokeh_graph.node_renderer.hover_glyph = Circle(size=10, fill_color='red')
bokeh_graph.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(bokeh_graph)

output_file(company_name + "_graph.html")
show(plot)
