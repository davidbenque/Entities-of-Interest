

##############################
##   This does not work yet ##
##############################





from py2neo import Graph
import networkx as nx

# login local ICIJ Neo4j database at http://localhost:7474

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

company_name = "A.C. Futures Inc."

#%%

node_query = '''
        MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
        WHERE a.name = {name}
        RETURN a, b, c
        '''

node_results = graph.run(node_query, name = company_name)

nodes = []
links = []

for n in node_results:
    for i in n:
        node_desc = (int(i["node_id"]), {
                    "type": list(i.labels())[0],
                    "name": i["name"]})

        if node_desc not in nodes:
            nodes.append(node_desc)


focus_node = nodes[0][0]
print(len(nodes), "unique nodes")

link_query = '''
        MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
        WHERE a.name = {name}
        RETURN ID(a), ID(b), ID(c)
        '''

link_results = graph.run(link_query, name = company_name)



for l in link_results:
    link_1 = (int(l["ID(a)"]), int(l["ID(b)"]))
    link_2 = (int(l["ID(b)"]), int(l["ID(c)"]))
    for link in [link_1, link_2]:
        if link not in links:
            links.append(link)

print(len(links), "unique links")
links
nodes[0]

# %%

G = nx.Graph()

for n in nodes:
    G.add_node(n[0], attr_dict=n[1])

for edge in links:
    G.add_edge(edge[0], edge[1])

# %%
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
