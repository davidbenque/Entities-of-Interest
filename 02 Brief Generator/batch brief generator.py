# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-03-29 11:14:25
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-05-31 12:14:53

from py2neo import Graph
import itertools
import os
import pandas as pd

# login local ICIJ Neo4j database at http://localhost:7474

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

name_list = pd.read_csv('../01 Name Hunting/_selected_names.csv')
shuffled_names = name_list.sample(frac=1).reset_index(drop=True)


## Functions

def parse_node(node):
    ''' returns a dict of properties for a graph node'''
    label = list(node.labels())[0] # assumes 1 label per node
    if label == "Officer":
        return {"name": node["name"], "countries": node["countries"]}
    elif label == "Intermediary":
        return {"name": node["name"], "address": node["address"], "countries": node["countries"]}
    elif label == "Address":
        return {"address": node["address"], "countries": node["countries"]}
    elif label == "Entity":
        return {"name": node["name"], "address": node["address"]}


# Generator check - see if there are any incoming/outgoing links to display

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)


def graph_node_label(node):

    try:
        a = node["name"]
    except:
        a = "" #node["address"]

    try:
        b = node["countries"]
    except:
        b = ""

    return str(a) + "<br>" + str(b)


def graphnode(input_node):
    global node_index, graph_nodes

    node = parse_node(input_node)
    graphnode = graph_node_label(node)
    node_name = add_graph_node(graphnode, graph_nodes)
    

    for i in graph.match(end_node = input_node):
        node_queue.append(i.start_node())

        source = parse_node(i.start_node())
        source_graphnode = graph_node_label(source)

        source_name = add_graph_node(source_graphnode, graph_nodes)
        file.write(source_name + "-->|" + i.type() + "|" +  node_name + "\n")

    for i in graph.match(start_node = input_node):

        target = parse_node(i.end_node())
        target_graphnode = graph_node_label(target)

        target_name = add_graph_node(target_graphnode, graph_nodes)

        file.write(node_name + "-->|" + i.type() + "|" +  target_name + "\n")

############
# Loop through all names in the list and generate a brief for each
############

for index, row in name_list.iterrows():

    company_name = row["name"]

    file = open('briefs/' + company_name + '.md', 'w')
    print("processing: ", company_name)

    # Get the node from the graph
    query = '''
        MATCH (a:Entity)
        WHERE a.name = {name}
        RETURN a
        '''

    entity = graph.run(query, name = company_name)
    entity.forward()
    start = entity.current()
    start_id = start["a"]["node_id"]
    entity_node = graph.find_one("Entity", "node_id", start_id)



    # Company Details
    file.write("#" + start["a"]["name"] + "\n")

    basic_info = ["company_type", "status", "address"]

    for deet in basic_info:
        if entity_node[deet]:
            file.write(deet.title() + ": " + entity_node[deet] + "\n") 
    file.write("\n")


    

    # Incoming links 
    incoming_nodes = graph.match(end_node = entity_node)
    in_check = peek(incoming_nodes)

    if in_check is None:
        file.write("" + "\n")
    else:
        file.write("##Incoming" + "\n")
        first, nodelist_in = in_check
        for i in nodelist_in:
            link_type = i.type()
            if link_type.endswith("_OF"):
                link_type = link_type[:-3]
            file.write(link_type + "\n")
            source_dict = parse_node(i.start_node())
            for key, i in source_dict.items():
                if i:
                    file.write(i + "\n" )
            file.write("" + "\n" + "\n")

    # Outgoing links 

    outgoing_nodes = graph.match(start_node = entity_node)
    out_check = peek(outgoing_nodes)

    if out_check is None:
        file.write("" + "\n")
    else:
        file.write("##Outgoing" + "\n")
        first, nodelist_out = out_check
        for i in nodelist_out:
            link_type = i.type()
            if link_type.endswith("_OF"):
                link_type = link_type[:-3]
            file.write(link_type)

            source_dict = parse_node(i.end_node())
            for key, i in source_dict.items():
                if i:
                    file.write(i + "\n")
            file.write("" + "\n" + "\n") 


    # Network Graph


    file.write("##Graph" + "\n")

    file.write("```mermaid" + "\n")
    file.write("graph LR" + "\n")

    file.write("classDef outline fill:#fff,stroke:#000,stroke-width:1px;" + "\n")

    node_index = 1
    graph_nodes = {}
    node_queue = []





    def add_graph_node(graph_node, node_dict):
        global node_index, graph_nodes
        if graph_node not in graph_nodes.values():
            graph_nodes["node" + str(node_index)] = graph_node
            node_index += 1

            node_name = list(graph_nodes.keys())[list(graph_nodes.values()).index(graph_node)]

            # remove special characters as they break the mermaid graph syntax
            display_name = graph_node.translate(str.maketrans({
                                            "(": r"%28",
                                            ")": r"%29",
                                            "]": r"%5D",
                                            "{": r"%7B",
                                            "}": r"%7D",
                                            ".": r"",
                                            ";": r" ",
                                            "·": r"",
                                            "@": r"",
                                            "'": r"%27",
                                            "’": r"%27",
                                              "[":  r"%5B"}))
            file.write(node_name + "[" + display_name + "]" + "\n")

        node_name = list(graph_nodes.keys())[list(graph_nodes.values()).index(graph_node)]
        return node_name


    



    graphnode(entity_node)
    file.write("class node1 outline" + "\n")

    for node in node_queue:
        graphnode(node)


    file.write("```")

