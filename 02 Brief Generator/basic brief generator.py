# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-03-29 11:14:25
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-05-30 16:19:35

from py2neo import Graph
import itertools

# login local ICIJ Neo4j database at http://localhost:7474

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)


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


company_name = "In the Name of the Father Ltd"

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

import sys
sys.stdout = open('file.md', 'w')

# Company Details
print("#" + start["a"]["name"])

basic_info = ["company_type", "status", "address"]

for deet in basic_info:
    if entity_node[deet]:
        print(deet.title() + ": " + entity_node[deet]) 
print("")


# Generator check 

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)

# Incoming links 
incoming_nodes = graph.match(end_node = entity_node)
in_check = peek(incoming_nodes)

if in_check is None:
    print("")
else:
    print("--- Incoming ---")
    first, nodelist = in_check
    for i in nodelist:
        link_type = i.type()
        if link_type.endswith("_OF"):
            link_type = link_type[:-3]
        print(link_type)
        source_dict = parse_node(i.start_node())
        for key, i in source_dict.items():
            if i:
                print(i)
        print("")

# Outgoing links 
outgoing_nodes = graph.match(start_node = entity_node)
out_check = peek(outgoing_nodes)

if out_check is None:
    print("")
else:
    print("--- Outgoing ---")
    first, nodelist = out_check
    for i in outgoing_nodes:
        link_type = i.type()
        if link_type.endswith("_OF"):
            link_type = link_type[:-3]
        print(link_type)

        source_dict = parse_node(i.end_node())
        for key, i in source_dict.items():
            if i:
                print(i)
        print("")


# Network
print("--- Graph ---")

print("```mermaid")
print("graph TD")

target = parse_node(entity_node)
target_graphnode = target["name"]

print("target[" + target_graphnode + "]")
print("class target outline")
print("classDef outline fill:#fff,stroke:#000,stroke-width:1px;")

source_index = 1

for i in graph.match(end_node = entity_node):
    source = parse_node(i.start_node())
    source_graphnode = source["name"] + "<br>" + source["countries"]
    source_ref = "source" + str(source_index)
    source_index += 1
    print(source_ref + "[" + source_graphnode + "]")
    print(source_ref + "-->|" + i.type() + "|target")

    #print(source["name"], "-->|" + i.type())

print("```")

