# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-06-14 20:37:38
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-06-15 13:17:43


from py2neo import Graph
import pandas as pd

from pathlib import Path

import datashader as ds
import datashader.transfer_functions as tf
from datashader.layout import forceatlas2_layout
from datashader.bundling import connect_edges

from datashader.utils import export_image
import os


# log in to database

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

name_list = pd.read_csv('../01-Name Hunting/_selected_names.csv')
shuffled_names = name_list.sample(frac=1).reset_index(drop=True)
first_row = shuffled_names.iloc[0]


# black_list
# these return empty node lists
blacklist = ["DEEPWATER SHIPPING (MALTA) LIMITED","GOLDEN GLARE INTERNATIONAL LLC","MESS DEVELOPMENT CORP.","SPIRAL FINANCE LIMITED","SUCCESS PEARL LIMITED","THE MAGIC VALLEY INC."]

for index, row in name_list.iterrows():

    company_name = row["name"]
    file = company_name.replace(" ","_")
    file_name = file + ".png"
    saved_file_name = '../../ent-out/' + file_name
    graph_file = Path(saved_file_name)

    if graph_file.exists():
        print("Skipping: " + company_name)
        next(name_list.iterrows())
        continue

    if company_name in blacklist:
        print("Blacklisted: " + company_name)
        next(name_list.iterrows())
        continue

    print("processing: ", company_name)

    # set up dataframes
    nodes_df = pd.DataFrame(columns=['id', 'name', 'type'])
    nodes_df.set_index('id', inplace=True)

    edges_df = pd.DataFrame(columns=['source', 'target'])


    # get nodes

    node_query = '''
            MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
            WHERE a.name = {name}
            RETURN a, b, c
            '''

    node_results = graph.run(node_query, name = company_name)

    for nodes in node_results:
        for node in nodes:
            #row = {"id":int(node["node_id"]),"name": node["name"], "type": list(node.labels())[0]}
            label = list(node.labels())[0]
            name = node["name"] 
            nodes_df.loc[int(node["node_id"])] = {"name": name, "type": label}

    nodes_df.iat[0,1] = 'Focus'
    nodes_df.type = nodes_df.type.astype('category')

    # get links

    link_query = '''
            MATCH (a:Entity)-[r1]-(b)-[r2]-(c)
            WHERE a.name = {name}
            RETURN a.node_id, b.node_id, c.node_id
            '''

    link_results = graph.run(link_query, name = company_name)

    for l in link_results:
        a = int(l["a.node_id"])
        b = int(l["b.node_id"])
        c = int(l["c.node_id"])
        
        if ((edges_df['source'] == a) & (edges_df['target'] == b)).any() == False:
            edges_df.loc[len(edges_df)] = {"source": a, "target": b}
            
        if ((edges_df['source'] == b) & (edges_df['target'] == c)).any() == False:
            edges_df.loc[len(edges_df)] = {"source": b, "target": c}

    edges_df = edges_df.apply(pd.to_numeric)


    # Datashader

    nodes = nodes_df
    edges = edges_df
    print(len(nodes), "Nodes")
    print(len(edges), "Edges")

    cvsopts = dict(plot_height=1000, plot_width=1000)
    colors = {"Focus": "#FF0000", "Officer": "#ff69f9", "Entity": "#0e438a", "Address": "#8bf156", "Intermediary": "#ff8200"}

    def my_nodesplot(nodes, name=None, canvas=None, cat=None):
        canvas = ds.Canvas(**cvsopts) if canvas is None else canvas
        aggregator=None if cat is None else ds.count_cat(cat)
        agg=canvas.points(nodes,'x','y',aggregator)
        return tf.spread(tf.shade(agg, cmap=["#333333"], color_key=colors, min_alpha=255), px=3, name=name)

    def edgesplot(edges, name=None, canvas=None):
        canvas = ds.Canvas(**cvsopts) if canvas is None else canvas
        return tf.shade(canvas.line(edges, 'x','y', agg=ds.count()), name=name)

    def my_graphplot(nodes, edges, name="", canvas=None, cat=None, margin=0.05):
        if canvas is None:
            xr = nodes.x.min() - margin, nodes.x.max() + margin
            yr = nodes.y.min() - margin, nodes.y.max() + margin
            canvas = ds.Canvas(x_range=xr, y_range=yr, **cvsopts)
            
        np = my_nodesplot(nodes, name + " nodes", canvas, cat)
        ep = edgesplot(edges, name + " edges", canvas)
        return tf.stack(ep, np, how="over", name=name)


    forcedirected = forceatlas2_layout(nodes, edges)
    fd = forcedirected

    fd.iat[0,2] = (fd.x.min() + fd.x.max())/2 # center focus node on x
    fd.iat[0,3] = 1 # center focus node on y

    ## save image?!
    
    image = tf.Image(my_graphplot(fd, connect_edges(fd,edges), "Force-directed", cat="type", margin=0.02))

    export_image(image, filename=file)
    os.rename(file_name, saved_file_name)

